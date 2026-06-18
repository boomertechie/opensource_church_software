#!/usr/bin/env python3
"""Audit GitHub repos linked from category READMEs and flag dead/archived ones.

Walks markdown files under the repo root, extracts every `github.com/owner/repo`
link, queries the GitHub API for each, and posts a single rolling "Listed-repo
health report" issue. Repos that haven't seen a non-bot commit within
STALE_DAYS, or that are archived, are flagged.

Link tiering
------------
Each repo is classified into one of three tiers:

  recommended  (default) — checked and flagged normally.
  historical   — upstream/predecessor repos credited for provenance;
                 informational only; never flagged.
  archaeology  — explicitly-abandoned projects documented for historical
                 context only; never flagged.

Explicit tiers are loaded from `.github/listed-repos-tiers.txt`.

Auto-archaeology heuristic
---------------------------
If the link's containing line OR the nearest preceding heading (## / ###)
contains any of the following markers, the repo is auto-classified as
archaeology regardless of the tiers file:

  - "Not Recommended"  (case-insensitive)
  - "⛔"
  - "for archaeology only"  (case-insensitive)

This catches the common pattern where a section is explicitly called out in
the docs as abandoned without needing a manual entry in the tiers file.

Designed to flag-not-fix: the maintainer reviews the issue and decides what
needs to be edited in the category READMEs.

Run locally with:
  GITHUB_TOKEN=$(gh auth token) GITHUB_REPOSITORY=owner/repo \\
  DRY_RUN=1 python scripts/check_listed_repos.py
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKEN = os.environ.get("GITHUB_TOKEN")
REPO = os.environ.get("GITHUB_REPOSITORY")
DRY_RUN = bool(os.environ.get("DRY_RUN"))

STALE_DAYS = int(os.environ.get("STALE_DAYS", "365"))
SKIP_FILE = ROOT / ".github" / "listed-repos-skip.txt"
TIERS_FILE = ROOT / ".github" / "listed-repos-tiers.txt"
REPORT_TITLE_PREFIX = "Listed-repo health report"
REPORT_LABEL = "maintenance"

LINK_RE = re.compile(
    r"https?://github\.com/(?P<owner>[A-Za-z0-9][A-Za-z0-9_.-]*)"
    r"/(?P<repo>[A-Za-z0-9][A-Za-z0-9_.-]*)"
)
BOT_RE = re.compile(
    r"\[bot\]|\bbot\b|dependabot|renovate|github-actions|pre-commit-ci",
    re.IGNORECASE,
)
RESERVED_OWNERS = {
    "orgs", "users", "marketplace", "topics", "settings",
    "features", "about", "pricing", "sponsors", "apps", "search",
}

# Patterns that auto-classify a link as archaeology when found in its
# surrounding line or the nearest preceding heading.
ARCHAEOLOGY_MARKERS_RE = re.compile(
    r"Not Recommended|⛔|for archaeology only",
    re.IGNORECASE,
)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+)", re.MULTILINE)


# ---------------------------------------------------------------------------
# Tier loading
# ---------------------------------------------------------------------------

def load_tiers() -> dict[str, str]:
    """Return {slug_lower: tier} from the tiers file.

    Lines have the form:  <tier> <owner/repo>
    Blank lines and lines starting with # are ignored.
    """
    tiers: dict[str, str] = {}
    if not TIERS_FILE.exists():
        return tiers
    for raw in TIERS_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) == 2:
            tier, slug = parts
            tiers[slug.lower()] = tier.lower()
    return tiers


def _nearest_preceding_heading(lines: list[str], link_line_idx: int) -> str:
    """Return the text of the nearest ## or ### heading above link_line_idx."""
    for i in range(link_line_idx - 1, -1, -1):
        m = HEADING_RE.match(lines[i])
        if m:
            return m.group(1)
    return ""


def classify_link(slug_lower: str, link_line: str, nearest_heading: str,
                  explicit_tiers: dict[str, str]) -> str:
    """Return the tier string for this slug.

    Priority:
      1. Explicit entry in tiers file.
      2. Auto-archaeology heuristic on containing line + nearest heading.
      3. 'recommended' (default).
    """
    if slug_lower in explicit_tiers:
        return explicit_tiers[slug_lower]

    # Auto-heuristic: scan the link's own line and the nearest preceding heading.
    combined = link_line + " " + nearest_heading
    if ARCHAEOLOGY_MARKERS_RE.search(combined):
        return "archaeology"

    return "recommended"


# ---------------------------------------------------------------------------
# GitHub API helpers
# ---------------------------------------------------------------------------

def gh(method: str, path: str, params: dict | None = None, body: dict | None = None):
    url = f"https://api.github.com{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "listed-repos-check",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = json.dumps(body).encode() if body is not None else None
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        raw = resp.read()
    return json.loads(raw) if raw else {}


def collect_links(explicit_tiers: dict[str, str]) -> dict[str, dict]:
    """Return {owner/repo (lowercased): {sources, tier}}.

    Tier is determined per-occurrence; if the same slug appears in multiple
    contexts the most permissive classification wins
    (archaeology < historical < recommended).
    """
    TIER_ORDER = {"archaeology": 0, "historical": 1, "recommended": 2}

    found: dict[str, dict] = {}
    for path in ROOT.rglob("*.md"):
        rel_parts = path.relative_to(ROOT).parts
        if any(p.startswith(".") for p in rel_parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        for line_idx, line in enumerate(lines):
            for m in LINK_RE.finditer(line):
                owner = m.group("owner")
                repo = m.group("repo")
                if owner.lower() in RESERVED_OWNERS:
                    continue
                if repo.endswith(".git"):
                    repo = repo[:-4]
                slug = f"{owner}/{repo}".rstrip(".")
                slug_lower = slug.lower()

                nearest_heading = _nearest_preceding_heading(lines, line_idx)
                tier = classify_link(slug_lower, line, nearest_heading,
                                     explicit_tiers)

                src = str(path.relative_to(ROOT))
                if slug_lower not in found:
                    found[slug_lower] = {"sources": set(), "tier": tier}
                else:
                    # If seen in multiple contexts, use the less-permissive tier
                    # (i.e., if it's recommended anywhere, keep recommended).
                    existing_order = TIER_ORDER.get(found[slug_lower]["tier"], 2)
                    new_order = TIER_ORDER.get(tier, 2)
                    if new_order > existing_order:
                        found[slug_lower]["tier"] = tier
                found[slug_lower]["sources"].add(src)

    # Normalise sources to sorted list
    for v in found.values():
        v["sources"] = sorted(v["sources"])
    return found


def load_skiplist() -> set[str]:
    if not SKIP_FILE.exists():
        return set()
    out = set()
    for line in SKIP_FILE.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.add(line.lower())
    return out


def last_non_bot_commit(slug: str) -> tuple[str | None, str | None]:
    try:
        commits = gh("GET", f"/repos/{slug}/commits", params={"per_page": 30})
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"
    if not isinstance(commits, list):
        return None, "unexpected response"
    for c in commits:
        commit_obj = c.get("commit") or {}
        author_name = (commit_obj.get("author") or {}).get("name") or ""
        login = ((c.get("author") or {}) or {}).get("login") or ""
        if BOT_RE.search(author_name) or BOT_RE.search(login):
            continue
        return (commit_obj.get("author") or {}).get("date"), None
    return None, f"no non-bot commit in last {len(commits)}"


def latest_release_date(slug: str) -> str | None:
    """Return the published_at date of the latest release, or None if none."""
    try:
        release = gh("GET", f"/repos/{slug}/releases/latest")
        return release.get("published_at")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    except Exception:
        return None


def check_repo(slug: str) -> dict:
    try:
        meta = gh("GET", f"/repos/{slug}")
    except urllib.error.HTTPError as e:
        return {"slug": slug, "error": f"HTTP {e.code}"}
    except Exception as e:
        return {"slug": slug, "error": f"{type(e).__name__}: {e}"}
    last_human, err = last_non_bot_commit(slug)
    release_date = latest_release_date(slug)
    license_id = None
    lic = meta.get("license")
    if isinstance(lic, dict):
        license_id = lic.get("spdx_id") or lic.get("key")
    return {
        "slug": meta.get("full_name", slug),
        "archived": bool(meta.get("archived")),
        "stars": meta.get("stargazers_count", 0),
        "license": license_id,
        "last_push": meta.get("pushed_at"),
        "latest_release": release_date,
        "last_human_commit": last_human,
        "human_commit_error": err,
        "html_url": meta.get("html_url", f"https://github.com/{slug}"),
    }


def days_since(iso: str | None) -> int | None:
    if not iso:
        return None
    try:
        d = dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return None
    return (dt.datetime.now(dt.timezone.utc) - d).days


# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------

def _fmt_date(iso: str | None) -> str:
    """Return YYYY-MM-DD from an ISO timestamp, or '—'."""
    if not iso:
        return "—"
    return iso[:10]


def render_body(
    recommended: list[dict],
    historical: list[dict],
    archaeology: list[dict],
    flagged: list[tuple[dict, str]],
) -> str:
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    lines = [
        f"_Auto-generated {now} by `.github/workflows/weekly-trust.yml`._",
        "",
        f"Threshold: a recommended repo is flagged if it is archived OR has had no "
        f"non-bot commit in **{STALE_DAYS} days**.",
        "",
        "> **Tiers:** `recommended` repos are checked and can be flagged. "
        "`historical` repos are upstream/predecessor credits. "
        "`archaeology` repos are documented as abandoned — informational only.",
        "",
    ]

    # --- Flagged section ---
    if flagged:
        lines += [
            "## Flagged recommended repos",
            "",
            "| Repo | Reason | Last human commit | Listed in |",
            "| --- | --- | --- | --- |",
        ]
        for r, reason in flagged:
            human = _fmt_date(r.get("last_human_commit"))
            srcs = ", ".join(f"`{s}`" for s in sorted(r.get("sources", [])))
            lines.append(
                f"| [{r['slug']}]({r.get('html_url', '')}) "
                f"| {reason} | {human} | {srcs} |"
            )
        lines.append("")
    else:
        lines += ["## All recommended repos look healthy", ""]

    # --- Full recommended table (collapsed) ---
    lines += [
        "<details>",
        "<summary>Full recommended-repo table</summary>",
        "",
        "| Repo | Stars | License | Latest release | Last human commit | Days stale | Archived |",
        "| --- | ---: | --- | --- | --- | ---: | :---: |",
    ]
    for r in sorted(recommended, key=lambda x: x.get("slug", "").lower()):
        if r.get("error"):
            lines.append(f"| {r['slug']} | — | — | — | error: {r['error']} | | |")
            continue
        d = days_since(r.get("last_human_commit"))
        lines.append(
            f"| [{r['slug']}]({r.get('html_url', '')}) "
            f"| {r.get('stars', 0)} "
            f"| {r.get('license') or '—'} "
            f"| {_fmt_date(r.get('latest_release'))} "
            f"| {_fmt_date(r.get('last_human_commit'))} "
            f"| {d if d is not None else '—'} "
            f"| {'yes' if r.get('archived') else ''} |"
        )
    lines += ["", "</details>", ""]

    # --- Historical section (informational, always collapsed) ---
    if historical:
        lines += [
            "<details>",
            "<summary>Historical repos (upstream credits — not checked)</summary>",
            "",
            "These are upstream or predecessor repositories credited in the docs for "
            "provenance. They are not evaluated for health.",
            "",
            "| Repo | Listed in |",
            "| --- | --- |",
        ]
        for r in sorted(historical, key=lambda x: x.get("slug", "").lower()):
            srcs = ", ".join(f"`{s}`" for s in sorted(r.get("sources", [])))
            url = r.get("html_url") or f"https://github.com/{r['slug']}"
            lines.append(f"| [{r['slug']}]({url}) | {srcs} |")
        lines += ["", "</details>", ""]

    # --- Archaeology section (informational, always collapsed) ---
    if archaeology:
        lines += [
            "<details>",
            "<summary>Archaeology repos (documented as abandoned — not checked)</summary>",
            "",
            "These repos are explicitly documented in the guide as abandoned. "
            "They are recorded here for transparency but are never flagged.",
            "",
            "| Repo | Listed in | Auto-classified? |",
            "| --- | --- | --- |",
        ]
        for r in sorted(archaeology, key=lambda x: x.get("slug", "").lower()):
            srcs = ", ".join(f"`{s}`" for s in sorted(r.get("sources", [])))
            url = r.get("html_url") or f"https://github.com/{r['slug']}"
            auto = "yes (heuristic)" if r.get("auto_classified") else "no (tiers file)"
            lines.append(f"| [{r['slug']}]({url}) | {srcs} | {auto} |")
        lines += ["", "</details>", ""]

    lines += [
        "---",
        "To exclude a repo from this check, add `owner/repo` to "
        "`.github/listed-repos-skip.txt`. "
        "To assign a tier, edit `.github/listed-repos-tiers.txt`.",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def write_step_summary(body: str) -> None:
    """Append the report to the workflow's job summary so it shows on the run page."""
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    try:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write(body)
            f.write("\n")
    except OSError as e:
        print(f"could not write step summary: {e}", file=sys.stderr)


def upsert_report_issue(body: str) -> None:
    if DRY_RUN or not REPO or not TOKEN:
        print("--- DRY RUN: would post the following issue body ---")
        print(body)
        return
    try:
        issues = gh("GET", f"/repos/{REPO}/issues",
                    params={"state": "open", "per_page": 100})
    except urllib.error.HTTPError as e:
        if e.code in (404, 410):
            print(
                "issues API returned "
                f"{e.code}; issues likely disabled on this repo. "
                "Report is still in the job summary. To enable issues: "
                "Settings → Features → Issues, or "
                "`gh api -X PATCH repos/{owner}/{repo} -F has_issues=true`.",
                file=sys.stderr,
            )
            return
        raise
    existing = next(
        (
            i for i in issues
            if i.get("title", "").startswith(REPORT_TITLE_PREFIX)
            and not i.get("pull_request")
        ),
        None,
    )
    title = f"{REPORT_TITLE_PREFIX} — {dt.date.today()}"
    try:
        if existing:
            gh("PATCH", f"/repos/{REPO}/issues/{existing['number']}",
               body={"title": title, "body": body})
            print(f"Updated issue #{existing['number']}")
        else:
            gh("POST", f"/repos/{REPO}/issues",
               body={"title": title, "body": body, "labels": [REPORT_LABEL]})
            print("Created new health-report issue")
    except urllib.error.HTTPError as e:
        # Don't fail the whole run if posting fails — the summary is the fallback.
        print(f"could not upsert issue (HTTP {e.code}); see job summary instead",
              file=sys.stderr)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    explicit_tiers = load_tiers()
    skip = load_skiplist()
    links = collect_links(explicit_tiers)

    # Separate into tier buckets.
    recommended_slugs: list[tuple[str, dict]] = []
    historical_slugs: list[tuple[str, dict]] = []
    archaeology_slugs: list[tuple[str, dict]] = []

    for slug_lower, info in sorted(links.items()):
        if slug_lower in skip:
            continue
        tier = info["tier"]
        if tier == "historical":
            historical_slugs.append((slug_lower, info))
        elif tier == "archaeology":
            archaeology_slugs.append((slug_lower, info))
        else:
            recommended_slugs.append((slug_lower, info))

    # Detect auto-classified archaeology entries (not in tiers file).
    explicit_archaeology = {
        s.lower() for s, t in explicit_tiers.items() if t == "archaeology"
    }

    # Fetch API data for recommended repos only.
    recommended_results: list[dict] = []
    for slug_lower, info in recommended_slugs:
        r = check_repo(slug_lower)
        r["sources"] = info["sources"]
        recommended_results.append(r)

    # Build lightweight records for non-recommended tiers (no API calls needed).
    historical_results: list[dict] = []
    for slug_lower, info in historical_slugs:
        historical_results.append({
            "slug": slug_lower,
            "html_url": f"https://github.com/{slug_lower}",
            "sources": info["sources"],
        })

    archaeology_results: list[dict] = []
    for slug_lower, info in archaeology_slugs:
        archaeology_results.append({
            "slug": slug_lower,
            "html_url": f"https://github.com/{slug_lower}",
            "sources": info["sources"],
            "auto_classified": slug_lower not in explicit_archaeology,
        })

    # Flag logic (recommended only).
    flagged: list[tuple[dict, str]] = []
    for r in recommended_results:
        if r.get("error"):
            flagged.append((r, f"API error: {r['error']}"))
            continue
        if r.get("archived"):
            flagged.append((r, "archived"))
            continue
        d = days_since(r.get("last_human_commit"))
        if d is None:
            flagged.append((r, r.get("human_commit_error") or "no human commit found"))
        elif d > STALE_DAYS:
            flagged.append((r, f"no non-bot commit in {d} days"))

    # Emit a summary of tier counts for transparency.
    print(
        f"Tiers: {len(recommended_results)} recommended, "
        f"{len(historical_results)} historical, "
        f"{len(archaeology_results)} archaeology "
        f"({sum(1 for a in archaeology_results if a.get('auto_classified'))} auto-classified), "
        f"{len(skip)} skipped",
        file=sys.stderr,
    )
    if flagged:
        print(f"Flagged: {len(flagged)} repo(s)", file=sys.stderr)
        for r, reason in flagged:
            print(f"  - {r['slug']}: {reason}", file=sys.stderr)

    body = render_body(recommended_results, historical_results,
                       archaeology_results, flagged)
    write_step_summary(body)
    upsert_report_issue(body)
    return 0


if __name__ == "__main__":
    sys.exit(main())

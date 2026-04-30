#!/usr/bin/env python3
"""Audit GitHub repos linked from category READMEs and flag dead/archived ones.

Walks markdown files under the repo root, extracts every `github.com/owner/repo`
link, queries the GitHub API for each, and posts a single rolling "Listed-repo
health report" issue. Repos that haven't seen a non-bot commit within
STALE_DAYS, or that are archived, are flagged.

Designed to flag-not-fix: the maintainer reviews the issue and decides what
needs to be edited in the category READMEs.

Run locally with: GITHUB_TOKEN=$(gh auth token) GITHUB_REPOSITORY=owner/repo
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


def collect_links() -> dict[str, set[str]]:
    """Return {owner/repo (lowercased): set(source paths)}."""
    found: dict[str, set[str]] = defaultdict(set)
    for path in ROOT.rglob("*.md"):
        rel_parts = path.relative_to(ROOT).parts
        if any(p.startswith(".") for p in rel_parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for m in LINK_RE.finditer(text):
            owner = m.group("owner")
            repo = m.group("repo")
            if owner.lower() in RESERVED_OWNERS:
                continue
            if repo.endswith(".git"):
                repo = repo[:-4]
            slug = f"{owner}/{repo}".rstrip(".")
            found[slug.lower()].add(str(path.relative_to(ROOT)))
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


def check_repo(slug: str) -> dict:
    try:
        meta = gh("GET", f"/repos/{slug}")
    except urllib.error.HTTPError as e:
        return {"slug": slug, "error": f"HTTP {e.code}"}
    except Exception as e:
        return {"slug": slug, "error": f"{type(e).__name__}: {e}"}
    last_human, err = last_non_bot_commit(slug)
    return {
        "slug": meta.get("full_name", slug),
        "archived": bool(meta.get("archived")),
        "stars": meta.get("stargazers_count", 0),
        "last_push": meta.get("pushed_at"),
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


def render_body(results: list[dict], flagged: list[tuple[dict, str]]) -> str:
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    lines = [
        f"_Auto-generated {now} by `.github/workflows/check-listed-repos.yml`._",
        "",
        f"Threshold: a repo is flagged if it's archived OR has had no non-bot "
        f"commit in **{STALE_DAYS} days**.",
        "",
    ]
    if flagged:
        lines += [
            "## Flagged",
            "",
            "| Repo | Reason | Last human commit | Listed in |",
            "| --- | --- | --- | --- |",
        ]
        for r, reason in flagged:
            human = r.get("last_human_commit") or "—"
            srcs = ", ".join(f"`{s}`" for s in sorted(r.get("sources", [])))
            lines.append(
                f"| [{r['slug']}]({r.get('html_url', '')}) "
                f"| {reason} | {human} | {srcs} |"
            )
        lines.append("")
    else:
        lines += ["## All listed repos look healthy", ""]

    lines += [
        "## Full report",
        "",
        "| Repo | Stars | Last human commit | Days | Archived |",
        "| --- | ---: | --- | ---: | :---: |",
    ]
    for r in sorted(results, key=lambda x: x.get("slug", "").lower()):
        if r.get("error"):
            lines.append(f"| {r['slug']} | — | error: {r['error']} | | |")
            continue
        d = days_since(r.get("last_human_commit"))
        lines.append(
            f"| [{r['slug']}]({r.get('html_url', '')}) "
            f"| {r.get('stars', 0)} "
            f"| {r.get('last_human_commit') or '—'} "
            f"| {d if d is not None else '—'} "
            f"| {'yes' if r.get('archived') else ''} |"
        )
    lines += [
        "",
        "To exclude a repo from this check, add `owner/repo` to "
        "`.github/listed-repos-skip.txt`.",
    ]
    return "\n".join(lines)


def upsert_report_issue(body: str) -> None:
    if DRY_RUN or not REPO or not TOKEN:
        print("--- DRY RUN: would post the following issue body ---")
        print(body)
        return
    issues = gh("GET", f"/repos/{REPO}/issues", params={"state": "open", "per_page": 100})
    existing = next(
        (
            i for i in issues
            if i.get("title", "").startswith(REPORT_TITLE_PREFIX)
            and not i.get("pull_request")
        ),
        None,
    )
    title = f"{REPORT_TITLE_PREFIX} — {dt.date.today()}"
    if existing:
        gh("PATCH", f"/repos/{REPO}/issues/{existing['number']}",
           body={"title": title, "body": body})
        print(f"Updated issue #{existing['number']}")
    else:
        gh("POST", f"/repos/{REPO}/issues",
           body={"title": title, "body": body, "labels": [REPORT_LABEL]})
        print("Created new health-report issue")


def main() -> int:
    skip = load_skiplist()
    links = collect_links()
    results: list[dict] = []
    for slug_lower, sources in sorted(links.items()):
        if slug_lower in skip:
            continue
        r = check_repo(slug_lower)
        r["sources"] = sorted(sources)
        results.append(r)

    flagged: list[tuple[dict, str]] = []
    for r in results:
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

    body = render_body(results, flagged)
    upsert_report_issue(body)
    return 0


if __name__ == "__main__":
    sys.exit(main())

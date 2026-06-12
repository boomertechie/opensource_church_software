# Entry Template

Copy this structure when adding a tool to a category guide. The format matches existing entries — consistency is what keeps the guides scannable and the [health checks](scripts/check_listed_repos.py) meaningful.

Statuses: `✅ Active` (verified date), `✅ New` (first release within a year), `⚠️ Stale` (no meaningful commits in 1–3 years), `⚠️ Low activity`, `⛔ Not Recommended — Abandoned/Archived` (keep the entry with reasons and a successor; readers search for dead projects too).

```markdown
## Tool Name

**Status:** ✅ Active (verified YYYY-MM-DD)

**Skill Level:** Beginner / Intermediate / Advanced

**License:** MIT / GPL-3.0 / AGPL-3.0 / …

**Hosting model:** Self-hosted / Hosted / Both

**True Cost:**
- Software: Free
- Hosting: $X–Y/mo VPS (RAM needed)
- Setup Time: realistic estimate
- Ongoing Maintenance: hours/month, honestly

**What It Does:**
Two or three sentences. What problem it solves, for whom.

**Why Churches Use It:**
- Concrete capabilities, not adjectives
- Things a church would actually notice

**Installation:**
The shortest real path (Docker preferred). Link to upstream docs for the rest.

**Caveats:**
- What will frustrate a volunteer techie
- Where it falls short of the commercial equivalent
- Disclose any maintainer affiliation with this guide

**Links:**
- Website:
- GitHub:
- Docs:
```

Optional sections when they earn their space: **Best for / Avoid if** (when the fit is genuinely narrow), **Security notes** (anything handling children's data, payments, or credentials), **Comparison matrix row** (add the tool to the category's matrix if one exists).

Before submitting: test the install path on a clean machine, verify the project's activity yourself (don't trust its README), and state version/date for anything that will rot.

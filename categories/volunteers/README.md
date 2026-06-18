# Volunteer Scheduling & Management

> Coordinating volunteers for services, events, and ministry teams.

## Why It Matters

Most churches run on volunteers. Coordinating dozens (or hundreds) of volunteers across multiple ministries, services, and events quickly becomes unmanageable with spreadsheets. Good volunteer scheduling software:

- Prevents gaps in coverage (no more last-minute panic)
- Respects volunteer availability and preferences
- Enables easy substitutions and swaps
- Sends reminders and notifications
- Tracks serving history and preferences

## The Landscape

There are two main approaches:

1. **Dedicated Volunteer Schedulers** — Purpose-built for recurring ministry schedules
2. **General Scheduling Tools** — Adapted for church use (Doodle-style polling)

For a long time this category had no healthy dedicated option — the purpose-built projects below are abandoned or stale, leaving "adopt a full ChMS" or "use a spreadsheet" as the honest advice. As of mid-2026 the category has a maintained standalone entry: VoloRota.

---

## VoloRota

**Status:** ✅ New — first release June 2026, actively developed

**Skill Level:** Beginner (Docker)

**True Cost:**
- Software: Free (AGPL-3.0)
- Hosting: $5-7/mo VPS (1GB RAM is plenty — runs in ~18MB)
- Setup Time: ~10-30 minutes (timed walkthrough: clone to published schedule)
- Ongoing Maintenance: Minimal (single container, SQLite, no external services beyond an SMTP relay)

**What It Does:**
Standalone volunteer/serving scheduler — the Planning Center Services scheduling niche, self-hosted. Define teams and roles, generate recurring services from templates, and auto-fill a fair rotation. Volunteers accept, decline, or arrange their own replacement from emailed magic links — no volunteer accounts or passwords.

**Why Churches Use It:**
- Every volunteer action happens from an emailed link on a phone — this addresses the most common complaint about commercial schedulers, forced volunteer accounts
- Fair, explainable auto-fill: least-recently-served rotation honoring blockout dates, per-member role qualifications (your keys player is never scheduled on vocals), and no cross-team double-booking
- Both scheduling models real churches use: individual rotation (nursery, sound) AND whole-crew rotation ("Worship Crew B has the 2nd Sunday")
- Matrix view: services × role slots at a glance — the feature people miss most when leaving Planning Center
- Decline-with-replacement: a declining volunteer picks their own cover from eligible teammates; the leader gets notified
- ICS calendar feeds per volunteer, CSV export, printable schedules, per-service notes
- No telemetry and no third-party requests on any page, enforced by the project's own test suite

**Installation:**
```bash
docker run -d --name volorota \
  -p 3000:3000 -v volorota_data:/data \
  -e VOLOROTA_ADMIN_PASSWORD='pick-a-strong-password' \
  volorota   # build from source — see the repo README
```
Docker Compose and a full deployment guide (including a Caddy/TLS demo stack) are in the repo.

**Live Demo:** https://demo.volorota.org (resets hourly; admin password and volunteer links published at https://volorota.org)

**Caveats:**
- Young project (June 2026) — small community, no third-party plugin ecosystem yet
- Single admin account in v1 (volunteers don't need accounts; co-admins share a password)
- Email notifications only — no SMS (per-volunteer ICS feeds are the calendar bridge)
- Scheduling only, by design: no check-in, giving, or member database — pair it with your ChMS
- Disclosure: VoloRota is built and maintained by contributors to this guide

**Links:**
- Website + demo: https://volorota.org
- GitHub: https://github.com/VoloRota/volorota

---

## OpenVolunteerPlatform

**Status:** ⛔ Not Recommended — Abandoned

**Why we removed the recommendation:**
- Last meaningful commit was **July 2020**; only Renovate bot dependency PRs since
- Built as a one-off COVID-19 response project by Red Hat's now-defunct aerogear team
- Core dependencies are themselves abandoned (Graphback, Offix), so "updating" the project is effectively a rewrite
- Multiple unaddressed CVEs in transitive dependencies (express, mongodb, keycloak-connect, moment, etc.)

**If you're searching for this project:** Skip the fork-and-update path. The architecture (Graphback + Offix + MQTT + Keycloak) wasn't justified for most churches even when it was alive. For comparable functionality, see Volunteer Planner, ChurchApps, or your existing ChMS.

**Original links (for archaeology only):**
- GitHub: https://github.com/aerogear/OpenVolunteerPlatform

---

## Volunteer Planner (volunteer-planner.org)

**Status:** ⚠️ Stale (last commit: May 2023, mostly Dependabot)

**Skill Level:** Intermediate

**True Cost:**
- Software: Free
- Hosting: $5-15/mo VPS
- Setup Time: 2-4 hours
- Ongoing Maintenance: 1-2 hours/month

**What It Does:**
Django-based volunteer scheduling platform originally built for refugee aid coordination in Europe. Proven in production since 2015. Supports complex organizational hierarchies and shift-based scheduling.

**Why Churches Use It:**
- Battle-tested in high-volume environments (refugee aid)
- Simple, clean interface for volunteers
- Location-based hierarchy supports multi-site churches
- Multi-language support (Transifex integration)
- Self-contained — single Python application

**Installation:**
```bash
# Using Docker (recommended)
git clone https://github.com/coders4help/volunteer_planner.git
cd volunteer_planner
docker-compose up -d

# Or manual setup
git clone https://github.com/coders4help/volunteer_planner.git
cd volunteer_planner
virtualenv .venv
source .venv/bin/activate
pip install -r requirements/dev.txt
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

**Features for Churches:**
- Create organizations ("Children's Ministry", "Worship Team")
- Add facilities/rooms ("Nursery", "Main Sanctuary")
- Define shifts ("Sunday 9AM Service - Nursery")
- Volunteers self-register and claim shifts
- Automatic conflict detection
- Email notifications

**Caveats:**
- European-focused ( GDPR-compliant by default)
- UI is utilitarian, not polished
- Email configuration required for notifications
- No built-in check-in/check-out (scheduling only)

**Links:**
- GitHub: https://github.com/coders4help/volunteer_planner
- Demo: https://volunteer-planner.org
- Docs: https://github.com/coders4help/volunteer_planner/blob/develop/README_DOCKER.md

---

## Rallly

**Status:** ✅ Very Active (verified 2026-04-30, commits same day)

**Skill Level:** Beginner to Intermediate

**True Cost:**
- Software: Free
- Hosting: $5-10/mo VPS (or free tier on Railway/Render)
- Setup Time: 30 minutes
- Ongoing Maintenance: Minimal

**What It Does:**
Modern, Doodle-style scheduling tool for finding the best time for group meetings. While not built specifically for recurring volunteer schedules, it excels at event-based coordination and one-time scheduling needs.

**Why Churches Use It:**
- Beautiful, modern interface
- No account required for participants
- Works perfectly for: training sessions, one-time events, committee meetings
- Self-hostable with Docker
- Mobile-responsive
- Automatic timezone handling

**Installation (Docker):**
```yaml
version: "3"
services:
  rallly:
    image: rallly/rallly:latest
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://postgres:postgres@db:5432/rallly
      - SECRET_KEY=${RALLLY_SECRET}
    depends_on:
      - db
  db:
    image: postgres:14
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=rallly
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

**When to Use Rallly:**
- Scheduling training sessions
- Finding best time for volunteer meetings
- Coordinating one-time events
- Committee scheduling

**When NOT to Use Rallly:**
- Recurring weekly volunteer rotations (use Volorota or ChMS instead)
- Complex shift management with capacity limits
- Organizations with 100+ recurring positions

**Links:**
- Website: https://rallly.co
- GitHub: https://rallly.co/github
- Self-hosting docs: https://support.rallly.co/self-hosting

---

## ChurchApps (CHUMS/B1)

**Status:** ✅ Very Active (verified 2026-04-30, commits same day)

**Skill Level:** Beginner

**True Cost:**
- Software: Free (open source)
- Hosting: Cloud (free tier available) or self-hosted
- Setup Time: 15 minutes (cloud) or 2-4 hours (self-hosted)
- Ongoing Maintenance: Minimal (cloud) or 1-2 hours/month (self-hosted)

**What It Does:**
Full church management system with integrated volunteer scheduling, check-in, group management, and giving. The volunteer module includes scheduling, team management, and service planning.

**Why Churches Use It:**
- All-in-one solution (no integration needed)
- Native mobile apps for iOS/Android
- Check-in integration (volunteers and children)
- Service planning with volunteer assignments
- Free cloud tier for small churches
- Active development and community

**Deployment Options:**
- **Cloud:** https://b1.church/ (free for small churches)
- **Self-hosted:** Docker images available

**Volunteer Features:**
- Create volunteer teams/groups
- Schedule volunteers for services
- Self-check-in via mobile app
- Swapping/declining shifts
- Automated reminders
- Integration with service planning

**Caveats:**
- Full ChMS — may be overkill if you only need volunteer scheduling
- Self-hosted version requires multiple containers (API, web app, database)
- Cloud version has feature limitations on free tier

**Links:**
- GitHub: https://github.com/ChurchApps/B1Admin
- Website: https://b1.church/
- Docs: https://churchapps.org/dev

---

## Comparison Matrix

| Feature | VoloRota | Volunteer Planner | Rallly | ChurchApps |
|---------|----------|-------------------|--------|------------|
| **Project Health** | ✅ New, active (2026) | ⚠️ Stale (2023) | ✅ Very active | ✅ Very active |
| **Recurring Schedules** | ✅ (individual + crew rotation) | ✅ | ❌ | ✅ |
| **Self-Serve Swap** | ✅ (decline → pick replacement, no account) | ✅ | N/A | ✅ |
| **Volunteer Accounts Needed** | ❌ never (magic links) | ✅ | ❌ | ✅ |
| **Mobile Apps** | ✅ (mobile-first web) | ❌ | ✅ (web) | ✅ (native) |
| **Check-in Integration** | ❌ (by design) | ❌ | ❌ | ✅ |
| **Skill Level** | Beginner (Docker) | Intermediate | Beginner | Beginner |
| **Setup Time** | 10-30 min | 2-4 hrs | 30 min | 15 min (cloud) |
| **Maintenance** | Low | Medium | Low | Low/Medium |

---

## Recommendation by Church Size

### Church Plant (< 50 people)
**Use:** Google Sheets/Calendar, Rallly, or VoloRota
- Simple, free, no setup: shared Google Sheet with volunteer preferences
- For events: Rallly cloud (free) or self-hosted
- Already self-hosting a website? VoloRota adds real scheduling for one more container

### Small Church (50-200)
**Use:** VoloRota or ChurchApps Cloud
- VoloRota: self-hosted, volunteers need no accounts; pair it with your existing ChMS
- ChurchApps Cloud: all-in-one simplicity (scheduling + check-in + giving in one platform)
- Volunteer Planner remains an option if you need its multi-site shift model, but it is stale

### Mid-Size Church (200-1000)
**Use:** ChurchApps (self-hosted or cloud)
- Native mobile apps for volunteers
- Integrated with check-in and giving
- Service planning integration

### Large Church (1000+)
**Use:** ChurchApps (self-hosted) or a commercial ChMS with a volunteer module (Planning Center Services, Rock RMS)
- At this scale, integration with check-in, giving, and service planning matters more than scheduling alone
- Custom development is a real option, but start with a maintained platform — not an abandoned one
- Volunteer Planner can still work for single-purpose teams; pair it with your existing ChMS

---

## DIY QR Code Check-In for Volunteers

For churches wanting simple volunteer check-in without full scheduling:

### Simple PHP/MySQL Solution
```php
// Basic structure for volunteer check-in
// 1. Generate QR codes with volunteer IDs
// 2. Scan at check-in station
// 3. Log timestamp to database

// Requirements:
// - PHP 7.4+
// - MySQL/MariaDB
// - QR code library (endroid/qr-code)
// - Mobile device with camera for scanning (or cheap USB scanner)

// Estimated setup: 4-6 hours
// Hosting: $5/mo shared hosting
```

### Open-Source QR Libraries:
- **PHP:** `endroid/qr-code` (https://github.com/endroid/qr-code)
- **Python:** `qrcode` library + Flask/FastAPI
- **JavaScript:** `qrcodejs` (client-side generation)

---

## Integration Notes

### With ChurchCRM:
Use the Groups feature for volunteer teams, but it lacks scheduling. Export volunteer list to Volunteer Planner or use CalDAV integration for basic scheduling.

### With Nextcloud:
- Use **Calendar** for simple volunteer schedules
- Use **Polls** app for finding best times (Rallly alternative)
- Use **Forms** app for volunteer availability surveys

### With ChurchApps:
Native volunteer module included — no integration needed.

---

## Security Considerations

- **Volunteer data is personal data** — GDPR/CCPA compliance matters
- Use HTTPS for all volunteer-facing interfaces
- Implement rate limiting on login endpoints
- Regular backups of volunteer contact information
- Consider data retention policies (delete old records)


## If self-hosting is too much

- ChurchApps' hosted b1.church includes its volunteer module on the cloud free tier.
- A narrow paid scheduler beats a spreadsheet that one person understands — and beats a server nobody patches.
- Under ~50 people, the shared-sheet approach recommended above is genuinely fine.

---

*Last Updated: 2026-04-30 | Maintained by: church-tech-stack maintainers*

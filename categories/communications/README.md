# Email, Newsletters & Event Communications

> Keeping your congregation informed and engaged through newsletters, event announcements, and mass communications.

## Why It Matters

Churches need reliable ways to communicate with their members. Weekly announcements, event invitations, newsletter campaigns, and emergency notifications are essential for keeping the community connected. Good communication tools:

- Ensure important messages reach the right people
- Track engagement (who opened, who clicked)
- Segment audiences (send youth events only to families with teens)
- Maintain compliance with anti-spam laws (CAN-SPAM, GDPR)
- Save staff time with automation and templates
- Reduce dependence on expensive third-party services (MailChimp, Constant Contact)

## The Landscape

There are three main approaches:

1. **Newsletter Platforms** — Self-hosted alternatives to MailChimp for mass email campaigns
2. **Event Management** — Registration and ticketing for retreats, conferences, VBS
3. **Integrated ChMS** — Communication built into church management systems

This guide focuses on standalone tools. For integrated solutions, see ChurchCRM, Rock RMS, or ChurchApps.

---

## Listmonk

**Status:** ✅ Very Active (last commit: 2026)

**Skill Level:** Beginner to Intermediate

**True Cost:**
- Software: Free
- Hosting: $5-15/mo VPS (1GB RAM sufficient for most churches)
- Setup Time: 30-60 minutes
- Ongoing Maintenance: Minimal (< 1 hour/month)

**What It Does:**
High-performance, self-hosted newsletter and mailing list manager. The best open-source alternative to MailChimp for churches. Single binary application with a clean, modern interface. Handles segmentation, templates, analytics, and transactional emails.

**Why Churches Use It:**
- Escape MailChimp's pricing ($299/mo for 10,000 subscribers)
- Beautiful drag-and-drop template editor
- List segmentation (send youth events only to families)
- Real-time analytics (opens, clicks, bounces)
- Import existing subscriber lists (CSV)
- SMTP or API-based sending (Amazon SES, SendGrid, Postmark)
- Multi-language support (40+ languages)
- Privacy-focused (GDPR-compliant out of the box)

**Installation (Docker):**
```bash
# Create directory
mkdir listmonk && cd listmonk

# Download docker-compose.yml
wget -O docker-compose.yml https://raw.githubusercontent.com/knadh/listmonk/master/docker-compose.yml

# Generate config
docker-compose up -d db
docker-compose run --rm app ./listmonk --install

# Start
docker-compose up -d

# Access at http://localhost:9000
# Default credentials: listmonk / listmonk
```

**Architecture:**
- Backend: Go (single binary)
- Database: PostgreSQL
- Frontend: Vue.js
- Email: SMTP or transactional API (SES, SendGrid)

**Sending Options:**
1. **Self-hosted SMTP** (Postfix) — Free but requires reputation building
2. **Amazon SES** — $0.10 per 1,000 emails (best value)
3. **SendGrid** — 100 emails/day free, then $15/mo for 40,000
4. **Postmark** — $15/mo for 10,000 emails

**Features for Churches:**
- **Lists:** Create separate lists (Members, Volunteers, Youth)
- **Campaigns:** One-time newsletters or recurring announcements
- **Templates:** Visual editor with merge tags
- **Segments:** Send to "Families with children under 12"
- **Bounce Management:** Automatically remove invalid emails
- **Webhooks:** Integrate with other systems
- **API:** Programmatic access for automation

**Caveats:**
- Requires SMTP relay (can't send directly without email reputation)
- No A/B testing built-in (campaigns only)
- No built-in social media integration
- Template editor is good but not as polished as MailChimp

**Links:**
- GitHub: https://github.com/knadh/listmonk
- Demo: https://demo.listmonk.app (user: demo, pass: demo)
- Docs: https://listmonk.app/docs

---

## Mailtrain

**Status:** ⛔ Not Recommended — Abandoned (last human commit December 2022)

Listmonk above does everything most churches need from a newsletter platform and is an active, single-binary Go application — easier to deploy and maintain than Mailtrain ever was. If you specifically need Mailtrain's automation workflows or A/B testing, evaluate Rock RMS or a hosted service instead. Don't start a new Mailtrain deployment in 2026.

- Original repo (for reference): https://github.com/Mailtrain-org/mailtrain

---

## Pretix

**Status:** ✅ Very Active (verified 2026-04-30)

**Skill Level:** Intermediate

**True Cost:**
- Software: Free (AGPL-3.0)
- Hosting: $10-20/mo VPS (2GB RAM)
- Setup Time: 2-4 hours
- Ongoing Maintenance: 1-2 hours/month

**What It Does:**
Modern, well-maintained event ticketing platform built in Django. Used in production by conferences, festivals, and nonprofits across Europe. Free and paid tickets, multiple ticket categories, discount codes, check-in, attendee export, embeddable widgets — all the things churches need for retreats, VBS, and fundraising dinners.

**Why Churches Use It:**
- Free *or* paid event registration (retreats, conferences, VBS, fundraising dinners)
- QR-code tickets and a check-in app
- Custom branding per event
- Discount codes and tiered pricing
- Stripe / PayPal / SEPA payment processing
- Strong GDPR posture out of the box
- Embeddable widgets for the church website
- Active development — regular releases

**Installation:**
- **Docker:** Official image at `pretix/standalone` with documented Compose setup
- **Hosted:** pretix.eu offers managed hosting if you'd rather not self-host
- **Docs:** https://docs.pretix.eu/

**Caveats:**
- Heavier than a "just collect names" form — overkill for free RSVPs to a 30-person event
- Originally designed for ticketed conferences; church-specific terminology (volunteer slots, room assignments) doesn't map perfectly
- For purely free / non-ticketed events, a Listmonk signup form or Nextcloud Forms is simpler

**Lighter alternative:** [Alf.io](https://github.com/alfio-event/alf.io) (also active, also AGPL) is a smaller-footprint Java/Spring application focused on ticketed events. Worth a look if Pretix feels like too much.

**For free RSVPs only:** Skip event-ticketing software entirely. Listmonk + a Nextcloud Form, or a WordPress contact form, handles it.

**Links:**
- GitHub: https://github.com/pretix/pretix
- Website: https://pretix.eu/
- Docs: https://docs.pretix.eu/

---

## Attendize

**Status:** ⛔ Not Recommended — Abandoned (last human commit January 2023)

Use **Pretix** above instead. Attendize was a useful Laravel-based ticketing platform but has not seen meaningful development since early 2023 and runs on PHP 7.4/8.0 versions that are themselves end-of-life.

- Original repo (for reference): https://github.com/Attendize/Attendize

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
Modern, Doodle-style scheduling tool for finding the best time for group meetings and events. While not a newsletter tool, it excels at coordinating event attendance and scheduling.

**Why Churches Use It:**
- Beautiful, modern interface
- No account required for participants
- Perfect for: training sessions, committee meetings, small group coordination
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
- Scheduling volunteer training sessions
- Finding best time for small group meetings
- Coordinating one-time events
- Committee meeting scheduling

**When NOT to Use Rallly:**
- Mass newsletters (use Listmonk)
- Event ticketing (use Pretix)
- Recurring weekly schedules (use ChMS)

**Links:**
- Website: https://rallly.co
- GitHub: https://rallly.co/github
- Self-hosting docs: https://support.rallly.co/self-hosting

---

## Integrated ChMS Solutions

### ChurchCRM

**Status:** ✅ Active (v6.8.0, February 2026)

**Email Features:**
- MailChimp integration (sync member lists)
- Email templates for common communications
- Event management with automatic reminders
- Group-based communication
- 40+ language support

**When to Use:**
- You need a full ChMS anyway
- You want member data and email in one system
- You're comfortable with MailChimp for sending

**Links:**
- GitHub: https://github.com/ChurchCRM/CRM
- Website: https://churchcrm.io

### Rock RMS

**Status:** ✅ Very Active (45,000+ commits)

**Communication Features:**
- Built-in email editor and sending
- SMS messaging (Twilio integration)
- Push notifications (mobile app)
- Communication history tracking
- Workflow automation (drip campaigns)
- Advanced segmentation (DataViews)

**When to Use:**
- Large church with complex communication needs
- Want SMS + Email + Push in one platform
- Need automation workflows (new visitor sequences)
- Have Windows Server infrastructure

**Links:**
- GitHub: https://github.com/SparkDevNetwork/Rock
- Website: https://www.rockrms.com

### ChurchApps (B1 Church)

**Status:** ✅ Very Active (last commit: 2025)

**Communication Features:**
- In-app messaging
- Email integration
- Event announcements
- Group messaging
- Mobile notifications

**When to Use:**
- Modern, mobile-first approach
- Want free cloud hosting
- Need all-in-one solution
- Prefer Docker deployment for self-hosting

**Links:**
- GitHub: https://github.com/ChurchApps
- Website: https://b1.church

---

## Comparison Matrix

| Feature | Listmonk | Pretix | Rallly | ChurchCRM | Rock RMS |
|---------|----------|--------|--------|-----------|----------|
| **Project Health** | ✅ Very active | ✅ Very active | ✅ Very active | ✅ Active | ✅ Very active |
| **Newsletter Campaigns** | ✅ | ❌ | ❌ | ✅ (via MailChimp) | ✅ |
| **Event Registration** | ❌ | ✅ | ❌ | ✅ (basic) | ✅ |
| **Meeting Scheduling** | ❌ | ❌ | ✅ | ❌ | ❌ |
| **A/B Testing** | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Automation Workflows** | ❌ | ❌ | ❌ | ❌ | ✅ |
| **SMS Messaging** | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Setup Time** | 30 min | 2-4 hrs | 30 min | 4-6 hrs | 8+ hrs |
| **Skill Level** | Beginner | Intermediate | Beginner | Intermediate | Advanced |
| **Maintenance** | Low | Medium | Low | Medium | High |

---

## Recommendation by Church Size

### Church Plant (< 50 people)
**Use:** Listmonk (self-hosted) or MailChimp (free tier)
- Listmonk: $5/mo VPS + $0.10/1000 emails (SES)
- MailChimp: Free for up to 500 subscribers
- For events: Google Forms + Calendar

### Small Church (50-200)
**Use:** Listmonk + Rallly
- Listmonk for weekly newsletters
- Rallly for event scheduling
- Total cost: $10-15/mo (VPS + email sending)
- Add Pretix if you run paid events

### Mid-Size Church (200-1000)
**Use:** Listmonk or ChurchApps (integrated)
- Listmonk: More control, lower cost at scale
- ChurchApps: All-in-one convenience
- Consider Rock RMS if you need SMS + automation

### Large Church (1000+)
**Use:** Rock RMS or commercial platform
- Rock RMS: Full communication suite with workflows
- Commercial alternatives: Planning Center, Elvanto
- Listmonk still viable for newsletter-only needs

---

## Email Sending Considerations

### Why You Need an SMTP Relay

Self-hosted email servers (Postfix) get flagged as spam without proper configuration:
- SPF, DKIM, DMARC records required
- IP reputation takes months to build
- Many ISPs block residential/VPS IP ranges
- Deliverability rates suffer (50-70% inbox placement)

### Recommended SMTP Services for Churches

**Amazon SES** (Best Value)
- **Cost:** $0.10 per 1,000 emails
- **Setup:** Moderate (AWS account, domain verification)
- **Deliverability:** Excellent (99%+ inbox rate)
- **Limits:** 200 emails/day (free tier), then unlimited
- **Best for:** Churches with technical staff or consultant

**SendGrid** (Easiest)
- **Cost:** Free (100/day), $15/mo (40,000/mo)
- **Setup:** Easy (5 minutes)
- **Deliverability:** Excellent
- **Limits:** Clear tiers
- **Best for:** Small churches wanting simplicity

**Postmark** (Premium)
- **Cost:** $15/mo (10,000 emails)
- **Setup:** Easy
- **Deliverability:** Best-in-class (focus on transactional)
- **Limits:** Per-plan allocation
- **Best for:** Churches prioritizing deliverability

**Mailgun**
- **Cost:** Free (5,000/mo for 3 months), then $35/mo
- **Setup:** Moderate
- **Deliverability:** Good
- **Best for:** Developer-friendly churches

### Cost Comparison (10,000 emails/month)

| Service | Monthly Cost | Setup Difficulty | Deliverability |
|---------|--------------|------------------|----------------|
| Amazon SES | $1.00 | Moderate | Excellent |
| SendGrid | $15.00 | Easy | Excellent |
| Postmark | $15.00 | Easy | Best |
| Mailgun | $35.00 | Moderate | Good |
| Self-hosted (Postfix) | $0 + VPS | Very Hard | Poor |

---

## Integration Notes

### Listmonk + WordPress
- Use Listmonk API to sync subscribers
- Embed signup forms via HTML/JavaScript
- Trigger campaigns from WordPress events

### Listmonk + ChurchCRM
- Export member list from ChurchCRM (CSV)
- Import to Listmonk lists
- Update periodically or use API integration

### Pretix + Giving Platform
- Embed Pretix registration widget on church website
- Use webhooks to trigger follow-up emails
- Export attendee data for check-in systems

### Rallly for Multi-Site Scheduling
- Create separate polls per campus
- Share links via existing email lists
- Use results to inform event planning

---

## Privacy and Compliance

### GDPR Considerations
- **Consent:** Explicit opt-in for email lists (no pre-checked boxes)
- **Unsubscribe:** One-click unsubscribe in every email
- **Data Access:** Members can request their data
- **Data Deletion:** Honor removal requests within 30 days
- **Record Keeping:** Log consent timestamps

### CAN-SPAM (US) Requirements
- **Physical Address:** Include church address in footer
- **Unsubscribe:** Honor within 10 business days
- **Identification:** Clear sender identification
- **Subject Lines:** No deceptive subject lines

### Best Practices
- Segment lists (don't spam everyone with everything)
- Clean lists regularly (remove bounces and unsubscribes)
- Use double opt-in for new subscribers
- Include privacy policy link in signup forms
- Store subscriber data securely (HTTPS, encrypted backups)

---

## Security Considerations

- **HTTPS Required:** All email management interfaces must use HTTPS
- **Rate Limiting:** Prevent brute-force login attempts
- **API Keys:** Rotate SMTP credentials regularly
- **Backup Strategy:** Daily database backups with encryption
- **Access Control:** Limit who can send mass emails
- **Audit Logging:** Track who sends what to whom
- **Spam Prevention:** Implement CAPTCHA on public signup forms

---

*Last Updated: 2026-04-30 | Maintained by: church-tech-stack maintainers*

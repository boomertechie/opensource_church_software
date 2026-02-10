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

**Status:** ⚠️ Low Activity (last significant commit: 2023)

**Skill Level:** Intermediate

**True Cost:**
- Software: Free
- Hosting: $10-20/mo VPS (2GB RAM recommended)
- Setup Time: 2-4 hours
- Ongoing Maintenance: 2-3 hours/month

**What It Does:**
Self-hosted newsletter application built on Node.js. Inspired by MailChimp with similar features including automation, segmentation, and visual editors. More feature-rich than Listmonk but more complex to deploy.

**Why Churches Use It:**
- Full automation workflows (welcome series, drip campaigns)
- A/B testing for campaigns
- RSS-to-email (auto-send blog posts)
- Custom forms and landing pages
- Advanced segmentation logic
- Multi-user support with permissions

**Installation:**
```bash
# Prerequisites: Node.js 14+, MySQL/PostgreSQL, Redis
git clone https://github.com/Mailtrain-org/mailtrain.git
cd mailtrain
npm install
cp config/default.yaml config/production.yaml
# Edit production.yaml with your settings
NODE_ENV=production npm start
```

**Architecture:**
- Backend: Node.js/Express
- Database: MySQL or PostgreSQL
- Queue: Redis
- Frontend: React

**Caveats:**
- Project appears to be in maintenance mode (minimal updates since 2023)
- More complex setup than Listmonk
- Requires more resources (2GB RAM vs 1GB)
- Smaller community and documentation
- Installation process is less streamlined

**Links:**
- GitHub: https://github.com/Mailtrain-org/mailtrain
- Docs: https://github.com/Mailtrain-org/mailtrain/wiki

---

## Attendize

**Status:** ⚠️ Maintenance Mode (last commit: 2022)

**Skill Level:** Intermediate

**True Cost:**
- Software: Free
- Hosting: $10-20/mo VPS
- Setup Time: 2-4 hours
- Ongoing Maintenance: 1-2 hours/month

**What It Does:**
Open-source event ticketing and management platform built on Laravel. Think Eventbrite for churches. Handles event registration, ticket sales (free or paid), check-in, and attendee management.

**Why Churches Use It:**
- Free/paid event registration (retreats, conferences, VBS)
- QR code tickets for check-in
- Custom event pages with branding
- Discount codes and early bird pricing
- Attendee data export
- Payment processing (Stripe, PayPal)
- Email confirmations and reminders
- Embeddable widgets for church website

**Installation:**
```bash
# Docker (recommended)
git clone https://github.com/Attendize/Attendize.git
cd Attendize
cp .env.example .env
# Edit .env with database and email settings
docker-compose up -d
docker-compose exec app php artisan key:generate
docker-compose exec app php artisan migrate
```

**Use Cases:**
- **Vacation Bible School** — Registration with age groups and volunteer signups
- **Church Retreats** — Ticket sales with early bird pricing
- **Conferences** — Multiple sessions, workshops, speaker management
- **Fundraising Dinners** — Table reservations and donations
- **Community Events** — Free events with RSVP tracking

**Caveats:**
- Project is in maintenance mode (no major updates since 2022)
- PHP 7.4/8.0 required (Laravel framework)
- Stripe/PayPal setup required for paid events
- Email configuration critical for ticket delivery
- Limited mobile app functionality (web-based only)

**Links:**
- GitHub: https://github.com/Attendize/Attendize
- Demo: https://www.attendize.com/documentation.php

---

## Rallly

**Status:** ✅ Very Active (last commit: 2025)

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
- Event ticketing (use Attendize)
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

| Feature | Listmonk | Mailtrain | Attendize | Rallly | ChurchCRM | Rock RMS |
|---------|----------|-----------|-----------|--------|-----------|----------|
| **Newsletter Campaigns** | ✅ | ✅ | ❌ | ❌ | ✅ (via MailChimp) | ✅ |
| **Event Registration** | ❌ | ❌ | ✅ | ❌ | ✅ (basic) | ✅ |
| **Meeting Scheduling** | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **A/B Testing** | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| **Automation Workflows** | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| **SMS Messaging** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Setup Time** | 30 min | 2-4 hrs | 2-4 hrs | 30 min | 4-6 hrs | 8+ hrs |
| **Skill Level** | Beginner | Intermediate | Intermediate | Beginner | Intermediate | Advanced |
| **Maintenance** | Low | Medium | Medium | Low | Medium | High |
| **Active Development** | ✅ | ⚠️ | ⚠️ | ✅ | ✅ | ✅ |

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
- Add Attendize if you run paid events

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

### Attendize + Giving Platform
- Embed Attendize registration on church website
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

*Last Updated: 2026-02-10 | Maintained by: church-tech-stack maintainers*

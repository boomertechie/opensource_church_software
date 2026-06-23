# Free and Open Source Church Software

A comprehensive guide to self-hosted church technology, with detailed category guides, ready-to-deploy stacks, and practical implementation advice.

## What's Different About This Fork

This repository significantly extends the [original meichthys/opensource_church_software](https://github.com/meichthys/opensource_church_software) with:

- **Detailed Category Guides:** In-depth reviews of software by function (children's check-in, giving, volunteers, communications, sermon media)
- **Ready-to-Deploy Stacks:** Complete Docker Compose configurations for churches of different sizes and priorities
- **Real-World Focus:** "True Cost" analysis including setup time, skill requirements, and ongoing maintenance
- **Security Guidance:** Best practices for child safety systems, data privacy, and infrastructure security
- **Comparison Matrices:** Side-by-side feature comparisons to help you choose the right tools

The original repo provided a helpful flat list of tools. This fork adds structure, deployment guides, and implementation details for church leaders who want to self-host their technology.

---

## Disclaimers

This project is not intended to:

- Discourage or diminish the use of great [paid church software](https://churchm.ag/church-management-software/)
- Provide a comprehensive list of all open-source church software (see [christian_foss](https://github.com/meichthys/christian_foss) instead)
- Suggest that open source solutions are always the best choice for every church
- Serve as a complete installation and configuration guide for each tool

This project is intended to:

- Provide free and open source alternatives to paid software
- Help church plants and budget-conscious ministries deploy working technology stacks with minimal financial resources
- Share practical implementation patterns and proven configurations
- Enable churches to maintain full control and ownership of their data

Some of the suggested software will:

- Require technical expertise to install and maintain
- Not have feature parity with commercial options
- Be actively developed or in maintenance mode with varying levels of community support
- Need customization or integration work to fit church-specific workflows

---

## Repository Structure

### Categories

Detailed guides organized by church function:

- [**Children's Ministry**](categories/children/) - Check-in/check-out systems, child safety, parent communication
- [**Communications**](categories/communications/) - Email newsletters, event management, announcements
- [**Giving**](categories/giving/) - Donation platforms, giving management, financial tracking
- [**Sermon & Media**](categories/sermon-media/) - Sermon hosting, podcasting, video management
- [**Volunteers**](categories/volunteers/) - Scheduling, coordination, role management
- [**Vacation Bible School**](categories/vbs/) - Registration recipe (Pretix), check-in, the honest landscape

Each category guide includes:
- Software comparisons with skill level and cost analysis
- Security and compliance considerations
- Recommendations by church size
- Integration patterns

### Deployments

Complete, tested Docker Compose stacks ready for production:

- [**Starter Stack**](deployments/starter/) - Recommended for most churches (WordPress, ChurchCRM, Listmonk, Vaultwarden)
- [**Church Plant**](deployments/church-plant/) - Minimal viable setup for new churches (WordPress, ChurchCRM only)
- [**Small Church**](deployments/small-church/) - Adds file storage and monitoring (50-200 members)
- [**Privacy-First**](deployments/privacy-first/) - Complete self-hosted ecosystem (video calls, document editing, encrypted backups)

See [deployments/README.md](deployments/README.md) for detailed comparison and deployment guides.

---

## Quick Start: Find Your Stack

### I'm planting a church with zero budget
**Use:** [Church Plant Stack](deployments/church-plant/)
- Just website + member management
- 1GB RAM VPS ($5-6/month)
- One weekend to deploy

### We're an established small church (50-200 members)
**Use:** [Small Church Stack](deployments/small-church/)
- Adds file sharing, newsletters, monitoring
- 2-4GB RAM VPS ($10-20/month)
- Comprehensive but manageable

### We need total data control and privacy
**Use:** [Privacy-First Stack](deployments/privacy-first/)
- Self-hosted video calls, document editing, encrypted backups
- 4-8GB RAM VPS ($20-40/month)
- Zero data sharing with third parties

### I just want a simple, working setup
**Use:** [Starter Stack](deployments/starter/)
- Best balance for most churches
- Core tools without complexity
- 2GB RAM VPS ($10-12/month)

---

## Categories of Church Software

### Core Functions

Most churches need software for these common functions:

**Content & Communication:**
- Website Management (WordPress, Ghost, Hugo)
- Email Newsletters (Listmonk)
- Document Management (Nextcloud, Seafile)
- Digital Signatures (LibreSign)

**People & Ministry:**
- Church Management Systems (ChurchCRM, ChurchApps, Jethro PMM)
- Volunteer Scheduling (VoloRota — see [Volunteers guide](categories/volunteers/))
- Children's Check-In (see [Children's Ministry guide](categories/children/))

**Media & Worship:**
- Presentation Software (OpenLP, Quelea)
- Tablet Chord Charts (Worship Viewer)
- Live Streaming (OBS Studio)
- Sermon Hosting (see [Sermon & Media guide](categories/sermon-media/))

**Operations:**
- Financial Accounting (GnuCash, Akaunting)
- Giving Management (see [Giving guide](categories/giving/))
- Password Management (Vaultwarden/Bitwarden)

### Specialized Functions

Additional capabilities some churches need:

- Video Conferencing (Jitsi Meet, BigBlueButton)
- Online Document Editing (OnlyOffice, Collabora)
- Bible Study Apps (And Bible)
- Event Registration Systems (Pretix)
- Vacation Bible School Management

Are we missing a category? [Suggest one here](https://github.com/boomertechie/opensource_church_software/issues/new?title=Category%20Suggestion) or submit a pull request. (The upstream repository this fork extends has been inactive since mid-2025 — suggestions are maintained here.)

---

## Contributing

We welcome contributions from church technology practitioners, developers, and ministry leaders.

**How to Contribute:**

1. **Add New Software:** Use the standard entry template for consistency
2. **Update Existing Entries:** Keep deployment links, status, and feature lists current
3. **Share Real-World Experience:** Add "Why Churches Use It" and "Caveats" sections
4. **Submit Deployment Configs:** Docker Compose stacks with .env templates
5. **Improve Documentation:** Installation guides, security checklists, troubleshooting tips

See [template.md](template.md) for the standard entry format.

Before submitting:
- Test any deployment configurations on a clean server
- Include skill level and time estimates
- Note any security or compliance considerations
- Credit original authors and link to upstream documentation

---

## Quick Reference: Software List

A condensed list of free and open source tools by category. See category guides for detailed comparisons.

### Website Management
- [WordPress](https://wordpress.org/) - Most popular CMS, extensive plugin ecosystem
- [Ghost](https://ghost.org/) - Modern publishing platform
- [Hugo](https://gohugo.io/) - Static site generator

### Document Management
- [Nextcloud](https://nextcloud.com/) - Files, calendars, contacts, collaboration
- [Seafile](https://www.seafile.com/) - High-performance file sync and share

### Digital Signatures
- [LibreSign](https://libresign.coop) - Self-hosted electronic signatures

### Financial Accounting
- [GnuCash](https://gnucash.org/) - Desktop accounting software
- [Akaunting](https://akaunting.com/) - Web-based accounting and invoicing

### Presentation
- [OpenLP](https://openlp.org/) - Worship presentation software
- [Quelea](https://quelea.org/) - Projection software for worship
- [Worship Viewer](https://github.com/boomertechie/worship-viewer) - Self-hosted tablet chord chart viewer for worship teams (Docker, iPad-optimized)

### Live Streaming
- [OBS Studio](https://obsproject.com/) - Video recording and live streaming

### Church Management Systems
- [ChurchCRM](https://churchcrm.io/) - Member management, giving tracking, check-in
- [ChurchApps](https://churchapps.org/) - Suite of church apps (ChMS, check-in, giving)
- [Jethro PMM](https://github.com/tbar0970/jethro-pmm) - Pastoral Ministry Manager

### Email & Communications
- [Listmonk](https://listmonk.app/) - High-performance newsletter platform

### Event Registration & Ticketing
- [Pretix](https://pretix.eu/) - Modern event ticketing (free + paid events; QR check-in)
- [Alf.io](https://github.com/alfio-event/alf.io) - Lighter-weight ticketing alternative

### Volunteer Management
- [VoloRota](https://github.com/VoloRota/volorota) - Self-hosted volunteer scheduling; magic-link volunteer flow, no accounts needed (live demo: [volorota.org](https://volorota.org))
- See [Volunteers Guide](categories/volunteers/) for detailed comparisons and DIY approaches

### Children's Check-In
- See [Children's Ministry Guide](categories/children/) for security-focused solutions

### Giving & Donations
- See [Giving Guide](categories/giving/) for donation platforms and integrations

### Bible Apps
- [And Bible](https://andbible.github.io/) - Open source Bible study app for Android

### Video Conferencing
- [Jitsi Meet](https://jitsi.org/) - Encrypted video calls
- [BigBlueButton](https://bigbluebutton.org/) - Web conferencing for online learning

### Online Document Editing
- [OnlyOffice](https://www.onlyoffice.com/) - Office suite with collaboration
- [Collabora Online](https://www.collaboraoffice.com/) - LibreOffice in the browser

### Vacation Bible School
- See the [VBS guide](categories/vbs/) — there is no healthy dedicated tool, and you don't need one: Pretix handles VBS registration well (full recipe in the guide)

### Password Management
- [Vaultwarden](https://github.com/dani-garcia/vaultwarden) - Bitwarden server implementation

### Monitoring & Operations
- [Uptime Kuma](https://github.com/louislam/uptime-kuma) - Service monitoring dashboard
- [Diun](https://github.com/crazy-max/diun) - **Recommended.** Notifies you when container images have updates available; you decide when to apply them
- [Duplicati](https://www.duplicati.com/) - Encrypted backup solution

> Note: `containrrr/watchtower`, previously listed here for automated container updates, was archived in late 2025. If you specifically want hands-off auto-updates the maintained successor is [`nicholas-fedor/watchtower`](https://github.com/nicholas-fedor/watchtower) (drop-in replacement, image at `ghcr.io/nicholas-fedor/watchtower`). For most churches, Diun + a manual `docker compose pull && docker compose up -d` during a maintenance window is the safer choice.

---

## Credits

**Original Repository:** [meichthys/opensource_church_software](https://github.com/meichthys/opensource_church_software)

**This Fork:** Maintained by contributors focused on practical deployment guidance for self-hosted church technology.

## License

See [LICENSE](LICENSE) for details.

---

*Last Updated: 2026-02-10*

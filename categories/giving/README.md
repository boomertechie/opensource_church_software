# Giving & Donation Management

*Track tithes, offerings, and donations with integrated online giving platforms*

> Church-specific giving platforms that handle member contributions, online payments, tax receipts, and financial reporting without relying on proprietary cloud services.

## Why It Matters

- **Financial transparency** builds trust with your congregation through clear, auditable donation records
- **Tax compliance** requires accurate year-end giving statements for member deductions
- **Online convenience** meets modern expectations - members expect digital payment options
- **Data ownership** keeps sensitive financial information under your direct control
- **Cost savings** can redirect thousands of dollars annually from payment processors to ministry
- **Integration needs** demand systems that work with your existing member database and accounting tools

---

## ChurchCRM

**Status:** Production Ready
**Skill Level:** Intermediate
**True Cost:** $0 software + $6-20/mo hosting + 2.9% + $0.30 per transaction (Stripe/PayPal fees)

### What It Does

Full-featured church management system with integrated donation tracking, online giving via Stripe and PayPal, automated tax receipts, family pledge tracking, and member portal for viewing giving history.

### Why Churches Use It

Most mature open source church platform with 10+ years development, active community of 813+ GitHub stars, comprehensive feature set beyond just donations (attendance, events, groups), and proven Docker deployment for production environments. Successfully deployed by hundreds of churches worldwide.

### Installation

Docker Compose recommended for production. Requires Apache, PHP 7.4+, MariaDB/MySQL. Full Docker stack includes Alpine Linux base, automatic backups, and SSL certificate support. Estimated setup time: 2-4 hours for technical administrators.

### Caveats

Requires technical knowledge for initial configuration and ongoing maintenance. Payment gateway setup demands SSL certificates and PCI compliance awareness. UI feels dated compared to commercial alternatives. Limited mobile-first design - desktop web interface works but not optimized for smartphone use.

### Links

- GitHub: https://github.com/ChurchCRM/CRM
- Website: https://churchcrm.io
- Documentation: https://github.com/ChurchCRM/CRM/wiki
- Docker: https://hub.docker.com/r/churchcrm/crm

---

## Chums (B1.Church Admin)

**Status:** Production Ready
**Skill Level:** Beginner
**True Cost:** $0 software + $6/mo VPS hosting + payment processor fees (2.9% + $0.30)

### What It Does

Modern TypeScript/Laravel church management platform with donation tracking, online giving integration, mobile apps (iOS/Android), member management, and attendance tracking. Rebuilt from ground up in 2025 with focus on ease of deployment.

### Why Churches Use It

Fastest deployment path - advertised as "10-minute Docker Compose setup" with sensible defaults. Clean, modern UI that works well on mobile devices. Free mobile app included for member engagement. Active development with monthly updates through 2025-2026.

### Installation

Single Docker Compose command gets full stack running. Requires basic Docker knowledge and VPS access. Automated SSL with Let's Encrypt. Configuration via web interface eliminates need for manual file editing. Stripe/PayPal integration through admin dashboard.

### Caveats

Smaller community than ChurchCRM (newer project). Less third-party documentation available. Some advanced features still in development. Freemium model means hosted cloud option exists - verify you're using self-hosted version to maintain data ownership.

### Links

- GitHub: https://github.com/ChurchApps/B1Admin
- Website: https://b1.church
- Documentation: https://churchapps.org/dev
- Mobile Apps: iOS App Store / Google Play (search "B1.Church")

---

## ACTS Church Management

**Status:** Stable
**Skill Level:** Intermediate
**True Cost:** $0 software + hosting costs + offline donation tracking only

### What It Does

Integrated system combining member management, attendance tracking, donation recording, and basic accounting ledger. Designed for churches that want single unified database for all administrative functions.

### Why Churches Use It

10+ years of active development demonstrates long-term viability. Tightly integrated accounting module eliminates need for separate QuickBooks/Xero subscriptions. Strong focus on data integrity and audit trails. Free/Open licensing with dedicated Facebook community for support.

### Installation

Windows-based installation with SQL Server Express backend. Requires Windows Server or desktop OS. Not containerized - traditional installed application model. Steeper learning curve but comprehensive feature documentation.

### Caveats

No built-in online giving - donations must be entered manually after collection. Windows-only deployment limits hosting flexibility compared to Docker solutions. Older technology stack (not web-based). No mobile app for member access. Best suited for churches comfortable with manual data entry workflows.

### Links

- Website: Contact via community channels for download
- Support: Facebook group (active community)
- Documentation: PDF manuals included with installation

---

## OpenPetra

**Status:** Production Ready
**Skill Level:** Advanced
**True Cost:** $0 software + $20-50/mo hosting + optional commercial hosting available

### What It Does

Comprehensive nonprofit donor management system originally designed for mission organizations. Handles recurring donations, complex fund accounting, multi-currency support, sponsor management, and detailed financial reporting.

### Why Churches Use It

Enterprise-grade feature set rivals commercial platforms like Blackbaud. Multi-tenant architecture supports denominations managing multiple congregations. Strong international support with 20+ language translations. GPLv3 license with commercial hosting option for churches wanting managed service.

### Installation

C# stack requires Windows Server with IIS or Linux with Mono runtime. PostgreSQL database backend. Docker support exists but community-maintained (not official). Complex initial configuration - recommended for churches with dedicated IT staff or budget for commercial hosting.

### Caveats

Steep learning curve due to enterprise complexity. Overkill for small churches under 200 members. Limited online payment integration compared to church-specific platforms. Better suited for denominational offices or large churches with complex fund accounting needs.

### Links

- GitHub: https://github.com/openpetra/openpetra
- Website: https://www.openpetra.org
- Commercial Hosting: https://www.openpetra.com
- Documentation: https://wiki.openpetra.org

---

## Akaunting

**Status:** Production Ready
**Skill Level:** Intermediate
**True Cost:** $0 software + $10-25/mo hosting + payment processor fees

### What It Does

Modern web-based accounting platform built on Laravel/VueJS. Customizable for donation workflows through customer/invoice system adaptation. Supports recurring transactions, multi-currency, online payments (Stripe/PayPal/Square), and financial reporting.

### Installation

Docker Compose for quick deployment. Requires PHP 8.0+, MySQL/PostgreSQL. Active marketplace for extensions and customization. Web-based admin interface for configuration.

### Caveats

Not church-specific - requires adaptation of accounting concepts to church workflows. "Customers" become "members", "invoices" become "donation receipts". No attendance tracking, event management, or church-specific features. Best used alongside dedicated church management system or for churches wanting accounting-first approach.

### Links

- GitHub: https://github.com/akaunting/akaunting
- Website: https://akaunting.com
- Documentation: https://akaunting.com/docs
- Docker: https://hub.docker.com/r/akaunting/akaunting

---

## Houdini Project

**Status:** Active Development
**Skill Level:** Advanced
**True Cost:** $0 software + $30-60/mo hosting + payment processor fees

### What It Does

Nonprofit fundraising platform supporting crowdfunding campaigns, recurring donors, event ticketing, peer-to-peer fundraising, and supporter management. Ruby on Rails stack with modern web interface.

### Why Churches Use It

Flexible architecture allows customization for church-specific workflows. Strong recurring donation support with Stripe integration. Event management features work well for church fundraising dinners, mission trips, capital campaigns. AGPL/LGPL dual licensing.

### Installation

Ruby on Rails requires technical expertise. PostgreSQL database. Redis for background jobs. Stripe Connect required for payment processing. Docker development environment available but production deployment requires Rails knowledge.

### Caveats

Not designed for churches - nonprofit fundraising focus means missing church-specific features (attendance, sermon management, small groups). Complex technical stack demands experienced developers for customization. Active but small development community. Better suited for church capital campaigns than weekly giving.

### Links

- GitHub: https://github.com/houdiniproject/houdini
- Website: https://houdiniproject.org
- Documentation: https://github.com/houdiniproject/houdini/wiki
- License: AGPL v3 (core), LGPL v3 (components)

---

## Comparison Matrix

| Feature | ChurchCRM | Chums | ACTS | OpenPetra | Akaunting | Houdini |
|---------|-----------|-------|------|-----------|-----------|---------|
| Online Giving Integration | Stripe, PayPal | Stripe, PayPal | No | Limited | Stripe, PayPal, Square | Stripe |
| Donation Tracking | Core Feature | Core Feature | Core Feature | Core Feature | Adapted | Core Feature |
| Recurring Donations | Yes | Yes | Manual | Yes | Yes | Yes |
| Tax Receipts | Automated | Automated | Manual | Automated | Custom | Custom |
| Member Management | Full CRM | Full CRM | Full | Donor CRM | Customer DB | Supporter DB |
| Attendance Tracking | Yes | Yes | Yes | No | No | No |
| Mobile App | Web Only | iOS/Android | No | Web Only | Web Only | Web Only |
| Ease of Setup (1-5, 5=easiest) | 3 | 5 | 2 | 1 | 4 | 1 |
| Docker Production Support | Official | Official | No | Community | Official | Dev Only |
| Last Major Update | Feb 2026 | Nov 2025 | Active 2025 | Active 2025 | Jan 2026 | Active 2025 |
| Church-Specific Design | Yes | Yes | Yes | No | No | No |

---

## Recommendations by Church Size

### Small Churches (Under 100 Members)

**Best Choice:** Chums (B1.Church Admin)

Easiest deployment, modern interface, mobile apps included, and free tier for self-hosting. Online giving built-in from day one. Small churches typically lack dedicated IT staff - Chums' 10-minute setup and web-based configuration eliminates technical barriers.

**Runner-Up:** ChurchCRM if you need more established ecosystem and community support.

### Medium Churches (100-500 Members)

**Best Choice:** ChurchCRM

Mature platform with proven track record at this scale. Comprehensive feature set grows with your church. Active community provides peer support. Docker deployment enables reliable hosting. Balance of features vs. complexity hits sweet spot for mid-size congregations.

**Runner-Up:** Chums if mobile engagement and modern UI are priorities over feature depth.

### Large Churches (500+ Members)

**Best Choice:** OpenPetra (with commercial hosting) or ChurchCRM

Large churches need enterprise reliability and complex fund accounting (building funds, mission funds, designated giving). OpenPetra's multi-tenant architecture and advanced reporting justify the steeper learning curve. Commercial hosting option provides professional support when stakes are high.

**Alternative:** ChurchCRM with dedicated IT staff for customization and integration with existing systems.

### Multi-Site or Denominational Offices

**Best Choice:** OpenPetra

Multi-tenant design built for this use case. Centralized donor management across multiple locations. Complex fund accounting matches denominational reporting requirements.

---

## Integration Notes

### Accounting Software Integration

Most giving platforms generate reports compatible with QuickBooks, Xero, or other accounting packages via CSV export. ChurchCRM and ACTS have tighter integration due to built-in ledger modules.

**Best Practice:** Use church platform for donation tracking and member-facing receipts, export monthly summaries to professional accounting software for bookkeeping and budgeting.

### Payment Processor Requirements

All online giving solutions require:
- SSL certificate (Let's Encrypt free option available)
- Business verification with Stripe/PayPal (church EIN/tax documents)
- PCI compliance awareness (processors handle card data, but configuration matters)
- Bank account for deposits

**Cost Reality:** Payment processor fees (2.9% + $0.30 per transaction) are unavoidable. Self-hosting saves monthly SaaS fees but not transaction fees.

### Member Portal Considerations

ChurchCRM and Chums provide member-facing portals where congregants can view giving history, print tax receipts, and update contact information. This reduces administrative burden but requires:
- Member authentication system
- Privacy policy for data handling
- Training materials for congregation

Churches without member portals must manually generate year-end statements and respond to giving history requests.

---

**Last Updated:** 2026-02-10
**Maintainer:** Open Source Church Software Project
**License:** This guide is CC BY-SA 4.0

## If self-hosting is too much

- ChurchApps' hosted b1.church runs the same open-source giving module without you operating the server — payment-adjacent systems punish neglect hardest.
- A narrow paid giving platform with clean export beats an unmaintained self-hosted one.
- For very small congregations, recorded checks and a spreadsheet remain compliant and sane.

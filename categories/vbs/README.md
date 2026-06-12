# Vacation Bible School Registration

> Registering kids, collecting the information that keeps them safe, and checking them in every morning — without paper stacks or a new piece of software.

## Why It Matters

VBS is most churches' biggest annual children's event: dozens to hundreds of registrations, arriving in a two-month window, each carrying allergy and pickup information that workers need at the door. It's also *seasonal* — whatever system you use runs hard for six weeks and idles for forty-six. That usage pattern changes the right answer.

## The honest landscape

There is no healthy, dedicated open-source VBS system, and this guide doesn't expect one to appear: the niche is seasonal, the registration mechanics aren't VBS-specific, and the major curriculum publishers bundle free hosted registration portals with the curriculum you're already buying. If your publisher's portal meets your needs, using it is a fine answer — see the end of this page.

If you want data ownership, no third-party portal, or registration that matches how your church already works, the good news is that **you don't need VBS software**. VBS registration is an event-registration problem, and [Pretix](https://pretix.eu/) — already recommended in the [Communications guide](../communications/) — handles it well. The rest of this page is the recipe.

## The Pretix recipe

**What you need:** a running Pretix instance (see the [Communications guide](../communications/) for self-hosting, or use pretix.eu's official hosting), and a phone or tablet for the check-in table.

### 1. Model the week as an event

Create one event: "VBS 2027 — June 14–18." Registration opens when you say so, closes when you say so, and the event page is the link you put in the bulletin and on Facebook.

### 2. Model age groups as products with quotas

Create one (free) ticket product per class or age group: "Preschool (ages 3–5)", "Elementary (grades 1–3)", "Preteens (grades 4–6)". Give each product a **quota** matching that classroom's real capacity — when the preschool room is full, preschool registration closes by itself while the other groups stay open. Enable Pretix's **waiting list** per product so latecomers queue automatically instead of calling the office.

### 3. Collect the safety information as questions

Pretix attaches **questions** to products. Mark these required:

- Parent/guardian name and phone (the number a worker calls at 10am)
- Allergies and medical notes
- People authorized to pick this child up
- Anything your insurance or denomination requires

Optional but popular: T-shirt size, grade in fall, home church. Answers export to a spreadsheet for class rosters and appear on each ticket at check-in.

### 4. Families register all their kids in one order

A parent adds one ticket per child — different products for different ages — in a single order, answering the questions once per child. One confirmation email, every child's ticket in it.

### 5. Check-in each morning with pretixSCAN

Install **pretixSCAN** (Android/iOS, works offline) on the check-in device. Create one **check-in list per day** — Monday through Friday — and scanning a child's ticket marks daily attendance; the question answers (allergies, pickup) display to the worker at the door. At week's end, the per-day lists are your attendance record.

### What this recipe doesn't do

- **Class rosters beyond the product split** — export the order data and sort in a spreadsheet; that's the realistic workflow anyway.
- **Volunteer staffing** — scheduling your VBS workers is a [volunteer-scheduling problem](../volunteers/); the tools there handle "who's in the preschool room Thursday."
- **Secure pickup codes at scale** — if your church requires check-in/out pairing with guardian verification, use a real [children's check-in system](../children/) alongside registration.

## Existing dedicated software

### Vacation Bible School System

**Status:** ⚠️ Low activity (no non-bot commits since May 2025)

A PHP/JavaScript registration platform by a single author. It exists and may run, but it has no community, no Docker packaging, and no commits in over a year — evaluate carefully before depending on it for an event involving children's data.

- GitHub: https://github.com/prabhu-qea/Vacation-Bible-School-System

## If self-hosting is too much

- Your curriculum publisher's bundled registration portal is the path of least resistance — already paid for, hosted, and familiar to other churches running the same program.
- pretix.eu's official hosting runs this exact recipe with no server.
- Under a few dozen kids, a paper form and a phone call is still a system that works.

---

*Last Updated: 2026-06-12 | Maintained by: church-tech-stack maintainers*

# Docker Compose Deployments

Ready-to-deploy Docker Compose stacks for self-hosting church software.

---

## Before You Deploy — Six Questions

Answer these before choosing a stack or running a single command.

1. **Who will patch this stack monthly?**
2. **Who gets alerted when something breaks at 2 AM?**
3. **Where are backups stored, and are they off this server?**
4. **Has anyone actually tested restoring from those backups?**
5. **What paid product does this replace, and what does it cost?**
6. **Is the money saved worth the time this will take to maintain?**

If no one owns those answers, use hosted tools. Self-hosting is not automatically more faithful, cheaper, or safer.

---

## Choose Your Stack

| Stack | Best For | RAM | What's Included |
|-------|----------|-----|-----------------|
| **[Starter](starter/)** | Most churches | 2GB | WordPress, ChurchCRM, Listmonk, Vaultwarden |
| [Church Plant](church-plant/) | Minimal setup | 1-2GB | WordPress, ChurchCRM only |
| [Small Church](small-church/) | Need file sharing | 2-4GB | + Nextcloud, Monitoring |
| [Privacy-First](privacy-first/) | Full self-hosted | 4-8GB | + Jitsi, OnlyOffice, Backups |

**Start with [Starter](starter/)** unless you have a specific reason for the others.

## Quick Start

```bash
cd deployments/starter
cp .env.example .env
# Edit .env — fill in all fields, leave nothing blank
nano .env
docker compose up -d
```

## What You Need

- A VPS with 2GB+ RAM ($10-12/month from DigitalOcean, Linode, or Vultr)
- A domain name pointed to your server
- Basic command line familiarity (copy/paste is fine)

## Stack Comparison

| Feature | Starter | Church Plant | Small Church | Privacy-First |
|---------|---------|--------------|--------------|---------------|
| Website (WordPress) | ✅ | ✅ | ✅ | ✅ |
| Member Management (ChurchCRM) | ✅ | ✅ | ✅ | ✅ |
| Email Newsletters (Listmonk) | ✅ | ❌ | ✅ | ✅ |
| Password Sharing (Vaultwarden) | ✅ | ❌ | ❌ | ✅ |
| File Storage (Nextcloud) | ❌ | ❌ | ✅ | ✅ |
| Video Calls (Jitsi) | ❌ | ❌ | ❌ | ✅ |
| Document Editing (OnlyOffice) | ❌ | ❌ | ❌ | ✅ |
| Monitoring (Uptime Kuma) | ❌ | ❌ | ✅ | ✅ |
| Encrypted Backups (Duplicati) | ❌ | ❌ | ❌ | ✅ |

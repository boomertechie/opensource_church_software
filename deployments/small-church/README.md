# Small Church Stack

> Balanced setup for established churches with 50-200 members.

---

## Before You Deploy — Six Questions

Answer these before running a single command. If no one owns the answers, use a hosted service instead (see the category guides' "If self-hosting is too much" sections).

1. **Who will patch this stack monthly?**
2. **Who gets alerted when something breaks at 2 AM?**
3. **Where are backups stored, and are they off this server?**
4. **Has anyone actually tested restoring from those backups?**
5. **What paid product does this replace, and what does it cost?**
6. **Is the money saved worth the time this will take to maintain?**

If no one owns those answers, use hosted tools. Self-hosting is not automatically more faithful, cheaper, or safer.

---

## What's Included

| Function | Tool | Purpose |
|----------|------|---------|
| **Website** | WordPress | Sermons, events, announcements |
| **ChMS** | ChurchCRM | Members, groups, check-in, giving tracking |
| **Files** | Nextcloud | Document storage, collaboration, calendars |
| **Email** | Listmonk | Newsletters, announcements, automated emails |
| **Monitoring** | Uptime Kuma | Service health monitoring |
| **Updates** | Diun | Notifies you of available container image updates (manual apply) |

## Update Policy

This stack pins images to stable version tags. Diun (already included) emails you when a new image tag is available. When you receive a notification, schedule a maintenance window, take a backup, then run `docker compose pull && docker compose up -d`. Never update on Saturday night or Sunday morning.

## System Requirements

- **Server:** VPS with 2GB RAM (4GB recommended), 50GB storage
- **OS:** Ubuntu 22.04 LTS or Debian 12
- **Domain:** One domain with wildcard or multiple subdomains
- **Skills:** Basic Linux, Docker familiarity, DNS management

## Quick Start

### 1. Prepare Your Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker

# Create directory
mkdir -p ~/small-church && cd ~/small-church
```

### 2. Configure DNS

Point these subdomains to your server IP:

```
www.yourchurch.com     → A Record → your-server-ip
crm.yourchurch.com     → A Record → your-server-ip
files.yourchurch.com   → A Record → your-server-ip
news.yourchurch.com    → A Record → your-server-ip
status.yourchurch.com  → A Record → your-server-ip
```

### 3. Download and Configure

```bash
# Download files
curl -o docker-compose.yml https://raw.githubusercontent.com/boomertechie/opensource_church_software/main/deployments/small-church/docker-compose.yml
curl -o .env.example https://raw.githubusercontent.com/boomertechie/opensource_church_software/main/deployments/small-church/.env.example
cp .env.example .env

# Edit configuration — fill in all fields, leave nothing blank
nano .env
```

Generate passwords with:
```bash
openssl rand -base64 24
```

### 4. Start the Stack

```bash
docker compose up -d
```

Wait 2-3 minutes for all services to initialize.

### 5. Complete Setup

**WordPress:** Visit `https://www.yourchurch.com`, complete setup wizard, install Sermon Manager, The Events Calendar, WP Mail SMTP, and Wordfence Security.

**ChurchCRM:** Visit `https://crm.yourchurch.com`, create admin account, configure email settings, set up groups and check-in.

**Nextcloud:** Visit `https://files.yourchurch.com`, install Calendar, Contacts, Deck, and Forms apps.

**Listmonk:** Visit `https://news.yourchurch.com`, configure SMTP, create subscriber lists.

**Uptime Kuma:** Visit `https://status.yourchurch.com`, create admin account, add monitors for each subdomain, configure notifications.

## Maintenance

### Backup Strategy

Create `backup.sh`:

```bash
#!/bin/bash
set -euo pipefail

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$HOME/backups"
mkdir -p $BACKUP_DIR

echo "Starting backup at $DATE..."

# WordPress
docker run --rm -v small-church_wordpress-data:/data -v $BACKUP_DIR:/backup alpine \
  tar czf /backup/wordpress_$DATE.tar.gz -C /data .
docker exec small-church-wordpress-db mysqldump -u root -p${MYSQL_ROOT_PASSWORD} wordpress > \
  $BACKUP_DIR/wordpress_db_$DATE.sql

# ChurchCRM
docker run --rm -v small-church_churchcrm-data:/data -v $BACKUP_DIR:/backup alpine \
  tar czf /backup/churchcrm_$DATE.tar.gz -C /data .
docker exec small-church-churchcrm-db mysqldump -u root -p${MYSQL_ROOT_PASSWORD_2} churchcrm > \
  $BACKUP_DIR/churchcrm_db_$DATE.sql

# Nextcloud
docker run --rm -v small-church_nextcloud-data-files:/data -v $BACKUP_DIR:/backup alpine \
  tar czf /backup/nextcloud_$DATE.tar.gz -C /data .
docker exec small-church-nextcloud-db mysqldump -u root -p${MYSQL_ROOT_PASSWORD_3} nextcloud > \
  $BACKUP_DIR/nextcloud_db_$DATE.sql

# Listmonk
docker run --rm -v small-church_listmonk-data:/data -v $BACKUP_DIR:/backup alpine \
  tar czf /backup/listmonk_$DATE.tar.gz -C /data .
docker exec small-church-listmonk-db pg_dump -U listmonk listmonk > \
  $BACKUP_DIR/listmonk_db_$DATE.sql

# Cleanup old backups (keep 14 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +14 -delete
find $BACKUP_DIR -name "*.sql" -mtime +14 -delete

echo "Backup completed: $(date)"
```

Make executable and schedule:
```bash
chmod +x backup.sh
(crontab -l 2>/dev/null; echo "0 2 * * * $HOME/small-church/backup.sh >> /var/log/church-backup.log 2>&1") | crontab -
```

Copy backups off this server — Backblaze B2 is $5/month for plenty of space.

## Restore (test this BEFORE you need it)

A backup you have never restored is a hope, not a plan. Practice this on a spare server or fresh directory before disaster strikes.

### Restore WordPress

```bash
cd ~/small-church

# 1. Stop the stack
docker compose down

# 2. Restore file volume
docker run --rm \
  -v small-church_wordpress-data:/data \
  -v $HOME/backups:/backup \
  alpine sh -c "rm -rf /data/* && tar xzf /backup/wordpress_YYYYMMDD_HHMMSS.tar.gz -C /data"

# 3. Start database, restore SQL dump
docker compose up -d wordpress-db
sleep 15
docker exec -i small-church-wordpress-db mysql -u root -p${MYSQL_ROOT_PASSWORD} wordpress \
  < $HOME/backups/wordpress_db_YYYYMMDD_HHMMSS.sql

# 4. Start everything
docker compose up -d

# 5. Verify: open https://www.yourchurch.com and log in
```

### Restore ChurchCRM

```bash
docker run --rm \
  -v small-church_churchcrm-data:/data \
  -v $HOME/backups:/backup \
  alpine sh -c "rm -rf /data/* && tar xzf /backup/churchcrm_YYYYMMDD_HHMMSS.tar.gz -C /data"

docker exec -i small-church-churchcrm-db mysql -u root -p${MYSQL_ROOT_PASSWORD_2} churchcrm \
  < $HOME/backups/churchcrm_db_YYYYMMDD_HHMMSS.sql

# Verify: open https://crm.yourchurch.com and confirm member records are present
```

### Restore Nextcloud

```bash
# Put Nextcloud in maintenance mode before restore
docker exec small-church-nextcloud php occ maintenance:mode --on

# Restore files
docker run --rm \
  -v small-church_nextcloud-data-files:/data \
  -v $HOME/backups:/backup \
  alpine sh -c "rm -rf /data/* && tar xzf /backup/nextcloud_YYYYMMDD_HHMMSS.tar.gz -C /data"

# Restore database
docker exec -i small-church-nextcloud-db mysql -u root -p${MYSQL_ROOT_PASSWORD_3} nextcloud \
  < $HOME/backups/nextcloud_db_YYYYMMDD_HHMMSS.sql

# Turn off maintenance mode
docker exec small-church-nextcloud php occ maintenance:mode --off

# Verify: open https://files.yourchurch.com and confirm files exist
```

### Restore Listmonk

```bash
docker run --rm \
  -v small-church_listmonk-data:/data \
  -v $HOME/backups:/backup \
  alpine sh -c "rm -rf /data/* && tar xzf /backup/listmonk_YYYYMMDD_HHMMSS.tar.gz -C /data"

docker exec -i small-church-listmonk-db psql -U listmonk listmonk \
  < $HOME/backups/listmonk_db_YYYYMMDD_HHMMSS.sql

# Verify: open https://news.yourchurch.com and confirm subscriber lists exist
```

### Updates

This stack uses **Diun** for image-update notifications. Diun does not update containers automatically — it emails you when a watched image has a new tag, and you apply the update manually during a maintenance window.

**To apply updates after a Diun notification:**

```bash
cd ~/small-church
docker compose pull
docker compose up -d
```

Run this during a quiet weekday window — never on Saturday night or Sunday morning. Test the affected service immediately after.

**Application-level updates (separate from container updates):**

- **WordPress:** Admin panel → Updates
- **ChurchCRM:** Built-in updater
- **Nextcloud:** Admin panel → Overview → Update
- **Listmonk:** Bump the image tag in `docker-compose.yml` and re-run `docker compose up -d`

### Monitoring

Check Uptime Kuma dashboard regularly. Common issues:

- **High CPU/Memory:** Check `docker stats`
- **Slow Nextcloud:** Redis is already configured; consider enabling PHP OPcache
- **Database errors:** Check individual service logs

## Troubleshooting

### Services won't start
```bash
# Check logs
docker compose logs [service-name]

# Check disk space
df -h

# Check memory
free -h
```

### SSL certificate issues
```bash
# Force renewal
docker compose down
rm -f letsencrypt/acme.json
docker compose up -d
```

### Database connection errors
```bash
# Verify databases are healthy
docker compose ps

# Check specific database logs
docker compose logs [db-name]
```

### Nextcloud performance issues
```bash
# Enable Redis in Nextcloud config
docker exec -it small-church-nextcloud \
  su -s /bin/sh www-data -c "php occ config:system:set memcache.local --value='\\OC\\Memcache\\Redis'"
docker exec -it small-church-nextcloud \
  su -s /bin/sh www-data -c "php occ config:system:set memcache.locking --value='\\OC\\Memcache\\Redis'"
docker exec -it small-church-nextcloud \
  su -s /bin/sh www-data -c "php occ config:system:set redis host --value=nextcloud-redis"
```

## Security Best Practices

1. **All passwords are required** — the stack will not start with blank values
2. **Regular backups:** Daily automated, test restore monthly
3. **Firewall:**
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```
4. **Fail2ban:** Install and configure for SSH protection
5. **Updates:** Apply after a Diun notification during a maintenance window
6. **Nextcloud security:** Enable 2FA for all admin accounts

## Support Resources

- WordPress: https://wordpress.org/support/
- ChurchCRM: https://github.com/ChurchCRM/CRM/wiki
- Nextcloud: https://docs.nextcloud.com/
- Listmonk: https://listmonk.app/docs/
- Uptime Kuma: https://github.com/louislam/uptime-kuma

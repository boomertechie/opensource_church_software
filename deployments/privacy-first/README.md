# Privacy-First Stack

> Fully self-hosted church technology stack for data sovereignty and privacy.

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

## Philosophy

This stack is for churches that:
- Believe member data belongs to the church, not third parties
- Want to avoid vendor lock-in and subscription fees
- Have (or can develop) technical expertise
- Value privacy and security

**What "Privacy-First" Means:**
- All data stored on your servers
- No third-party analytics or tracking
- Open source throughout
- Encrypted backups you control
- Self-hosted email capability

## What's Included

| Function | Tool | Purpose |
|----------|------|---------|
| **Website** | WordPress | Content, sermons, events |
| **ChMS** | ChurchCRM | Membership, giving, check-in |
| **Files/Collaboration** | Nextcloud | Documents, calendars, contacts |
| **Document Editing** | OnlyOffice | Collaborative document editing |
| **Email Lists** | Listmonk | Newsletters, announcements |
| **Email Server** | Mail-in-a-Box | Self-hosted email (separate VM) |
| **Video Conferencing** | Jitsi Meet | Online meetings, Bible studies |
| **Password Management** | Vaultwarden | Team password vault |
| **Monitoring** | Uptime Kuma | Service health monitoring |
| **Backups** | Duplicati | Encrypted, deduplicated backups |
| **Updates** | Diun | Notifies you of available container image updates (manual apply) |

## Update Policy

This stack pins images to stable version tags. Diun (already included) emails you weekly when a new image tag is available. When you receive a notification, schedule a maintenance window, take a backup, then run `docker compose pull && docker compose up -d`. Never update on Saturday night or Sunday morning.

## System Requirements

### Main Server
- **VPS/Dedicated:** 4GB RAM minimum, 8GB recommended
- **Storage:** 100GB minimum (more for file storage)
- **OS:** Ubuntu 22.04 LTS
- **Domain:** Main domain + multiple subdomains
- **IP:** Static IP address

### Email Server (Mail-in-a-Box)
- **Separate VPS:** 1GB RAM, 25GB storage
- **OS:** Ubuntu 22.04 LTS
- **Domain:** mail.yourdomain.com
- **IP:** Static IP with good reputation

## Quick Start

### Phase 1: Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker

# Set up firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 10000/udp  # Jitsi
sudo ufw --force enable
```

### Phase 2: DNS Configuration

Configure these DNS records pointing to your server IP:
- www.yourchurch.com (WordPress)
- crm.yourchurch.com (ChurchCRM)
- cloud.yourchurch.com (Nextcloud)
- office.yourchurch.com (OnlyOffice)
- news.yourchurch.com (Listmonk)
- meet.yourchurch.com (Jitsi)
- pass.yourchurch.com (Vaultwarden)
- status.yourchurch.com (Uptime Kuma)
- backup.yourchurch.com (Duplicati)

### Phase 3: Deploy

```bash
# Download and configure
curl -o docker-compose.yml https://raw.githubusercontent.com/boomertechie/opensource_church_software/main/deployments/privacy-first/docker-compose.yml
curl -o .env.example https://raw.githubusercontent.com/boomertechie/opensource_church_software/main/deployments/privacy-first/.env.example
cp .env.example .env

# Edit .env — fill in all fields, leave nothing blank
nano .env

# Start services
docker compose up -d
```

### Phase 4: Configure Each Service

1. **Nextcloud** - Enable Calendar, Contacts, Deck apps; connect OnlyOffice
2. **ChurchCRM** - Import members, set up groups, configure check-in
3. **Listmonk** - Configure SMTP, create mailing lists, import subscribers
4. **Jitsi** - Test video calls, create persistent rooms
5. **Vaultwarden** - Enable 2FA, create organization, invite users
6. **Duplicati** - Set up encrypted backups to S3/B2

## Security Best Practices

- All passwords are required — the stack will not start with blank values
- Enable 2FA on all admin accounts
- Configure fail2ban on the host
- Regular security updates
- Encrypted offsite backups
- Monitor Uptime Kuma alerts

## Traefik and docker.sock

Traefik mounts `/var/run/docker.sock` to discover containers automatically. This is standard for Traefik-based stacks, but it gives Traefik significant control over the Docker host. Treat this server and its SSH access as high-trust.

For those who want an extra layer of isolation, [docker-socket-proxy](https://github.com/Tecnativa/docker-socket-proxy) sits between Traefik and the Docker socket and exposes only the read-only endpoints Traefik actually needs. This is an optional hardening step — the stack works without it, but it is worth considering if you are running other potentially untrusted containers on the same host.

## Backup Strategy

Create `backup.sh`:

```bash
#!/bin/bash
set -euo pipefail

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$HOME/backups"
mkdir -p $BACKUP_DIR

echo "Starting backup at $DATE..."

# WordPress
docker run --rm -v privacy-first_wordpress-data:/data -v $BACKUP_DIR:/backup alpine \
  tar czf /backup/wordpress_$DATE.tar.gz -C /data .
docker exec privacy-first-wordpress-db mysqldump -u root -p${MYSQL_ROOT_PASSWORD} wordpress > \
  $BACKUP_DIR/wordpress_db_$DATE.sql

# ChurchCRM
docker run --rm -v privacy-first_churchcrm-data:/data -v $BACKUP_DIR:/backup alpine \
  tar czf /backup/churchcrm_$DATE.tar.gz -C /data .
docker exec privacy-first-churchcrm-db mysqldump -u root -p${MYSQL_ROOT_PASSWORD_2} churchcrm > \
  $BACKUP_DIR/churchcrm_db_$DATE.sql

# Nextcloud
docker run --rm -v privacy-first_nextcloud-files:/data -v $BACKUP_DIR:/backup alpine \
  tar czf /backup/nextcloud_$DATE.tar.gz -C /data .
docker exec privacy-first-nextcloud-db mysqldump -u root -p${MYSQL_ROOT_PASSWORD_3} nextcloud > \
  $BACKUP_DIR/nextcloud_db_$DATE.sql

# Listmonk
docker run --rm -v privacy-first_listmonk-data:/data -v $BACKUP_DIR:/backup alpine \
  tar czf /backup/listmonk_$DATE.tar.gz -C /data .
docker exec privacy-first-listmonk-db pg_dump -U listmonk listmonk > \
  $BACKUP_DIR/listmonk_db_$DATE.sql

# Vaultwarden
docker run --rm -v privacy-first_vaultwarden-data:/data -v $BACKUP_DIR:/backup alpine \
  tar czf /backup/vaultwarden_$DATE.tar.gz -C /data .

# Cleanup (keep 14 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +14 -delete
find $BACKUP_DIR -name "*.sql" -mtime +14 -delete

echo "Backup completed: $(date)"
```

Schedule it:
```bash
chmod +x backup.sh
(crontab -l 2>/dev/null; echo "0 2 * * * $HOME/church/backup.sh >> /var/log/church-backup.log 2>&1") | crontab -
```

Duplicati (already in this stack) can sync these local backups to S3/B2 with encryption. Configure it at `https://backup.yourchurch.com` after first boot.

## Restore (test this BEFORE you need it)

A backup you have never restored is a hope, not a plan. Practice on a spare server or fresh directory.

### Restore WordPress

```bash
docker compose down

docker run --rm \
  -v privacy-first_wordpress-data:/data \
  -v $HOME/backups:/backup \
  alpine sh -c "rm -rf /data/* && tar xzf /backup/wordpress_YYYYMMDD_HHMMSS.tar.gz -C /data"

docker compose up -d wordpress-db
sleep 15
docker exec -i privacy-first-wordpress-db mysql -u root -p${MYSQL_ROOT_PASSWORD} wordpress \
  < $HOME/backups/wordpress_db_YYYYMMDD_HHMMSS.sql

docker compose up -d

# Verify: open https://www.yourchurch.com and log in
```

### Restore ChurchCRM

```bash
docker run --rm \
  -v privacy-first_churchcrm-data:/data \
  -v $HOME/backups:/backup \
  alpine sh -c "rm -rf /data/* && tar xzf /backup/churchcrm_YYYYMMDD_HHMMSS.tar.gz -C /data"

docker exec -i privacy-first-churchcrm-db mysql -u root -p${MYSQL_ROOT_PASSWORD_2} churchcrm \
  < $HOME/backups/churchcrm_db_YYYYMMDD_HHMMSS.sql

# Verify: open https://crm.yourchurch.com and confirm member records
```

### Restore Nextcloud

```bash
# Put Nextcloud in maintenance mode before restore
docker exec privacy-first-nextcloud php occ maintenance:mode --on

docker run --rm \
  -v privacy-first_nextcloud-files:/data \
  -v $HOME/backups:/backup \
  alpine sh -c "rm -rf /data/* && tar xzf /backup/nextcloud_YYYYMMDD_HHMMSS.tar.gz -C /data"

docker exec -i privacy-first-nextcloud-db mysql -u root -p${MYSQL_ROOT_PASSWORD_3} nextcloud \
  < $HOME/backups/nextcloud_db_YYYYMMDD_HHMMSS.sql

docker exec privacy-first-nextcloud php occ maintenance:mode --off

# Verify: open https://cloud.yourchurch.com and confirm files exist
```

### Restore Vaultwarden

```bash
# Stop Vaultwarden first to prevent database corruption
docker compose stop vaultwarden

docker run --rm \
  -v privacy-first_vaultwarden-data:/data \
  -v $HOME/backups:/backup \
  alpine sh -c "rm -rf /data/* && tar xzf /backup/vaultwarden_YYYYMMDD_HHMMSS.tar.gz -C /data"

docker compose start vaultwarden

# Verify: open https://pass.yourchurch.com and log in with a staff account
```

### Restore Listmonk

```bash
docker run --rm \
  -v privacy-first_listmonk-data:/data \
  -v $HOME/backups:/backup \
  alpine sh -c "rm -rf /data/* && tar xzf /backup/listmonk_YYYYMMDD_HHMMSS.tar.gz -C /data"

docker exec -i privacy-first-listmonk-db psql -U listmonk listmonk \
  < $HOME/backups/listmonk_db_YYYYMMDD_HHMMSS.sql

# Verify: open https://news.yourchurch.com and confirm subscriber lists exist
```

## Support Resources

See individual service documentation for detailed help.

- WordPress: https://wordpress.org/support/
- ChurchCRM: https://github.com/ChurchCRM/CRM/wiki
- Nextcloud: https://docs.nextcloud.com/
- Listmonk: https://listmonk.app/docs/
- Jitsi: https://jitsi.github.io/handbook/
- Vaultwarden: https://github.com/dani-garcia/vaultwarden/wiki
- Uptime Kuma: https://github.com/louislam/uptime-kuma
- Duplicati: https://duplicati.readthedocs.io/

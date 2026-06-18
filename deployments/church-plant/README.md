# Church Plant Stack

> Zero-budget, minimal setup for new churches. One domain, one weekend.

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

| Function | Tool | Why |
|----------|------|-----|
| **Website** | WordPress | Familiar, plugin ecosystem, easy themes |
| **ChMS** | ChurchCRM | Member tracking, groups, basic check-in |
| **Database** | Adminer | Easy database management — opt-in only |
| **Proxy/SSL** | Traefik | Automatic HTTPS, simple routing |

## Update Policy

This stack pins images to stable version tags. Pinning gives you a predictable, tested version instead of an unknown update landing silently.

**How to stay updated:** Run [Diun](https://github.com/crazy-max/diun) (recommended in the root guide) to receive email notifications when a new image tag is published. When you get a notification, take a backup first, then run `docker compose pull && docker compose up -d` during a quiet weekday window.

## System Requirements

- **Server:** VPS with 1GB RAM (2GB recommended), 20GB storage
- **OS:** Ubuntu 22.04 LTS or Debian 12
- **Domain:** One domain with DNS access
- **Skills:** Basic Linux command line, Docker familiarity helpful

## Quick Start

### 1. Prepare Your Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create directory
mkdir -p ~/church-plant && cd ~/church-plant
```

### 2. Download Stack Files

```bash
# Download docker-compose.yml
curl -o docker-compose.yml https://raw.githubusercontent.com/boomertechie/opensource_church_software/main/deployments/church-plant/docker-compose.yml

# Download environment template
curl -o .env.example https://raw.githubusercontent.com/boomertechie/opensource_church_software/main/deployments/church-plant/.env.example
cp .env.example .env
```

### 3. Configure Environment

```bash
nano .env
```

Fill in all values. Leave nothing blank — the stack will refuse to start until every required variable has a real value.

To generate strong passwords:
```bash
openssl rand -base64 24
```

Run it once per password field.

### 4. Start the Stack

```bash
docker-compose up -d
```

### 5. Complete Setup

**WordPress:**
1. Visit `https://www.yourchurch.com`
2. Complete WordPress setup wizard
3. Install a church theme (recommend: "Church" or "Faith")
4. Essential plugins:
   - "Sermon Manager" for sermons
   - "The Events Calendar" for events
   - "WP Mail SMTP" for email

**ChurchCRM:**
1. Visit `https://crm.yourchurch.com`
2. Create admin account
3. Complete initial setup wizard
4. Configure email settings
5. Import members or add manually

## Adminer — Opt-In Database Panel

Adminer lets you browse and edit database contents through a web interface. A database panel left running permanently is an attractive target — it exposes direct read/write access to every table behind only basic auth. Start it only when you need it, then stop it when you are done.

```bash
# Start Adminer (when you need it)
docker compose --profile adminer up -d adminer

# Stop Adminer (immediately after you're done)
docker compose stop adminer
```

Before enabling Adminer, replace the default `ADMINER_AUTH` value in your `.env` with a fresh hash:

```bash
htpasswd -nb admin yourpassword | sed -e 's/\$/\$\$/g'
```

## Maintenance

### Backup

Create `backup.sh`:

```bash
#!/bin/bash
set -euo pipefail
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$HOME/backups"
mkdir -p $BACKUP_DIR

# Backup WordPress files
docker run --rm -v church-plant_wordpress-data:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/wordpress_$DATE.tar.gz -C /data .

# Backup ChurchCRM files
docker run --rm -v church-plant_churchcrm-data:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/churchcrm_$DATE.tar.gz -C /data .

# Backup databases
docker exec church-plant-wordpress-db mysqldump -u root -p${MYSQL_ROOT_PASSWORD} wordpress > $BACKUP_DIR/wordpress_db_$DATE.sql
docker exec church-plant-churchcrm-db mysqldump -u root -p${MYSQL_ROOT_PASSWORD_2} churchcrm > $BACKUP_DIR/churchcrm_db_$DATE.sql

# Keep only last 7 days
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete

echo "Backup completed: $DATE"
```

Add to crontab:
```bash
chmod +x backup.sh
(crontab -l 2>/dev/null; echo "0 2 * * * $HOME/church-plant/backup.sh >> /var/log/church-backup.log 2>&1") | crontab -
```

Copy backups off this server — Backblaze B2 is $5/month for plenty of space.

### Updates

See **Update Policy** above. Short version: backup, then pull.

```bash
docker-compose pull
docker-compose up -d
```

## Restore (test this BEFORE you need it)

A backup you have never restored is a hope, not a plan. Practice this on a spare server or fresh directory.

### Restore WordPress

```bash
# 1. Stop the stack
docker-compose down

# 2. Restore WordPress file volume
docker run --rm \
  -v church-plant_wordpress-data:/data \
  -v $HOME/backups:/backup \
  alpine sh -c "rm -rf /data/* && tar xzf /backup/wordpress_YYYYMMDD_HHMMSS.tar.gz -C /data"

# 3. Start just the database, restore the SQL dump
docker-compose up -d wordpress-db
sleep 15
docker exec -i church-plant-wordpress-db mysql -u root -p${MYSQL_ROOT_PASSWORD} wordpress \
  < $HOME/backups/wordpress_db_YYYYMMDD_HHMMSS.sql

# 4. Start everything
docker-compose up -d

# 5. Verify: open https://www.yourchurch.com and log in
```

### Restore ChurchCRM

```bash
docker run --rm \
  -v church-plant_churchcrm-data:/data \
  -v $HOME/backups:/backup \
  alpine sh -c "rm -rf /data/* && tar xzf /backup/churchcrm_YYYYMMDD_HHMMSS.tar.gz -C /data"

docker exec -i church-plant-churchcrm-db mysql -u root -p${MYSQL_ROOT_PASSWORD_2} churchcrm \
  < $HOME/backups/churchcrm_db_YYYYMMDD_HHMMSS.sql

# Verify: open https://crm.yourchurch.com and confirm member data is present
```

## Troubleshooting

### Can't access sites
```bash
# Check containers are running
docker-compose ps

# Check logs
docker-compose logs traefik
docker-compose logs wordpress

# Verify DNS
dig +short www.yourchurch.com
```

### SSL certificate issues
```bash
# View Traefik logs
docker-compose logs traefik

# Force renewal (delete acme.json and restart)
docker-compose down
rm letsencrypt/acme.json
docker-compose up -d
```

### Database connection errors
```bash
# Verify databases are healthy
docker-compose ps

# Check database logs
docker-compose logs wordpress-db
docker-compose logs churchcrm-db
```

## Security Notes

1. **Passwords are required** — the stack will not start until all variables are set
2. **Enable WordPress security plugin** (Wordfence or similar)
3. **Keep backups offsite** (rsync to another server or Backblaze B2)
4. **Configure firewall:**
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```
5. **Enable automatic security updates:**
   ```bash
   sudo apt install unattended-upgrades
   sudo dpkg-reconfigure unattended-upgrades
   ```
6. **No reverse proxy on this stack** means HSTS and security headers are managed by Traefik. If you ever remove Traefik, see the production guidance in the root guide for manual header configuration.

## Migration Path

When ready to upgrade to Small Church Stack:

1. Export data from WordPress (Tools → Export)
2. Export ChurchCRM database
3. Deploy Small Church Stack on larger server
4. Import data
5. Redirect domains

## Support

- WordPress docs: https://wordpress.org/support/
- ChurchCRM docs: https://github.com/ChurchCRM/CRM/wiki
- Traefik docs: https://doc.traefik.io/traefik/

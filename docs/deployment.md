# Deployment Architecture — Magic Bar Website

This document describes the authoritative production architecture.
Follow this exactly to avoid breaking uploads or deployments.

---

## Architecture Overview

Browser  
→ Nginx (system service)  
→ Docker (Django application)  
→ SQLite database + persistent media

---

## Tech Stack

- Hosting: AWS EC2 (Ubuntu)
- Web Server: Nginx (systemctl, NOT containerized)
- Application: Django
- Containerization: Docker Compose
- Database: SQLite
- Source Control: GitHub

---

## Responsibilities

### Nginx (Host)
- Serves `/media/` and `/static/`
- Terminates HTTPS
- Proxies requests to Django

### Django (Container)
- Handles application logic
- Handles admin uploads
- Writes uploaded files to `/app/media`

---

## Media Handling (CRITICAL)

### Canonical Media Pipeline

Admin Upload  
→ Django saves to `MEDIA_ROOT`  
→ Docker bind mount  
→ Host filesystem  
→ Nginx serves publicly

### Canonical Paths

| Purpose | Path |
|------|------|
| MEDIA_ROOT (container) | `/app/media` |
| Media on host | `/var/www/magicbar/media` |
| Event images | `/var/www/magicbar/media/events` |
| Carousel images | `/var/www/magicbar/media/carousel` |
| Cocktail menus | `/var/www/magicbar/media/cocktail_menus` |
| Kitchen menus | `/var/www/magicbar/media/kitchen_menus` |

---

## Docker Compose (Production)

```yaml
services:
  web:
    volumes:
      - ./backend:/app
      - /var/www/magicbar/media:/app/media
```

This volume mapping is **mandatory**.

---

## Nginx Configuration

```nginx
location /media/ {
    alias /var/www/magicbar/media/;
}

location /static/ {
    alias /var/www/magicbar/static/;
}
```

---

## Deployment Workflow

1. Edit code locally
2. Commit & push to GitHub
3. SSH into server
4. `git pull`
5. `./deploy.sh`
6. Restart Docker containers if needed

---

## Rules (Non-Negotiable)

- Never commit `media/` to Git
- Never serve media via Django in production
- Never invent a second upload pipeline
- If carousel uploads work, copy that pattern exactly

---

## Verification Commands

```bash
ls -la /var/www/magicbar/media/events
docker compose exec web ls -la /app/media/events
curl -I https://yourdomain/media/events/example.jpg
```

If all three succeed, uploads are correctly configured.

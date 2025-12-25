# Deployment Architecture — Magic Bar Website

This document describes the **authoritative production architecture** for the Magic Bar website.
Follow this exactly to avoid breaking uploads, media, or deployments.

---

## High-Level Architecture

Browser  
→ **Nginx (system service)**  
→ **Docker container (Django app)**  
→ SQLite database + persistent media storage

---

## Tech Stack

- OS: Ubuntu (AWS EC2)
- Web Server: Nginx (systemctl, NOT containerized)
- App: Django (Dockerized)
- Container Orchestration: Docker Compose
- Database: SQLite
- Source Control: GitHub

---

## Roles & Responsibilities

### Nginx (Host)
- Serves `/media/` and `/static/`
- Terminates HTTPS
- Proxies requests to Django container

### Docker / Django
- Handles all application logic
- Handles admin uploads
- Writes uploaded files to `/app/media`

---

## Media Handling (CRITICAL)

### Canonical Media Pipeline

Admin Upload  
→ Django saves to `MEDIA_ROOT`  
→ Docker bind-mount  
→ Host filesystem  
→ Nginx serves publicly

### Canonical Paths

| Purpose | Path |
|------|------|
| MEDIA_ROOT (container) | `/app/media` |
| Media on host | `/var/www/magicbar/media` |
| Carousel images | `/var/www/magicbar/media/carousel/` |
| Event images | `/var/www/magicbar/media/events/` |
| Cocktail menus | `/var/www/magicbar/media/cocktail_menus/` |
| Kitchen menus | `/var/www/magicbar/media/kitchen_menus/` |

---

## Docker Compose (Production)

```yaml
services:
  web:
    volumes:
      - ./backend:/app
      - /var/www/magicbar/media:/app/media

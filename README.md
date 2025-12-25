# Magic Bar Website

Production website for **Little Magic JC**, built with Django and deployed on AWS using Docker and Nginx.

This repository contains the application code, deployment configuration, and operational documentation required to safely develop, deploy, and maintain the site.

---

## ✨ Features

- Public-facing website with custom design
- Admin-managed content:
  - Carousel images
  - Event posts (image + caption)
  - Cocktail & kitchen menus
  - Business hours
- Responsive layout (desktop & mobile)
- Secure admin panel
- Persistent media uploads
- Dockerized deployment

---

## 🧰 Tech Stack

| Layer | Technology |
|-----|-----------|
| Backend | Django |
| Frontend | Django Templates + CSS |
| Containerization | Docker & Docker Compose |
| Web Server | Nginx (system service) |
| Hosting | AWS EC2 (Ubuntu) |
| Database | SQLite |
| Source Control | GitHub |

---

## 📁 Repository Structure

```
.
├── backend/            # Django project
├── docs/               # Authoritative documentation
│   ├── deployment.md   # Production architecture
│   ├── local-dev.md    # Local development workflow
│   └── runbook.md      # Debugging & ops playbook
├── docker-compose.yml
├── deploy.sh
└── README.md
```

---

## 🚀 Local Development (Quick Start)

### Requirements
- Docker
- Docker Compose
- Git

### Start locally
```bash
docker compose up -d --build
```

The site will be available at:
```
http://localhost:8000
```

---

## 🖼️ Media Handling (IMPORTANT)

Uploaded files (events, carousel images, menus) are **NOT tracked in Git**.

### Local
- Media stored in `./media/`
- Served directly by Django (`DEBUG=True`)
- `media/` is ignored by Git

### Production
- Media stored at:
  ```
  /var/www/magicbar/media
  ```
- Served by **Nginx**, not Django
- Persisted outside Docker containers

⚠️ **Never commit uploaded files to Git.**

For details, see:
- `docs/deployment.md`
- `docs/local-dev.md`

---

## 📦 Deployment (Production)

Canonical deployment flow:

1. Make changes locally
2. Commit & push to GitHub
3. SSH into the server
4. Pull changes
5. Run deploy script

```bash
git pull
./deploy.sh
```

Docker containers will be rebuilt/restarted as needed.

---

## 🛠️ Operations & Debugging

If something breaks:
- **Do not guess**
- Follow the checklist in:

```
docs/runbook.md
```

It covers:
- Missing images
- Upload failures
- Nginx misconfiguration
- Git deploy issues
- Permission problems

---

## 🔒 Git Rules (Non-Negotiable)

The following must **never** be committed:

```
media/
db.sqlite3
```

These are environment-specific and will break deployments if tracked.

---

## 🧠 Design Philosophy

- One media pipeline (no exceptions)
- Nginx is authoritative for `/media/` and `/static/`
- Docker containers are disposable
- Production data lives outside containers
- If something already works (e.g., carousel uploads), copy its pattern exactly

---

## 📚 Documentation Index

| Purpose | File |
|------|------|
| Production architecture | `docs/deployment.md` |
| Local development | `docs/local-dev.md` |
| Debugging & ops | `docs/runbook.md` |

---

## 👤 Maintainer Notes

This project is actively developed and deployed.
Changes should prioritize:
- Data safety
- Minimal disruption
- Clear rollback paths

---

## ✅ Status

✔ Local development working  
✔ Production deployment stable  
✔ Media uploads persistent  
✔ Admin-managed content live  

---

## 📌 Next Enhancements (Optional)

- GitHub Actions auto-deploy
- Media backups (S3)
- Admin drag-and-drop ordering
- Scheduled event publishing
- Image auto-cropping

---

**If you’re new to this project, read the `/docs` folder first.**

# Local Development — Magic Bar Website

This document explains how to run, edit, and test the Magic Bar website locally
without breaking production.

---

## Local Environment Overview

Local development differs intentionally from production.

### Local Stack
- Docker Compose
- Django (`DEBUG=True`)
- No Nginx required
- Media served by Django (development only)

Production uses Nginx to serve media; local does not.

---

## Local Docker Setup

Your local `docker-compose.yml` should include a bind-mounted media directory:

```yaml
services:
  web:
    volumes:
      - ./backend:/app
      - ./media:/app/media
```

This creates a local `./media/` directory that:
- Persists uploads
- Is ignored by Git
- Mirrors production behavior safely

---

## Serving Media Locally (DEBUG Only)

Django must serve media files when running locally.

In `magicbarproject/urls.py`:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # app urls
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
```

⚠️ **Never enable this in production.**

---

## Why Images May Be Missing Locally

This is expected behavior if:
- Images were uploaded in production
- `media/` is ignored by Git
- The local `./media/` directory is empty

This does NOT indicate a bug.

---

## Sync Production Media to Local (Optional)

If you want your local environment to display production uploads:

```bash
scp -r -i ~/.ssh/magicbar-prod-key.pem \
  ubuntu@SERVER_IP:/var/www/magicbar/media \
  ./media
```

After copying:
```bash
docker compose down
docker compose up -d --build
```

---

## Best Practices

- Treat local and production media as separate by default
- Sync media only when needed
- Never rely on Git for uploaded files
- Never modify production media from local dev

---

## Local Verification Commands

```bash
ls -la ./media/events
docker compose exec web ls -la /app/media/events
```

If both show files, local media is configured correctly.

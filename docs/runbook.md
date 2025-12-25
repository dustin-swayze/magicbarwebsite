# Runbook — Magic Bar Website

This document is the **operational and debugging playbook**.
Use it when something breaks. Follow the checklist. Do not guess.

---

## 🚨 Issue: Images Upload but Do Not Display

### Step 1 — Check inside the container
```bash
docker compose exec web ls -la /app/media/events
```

If files do not appear here, Django is not saving uploads correctly.

---

### Step 2 — Check the host filesystem
```bash
ls -la /var/www/magicbar/media/events
```

If files appear in the container but not on the host, the Docker volume
mapping is incorrect.

---

### Step 3 — Check Nginx serving
```bash
curl -I https://yourdomain/media/events/example.jpg
```

Expected:
- `200 OK`
- or `301` redirect to HTTPS

If `404`, Nginx is not serving the correct directory.

---

## 🚨 Issue: Carousel Works, Events Do Not

**Cause**  
Event uploads are not following the same media pipeline as carousel uploads.

**Fix**
- Confirm Event model uses `upload_to="events/"`
- Confirm Docker volume:
  ```
  /var/www/magicbar/media:/app/media
  ```
- Restart containers

---

## 🚨 Issue: Deploy Script Fails (“working tree is not clean”)

**Cause**
- `media/` folder exists inside the Git repo

**Fix**
```bash
echo "media/" >> .gitignore
git add .gitignore
git commit -m "Ignore media uploads"
rm -rf media/
```

---

## 🚨 Issue: Images Show in Production but Not Locally

**Cause**
- Media is ignored by Git
- Local media directory is empty

**Fix options**
- Upload images locally
- OR sync production media:
  ```bash
  scp -r -i ~/.ssh/magicbar-prod-key.pem \
    ubuntu@SERVER_IP:/var/www/magicbar/media \
    ./media
  ```

---

## 🚨 Issue: Nginx Returns 404 for `/media/*`

### Checklist
- Correct `server_name`
- Correct `location /media/` alias
- File exists on disk

```bash
sudo nginx -T | grep -n "location /media" -n -B2 -A3
```

---

## 🚨 Issue: Permission Denied Errors

**Fix**
```bash
sudo chown -R ubuntu:www-data /var/www/magicbar/media
sudo find /var/www/magicbar/media -type d -exec chmod 775 {} \;
sudo find /var/www/magicbar/media -type f -exec chmod 664 {} \;
```

---

## 🚨 Issue: `scp` Permission Denied

### Local key permissions
```bash
chmod 600 ~/.ssh/magicbar-prod-key.pem
```

### Force key usage
```bash
scp -o IdentitiesOnly=yes -i ~/.ssh/magicbar-prod-key.pem ...
```

---

## Golden Rules (Read This First)

- If one upload type works, copy its entire pattern
- Never debug uploads by changing everything at once
- Never commit media or databases to Git
- Always verify with `ls` and `curl` before changing configs

---

## Emergency Sanity Check (Fast)

```bash
docker compose ps
ls -la /var/www/magicbar/media
curl -I https://yourdomain/media/
```

If these pass, the system is healthy.

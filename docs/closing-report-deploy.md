Production checklist to repeat later (save this)

When you push to live and deploy:

Pull latest code

git pull

Rebuild / restart containers (your normal deploy flow)

./deploy.sh

(or your existing production steps)

Run migrations in production

docker compose exec web python manage.py migrate

Create StaffMember data in production

Visit /admin/

Add StaffMember rows for bartenders / barbacks / security

Mark them active=True

Set management recipients in production

Ensure prod has:

CLOSING_REPORT_RECIPIENTS = [...]

email backend configured (SMTP/SES/etc)

Production test

Go to /closing/

Create report → preview → email

Confirm you receive email + emailed_at is set in admin
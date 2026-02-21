from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from decimal import Decimal
import uuid


class StaffRole(models.TextChoices):
    BARTENDER = "bartender", "Bartender"
    BARBACK = "barback", "Barback"
    SECURITY = "security", "Security"


class StaffMember(models.Model):
    """
    Preexisting list of bartenders / barbacks / security.
    You manage these in Django admin.
    """
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=20, choices=StaffRole.choices)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["role", "name"]

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"


def default_business_date():
    """
    If report is completed after midnight, we usually want it to count for "yesterday".
    Cutoff is 6am local time by default. Change if you want.
    """
    now = timezone.localtime(timezone.now())
    cutoff_hour = 6
    if now.hour < cutoff_hour:
        return (now - timezone.timedelta(days=1)).date()
    return now.date()


class ClosingReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="closing_reports_created"
    )

    # "Date" on the report (business date), not necessarily the timestamp submitted
    business_date = models.DateField(default=default_business_date)

    # Staff selections (we’ll enforce max counts in the form)
    bartenders = models.ManyToManyField(StaffMember, related_name="closing_reports_as_bartender", blank=True)
    barbacks = models.ManyToManyField(StaffMember, related_name="closing_reports_as_barback", blank=True)
    security = models.ManyToManyField(StaffMember, related_name="closing_reports_as_security", blank=True)

    total_cash = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    cash_payments = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))  # can be + or -

    eighty_six_list = models.TextField(blank=True)
    shift_notes = models.TextField(blank=True)

    emailed_at = models.DateTimeField(null=True, blank=True)
    emailed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.PROTECT, related_name="closing_reports_emailed"
    )

    class Meta:
        ordering = ["-business_date", "-created_at"]

    def __str__(self):
        return f"Closing Report {self.business_date}"


class PaidOut(models.Model):
    report = models.ForeignKey(ClosingReport, on_delete=models.CASCADE, related_name="paid_outs")
    who = models.CharField(max_length=120)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Enter a positive dollar amount."
    )
    description = models.CharField(max_length=255)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.who} - ${self.amount} - {self.description}"
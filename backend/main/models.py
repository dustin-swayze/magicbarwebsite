from django.db import models
from django.contrib.auth.models import User

class CocktailMenuImage(models.Model):
    image = models.ImageField(upload_to='cocktail_menus/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Menu uploaded by {self.uploaded_by} on {self.uploaded_at}"

class KitchenMenuImage(models.Model):
    image = models.ImageField(upload_to='kitchen_menus/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Kitchen Menu uploaded by {self.uploaded_by} on {self.uploaded_at}"

class CarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Carousel image by {self.uploaded_by} on {self.uploaded_at}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"

class BusinessHours(models.Model):
    DAYS = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    day = models.IntegerField(choices=DAYS, unique=True)
    is_closed = models.BooleanField(default=False)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    notes = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["day"]

    def __str__(self):
        return f"{self.get_day_display()} hours"

class EventPost(models.Model):
    title = models.CharField(max_length=120, blank=True)
    image = models.ImageField(upload_to='events/')
    caption = models.CharField(max_length=220)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    is_approved = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    order = models.PositiveIntegerField(default=0, help_text="Lower shows first")

    class Meta:
        ordering = ["order", "-uploaded_at"]

    def __str__(self):
        name = self.title.strip() if self.title else "Event"
        return f"{name} (order {self.order})"

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
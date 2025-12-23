from django import forms
from .models import CocktailMenuImage, KitchenMenuImage, CarouselImage, ContactMessage, BusinessHours


class CocktailMenuImageForm(forms.ModelForm):
    class Meta:
        model = CocktailMenuImage
        fields = ['image']

class KitchenMenuImageForm(forms.ModelForm):
    class Meta:
        model = KitchenMenuImage
        fields = ['image']

class CarouselImageForm(forms.ModelForm):
    class Meta:
        model = CarouselImage
        fields = ['image']

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

class BusinessHoursForm(forms.ModelForm):
    class Meta:
        model = BusinessHours
        fields = ["is_closed", "open_time", "close_time", "notes"]
        widgets = {
            "open_time": forms.TimeInput(format="%H:%M", attrs={"type": "time"}),
            "close_time": forms.TimeInput(format="%H:%M", attrs={"type": "time"}),
        }
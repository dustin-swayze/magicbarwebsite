from django import forms
from .models import CocktailMenuImage, KitchenMenuImage, CarouselImage, ContactMessage


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
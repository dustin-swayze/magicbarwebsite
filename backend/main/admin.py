from django.contrib import admin
from .models import CocktailMenuImage, KitchenMenuImage, CarouselImage
from .models import ContactMessage

@admin.register(CocktailMenuImage)
class CocktailMenuImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_by', 'uploaded_at', 'is_approved')
    list_filter = ('is_approved',)
    actions = ['approve_selected']

    def approve_selected(self, request, queryset):
        queryset.update(is_approved=True)
    approve_selected.short_description = "Mark selected as approved"


@admin.register(KitchenMenuImage)
class KitchenMenuImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_by', 'uploaded_at', 'is_approved')
    list_filter = ('is_approved',)
    actions = ['approve_selected']

    def approve_selected(self, request, queryset):
        queryset.update(is_approved=True)
    approve_selected.short_description = "Mark selected as approved"

@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_by', 'uploaded_at', 'is_approved')
    list_filter = ('is_approved',)
    actions = ['approve_selected']

    def approve_selected(self, request, queryset):
        queryset.update(is_approved=True)
    approve_selected.short_description = "Mark selected images as approved"

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    readonly_fields = ('name', 'email', 'message', 'submitted_at')
    ordering = ('-submitted_at',)

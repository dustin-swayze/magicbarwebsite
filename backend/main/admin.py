from django.contrib import admin
from .models import CocktailMenuImage, KitchenMenuImage, CarouselImage, BusinessHours
from .models import ContactMessage, EventPost

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

@admin.register(BusinessHours)
class BusinessHoursAdmin(admin.ModelAdmin):
    list_display = ("day", "is_closed", "open_time", "close_time", "notes")
    list_editable = ("is_closed", "open_time", "close_time", "notes")
    ordering = ("day",)

@admin.register(EventPost)
class EventPostAdmin(admin.ModelAdmin):
    list_display = ("title", "is_approved", "order", "uploaded_at", "uploaded_by")
    list_filter = ("is_approved",)
    search_fields = ("title", "caption")
    ordering = ("order", "-uploaded_at")
    list_editable = ("order", "is_approved")  # ✅ edit in the list view

    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by_id:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

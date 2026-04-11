from django.contrib import admin
from .models import CocktailMenuImage, KitchenMenuImage, CarouselImage, BusinessHours
from .models import ContactMessage, EventPost
from .models import Cocktail
from .models import HomepagePanel
from adminsortable2.admin import SortableAdminMixin
from .models import KitchenMenu


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
class EventPostAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("title", "is_approved", "order", "uploaded_at", "uploaded_by")
    list_filter = ("is_approved",)
    search_fields = ("title", "caption")
    ordering = ("order", "-uploaded_at")
    list_editable = ("order", "is_approved")  # ✅ edit in the list view

    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by_id:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Cocktail)
class CocktailAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "sort_order")
    list_editable = ("is_active", "sort_order")
    search_fields = ("name", "ingredients")

@admin.register(HomepagePanel)
class HomepagePanelAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("title", "order", "link")

@admin.register(KitchenMenu)
class KitchenMenuAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "uploaded_at")
    list_filter = ("is_active",)
    search_fields = ("title",)

    def save_model(self, request, obj, form, change):
        if obj.is_active:
            KitchenMenu.objects.exclude(pk=obj.pk).update(is_active=False)
        super().save_model(request, obj, form, change)
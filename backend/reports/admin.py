from django.contrib import admin
from .models import StaffMember, ClosingReport, PaidOut


class PaidOutInline(admin.TabularInline):
    model = PaidOut
    extra = 0


@admin.register(ClosingReport)
class ClosingReportAdmin(admin.ModelAdmin):
    list_display = ("business_date", "created_at", "created_by", "emailed_at")
    list_filter = ("business_date", "emailed_at")
    search_fields = ("created_by__username", "eighty_six_list", "shift_notes")
    filter_horizontal = ("bartenders", "barbacks", "security")
    inlines = [PaidOutInline]


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "active")
    list_filter = ("role", "active")
    search_fields = ("name",)
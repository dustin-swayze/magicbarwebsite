from django.urls import path
from . import views

urlpatterns = [
    path("closing/", views.closing_create, name="reports_closing_create"),
    path("closing/<uuid:report_id>/preview/", views.closing_preview, name="reports_closing_preview"),
    path("closing/<uuid:report_id>/send/", views.closing_send, name="reports_closing_send"),
    path("closing/<uuid:report_id>/pdf/", views.closing_pdf, name="reports_closing_pdf"),
]
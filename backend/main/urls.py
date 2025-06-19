from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload-menu/', views.upload_menu, name='upload_menu'),
    path('upload-success/', views.upload_success, name='upload_success'),
    path('upload-kitchen-menu/', views.upload_kitchen_menu, name='upload_kitchen_menu'),
    path('upload-carousel/', views.upload_carousel_image, name='upload_carousel_image'),
    path('contact/', views.contact_view, name='contact'),
    path('contact-success/', views.contact_success, name='contact_success'),
    path('view-messages/', views.view_messages, name='view_messages'),
    path('bar-menu/', views.bar_menu_view, name='bar_menu'),
    path('kitchen-menu/', views.kitchen_menu_view, name='kitchen_menu'),


]

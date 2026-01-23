from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('contact/', views.contact_view, name='contact'),
    path('contact-success/', views.contact_success, name='contact_success'),

    # Menus

    path('bar-menu/', views.bar_menu_view, name='bar_menu'),
    path('kitchen-menu/', views.kitchen_menu_view, name='kitchen_menu'),
    path('order/', views.online_ordering_view, name='online_ordering'),


    # Uploads
    path('upload-menu/', views.upload_menu, name='upload_menu'),
    path('upload-success/', views.upload_success, name='upload_success'),
    path('upload-kitchen-menu/', views.upload_kitchen_menu, name='upload_kitchen_menu'),
    path('upload-carousel/', views.upload_carousel_image, name='upload_carousel_image'),
    
    path('view-messages/', views.view_messages, name='view_messages'),

     # Messages (staff)
    path('manage/messages/', views.view_messages, name='view_messages'),

    # ✅ NEW: Business hours management (staff)
    path('manage/hours/', views.manage_hours, name='manage_hours'),

    
]

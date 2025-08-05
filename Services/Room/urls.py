from django.urls import path
from . import views

urlpatterns = [
    # Main dashboard/hub
    path('dashboard/', views.services_dashboard, name='services_dashboard'),

    # Room management
    path('rooms/', views.room_list_view, name='room_list'),
    path('rooms/create/', views.create_room_view, name='create_room'),
    path('rooms/join/', views.join_room_view, name='join_room'),
    path('rooms/<int:room_id>/', views.room_detail_view, name='room_detail'),
    path('rooms/<int:room_id>/dashboard/', views.room_dashboard_view, name='room_dashboard'),
    path('rooms/<int:room_id>/owner/', views.room_owner_dashboard_view, name='room_owner_dashboard'),

    # Service management
    path('services/<int:service_id>/manage/', views.manage_service, name='manage_service'),
    path('records/<int:record_id>/edit/', views.edit_service_record, name='edit_service_record'),
    path('records/<int:record_id>/delete/', views.delete_service_record, name='delete_service_record'),

    # Admin dashboard
    path('admindashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('rooms/<int:room_id>/remove_member/<int:user_id>/', views.remove_member_view, name='remove_member'),
    path('services/<int:service_id>/delete/', views.delete_service_view, name='delete_service'),

]

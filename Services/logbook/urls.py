from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('',views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('forgot/',views.forgot, name='forgot'),
]

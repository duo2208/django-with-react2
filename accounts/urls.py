from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('password_change/', views.password_change, name='password_change'),
    path('edit/', views.profile_edit, name='profile_edit'),
]
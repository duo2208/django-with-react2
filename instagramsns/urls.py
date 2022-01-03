from django.urls import path
from . import views

app_name = 'instagramsns'

urlpatterns = [
    path('post/new/', views.post_new, name='post_new'),
]
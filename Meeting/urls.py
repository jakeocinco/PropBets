from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='meeting-home'),
    path('about/', views.about, name='meeting-about'),
]

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/submit', views.submit_form, name='submit_profile'),
]

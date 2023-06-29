from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "reviewer"

urlpatterns = [
    path("apply", views.profile, name="profile"),
    path('resume', views.stream_file, name='resume'),
    path('apply/submit', views.submit_form, name='submit_profile'),
]

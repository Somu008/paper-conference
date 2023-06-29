from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'paper'

urlpatterns = [
    path('upload', views.paper, name='upload_paper'),
    path('<id>', views.paper_detail, name='paper_detail'),
    path('', views.papers, name='paper_list'),
    path("<int:pk>/report", views.stream_file, name="report_pdf"),
    path('<id>/<action>', views.update_paper, name="update_paper")
    
]
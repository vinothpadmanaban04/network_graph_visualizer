from django.urls import path
from . import views

urlpatterns = [
    path('', views.visualize_data, name='visualize_data'),  # Set visualize_data as the home page
    path('upload/', views.upload_csv, name='upload_csv'),
    path('get_recent_files/', views.get_recent_files, name='get_recent_files'),
]

# newproject/urls.py
from django.views.generic import RedirectView 
from django.contrib import admin
from django.urls import path, include  # Include 'include' for including app URLs
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', include('graph_app.urls')),  # Include the app's URLs
    path('visualize/', include('graph_app.urls')),  # Include the app's URLs
    path('', RedirectView.as_view(url='upload/', permanent=False)),  # Redirect root to upload
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

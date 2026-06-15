from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', include('backend.authentication.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('backend.authentication.urls')),
    path('dashboard/', include('backend.dashboard.urls')),
    path('booking/', include('backend.booking.urls')),
    path('map/', include('backend.map.urls')),
    path('history/', include('backend.history.urls')),
    path('profile/', include('backend.profile.urls')),
    path('adminpanel/', include('backend.adminpanel.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

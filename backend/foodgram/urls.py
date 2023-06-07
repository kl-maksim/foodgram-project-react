from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from foodgram import settings

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

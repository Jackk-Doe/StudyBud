from django.contrib import admin
from django.urls import path, include

# For storing and routing to images
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # base app path
    path('', include('base.urls')),

    # api path
    path('api/', include('base.api.urls')),
]

# Set path to MEDIA_URL and Get files from MEDIA_ROOT
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
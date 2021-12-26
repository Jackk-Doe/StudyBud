from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # base app path
    path('', include('base.urls')),

    # api path
    path('api/', include('base.api.urls')),
]

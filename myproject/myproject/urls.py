from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('login.urls')),
    path('googlecalendar/', include('googlecalendar.urls')),
    path('', include('login.urls')),
    path('', include('googlecalendar.urls')),
]

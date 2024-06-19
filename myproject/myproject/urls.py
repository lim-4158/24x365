from django.contrib import admin
from django.urls import path, include
from chatbot import views as chatbot_views  # Import the views from the chatbot app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('googlecalendar/', include('googlecalendar.urls')),
    path('', include('googlecalendar.urls')),
    path('api/', include('myapp.urls')),
    path('chat/', include('chatbot.urls')),
]

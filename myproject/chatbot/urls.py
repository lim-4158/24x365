from django.urls import path
from . import views

urlpatterns = [
    # path('', views.chat, name='chat'),
    path('get_response/', views.get_response, name='get_response'),
]

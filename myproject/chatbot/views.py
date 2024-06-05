from django.shortcuts import render

# Create your views here.

from .models import ChatModel

def index(request):
    chats = ChatModel.objects.all()
    return render(request, 'chatbot/index.html', {'chats': chats})

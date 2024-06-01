from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from .models import ChatModel

class ChatModelTestCase(TestCase):
    def setUp(self):
        ChatModel.objects.create(user="testuser", message="Hello", timestamp="2024-01-01 00:00:00")

    def test_chat_model_creation(self):
        chat = ChatModel.objects.get(user="testuser")
        self.assertEqual(chat.message, "Hello")

# chatbot/views.py

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ChatResponseSerializer
import openai
import os

# Set your OpenAI API key here
openai.api_key = os.getenv('OPEN_AI_KEY')

@api_view(['GET'])
def get_response(request):
    user_input = request.GET.get('message')
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
        max_tokens=150
    )
    answer = response.choices[0].message.content
    # print(answer)
    serializer = ChatResponseSerializer(data={'message': answer})
    if serializer.is_valid():
        return Response(serializer.data)
    return Response(serializer.errors)

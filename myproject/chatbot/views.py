# chatbot/views.py

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ChatResponseSerializer
import openai
import os
from datetime import datetime

# Set your OpenAI API key here
openai.api_key = os.getenv('OPEN_AI_KEY')

# You are a part of a larger operation to help with time management to help user add events to their google calendar. Your task is to understand and extract information from the user. 
# You need to get information on the type of event and also the time of event. output in the following format "type: xxx, time: xxx". 
# The type of event is either ADD or DELETE. It means adding or deleting events. 
# Always ask for user confirmation after you retrieved the data. 
# When you are unsure of what the user wants, for example when the user say next wednesday but it could be ambiguous, clarify with the user.

@api_view(['POST'])
def get_response(request):

    # user_input = request.GET.get('message')
    
    conversation = request.data.get('messages', [])

    timenow = datetime.now()
    daynow = datetime.now().strftime("%A")


    formatted_messages = [{"role": "system", "content": f"""The time now is {timenow} and it is {daynow}.You are a part of a larger operation to help with time management to help user add events to their google calendar. Your task is to understand and extract information from the user. 
        You need to get information on the type of event and also the time of event. output in the following format 'type: xxx, time: xxx'. 
        The type of event is either ADD or DELETE. It means adding or deleting events. When I tell you that i got something going on without mentioning deletion, it would mean to add event. the default would be to add. 
        Always ask for user confirmation after you retrieved the data. 
        When you are unsure of what the user wants, for example when the user say next wednesday but it could be ambiguous, clarify with the user. 
        Once clarified, produce a json file with 3 fields, summary, start date and time, end date and time.
    """}]

    for msg in conversation:
        role = "user" if msg['type'] == 'user' else "assistant"
        formatted_messages.append({"role": role, "content": msg['text']})

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo", #gpt-4o #0125
        messages=formatted_messages,
        max_tokens=150
    )


    # response = openai.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "you are a helpful assistant."},
    #         {"role": "user", "content": user_input}
    #     ],
    #     max_tokens=150
    # )
    answer = response.choices[0].message.content
    # print(answer)
    serializer = ChatResponseSerializer(data={'message': answer})
    if serializer.is_valid():
        return Response(serializer.data)
    return Response(serializer.errors)

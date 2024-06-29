# chatbot/views.py

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ChatResponseSerializer
import openai
import os
from datetime import datetime
import json
from googlecalendar.views import create_google_calendar_event  # Import the function
from zoneinfo import ZoneInfo

# Set your OpenAI API key here
openai.api_key = os.getenv('OPEN_AI_KEY')

SGT = ZoneInfo("Asia/Singapore")  

@api_view(['POST'])
def get_response(request):
    conversation = request.data.get('messages', [])

    timenow = datetime.now()
    daynow = datetime.now().strftime("%A")

    system_message = f"""The time now is {timenow} and it is {daynow}. You are a part of a larger operation to help with time management to help users add events to their Google Calendar. Your task is to understand and extract information from the user. 
        You need to get information on the type of event and also the time of event. 
        The type of event is either ADD or DELETE. It means adding or deleting events. 
        When I tell you that I got something going on without mentioning deletion, it would mean to add event. The default would be to add. 
        Always ask for user confirmation after you retrieved the data. 
        When you are unsure of what the user wants, for example when the user says next Wednesday but it could be ambiguous, clarify with the user. 
        Once clarified, call the create_event function with the necessary information.
    """

    formatted_messages = [{"role": "system", "content": system_message}]
    
    for msg in conversation:
        role = "user" if msg['type'] == 'user' else "assistant"
        content = msg['text']
        if isinstance(content, (dict, list)):
            content = json.dumps(content)
        formatted_messages.append({"role": role, "content": content})

    create_event_schema = {
        "type": "object",
        "properties": {
            "summary": {
                "type": "string",
                "description": "A brief description of the event"
            },
            "start": {
                "type": "string",
                "description": "Start date and time of the event in ISO 8601 format"
            },
            "end": {
                "type": "string",
                "description": "End date and time of the event in ISO 8601 format"
            }
        },
        "required": ["summary", "start", "end"]
    }

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=formatted_messages,
            max_tokens=150, 
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "create_event", 
                        "description": "Create a new event in the user's Google Calendar",
                        "parameters": create_event_schema
                    }
                }
            ]
        )

        assistant_message = response.choices[0].message

        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                if tool_call.function.name == "create_event":
                    function_args = json.loads(tool_call.function.arguments)

                    start_time = datetime.fromisoformat(function_args['start']).replace(tzinfo=SGT)
                    end_time = datetime.fromisoformat(function_args['end']).replace(tzinfo=SGT)
                
                    result = create_google_calendar_event(
                        function_args['summary'],
                        start_time.isoformat(),
                        end_time.isoformat()
                    )
                    formatted_messages.append({"role": "function", "name": "create_event", "content": json.dumps(result)})
                    
                    # Get a follow-up response from the model
                    follow_up_response = openai.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=formatted_messages,
                        max_tokens=150
                    )
                    answer = follow_up_response.choices[0].message.content
        else:
            answer = assistant_message.content

        serializer = ChatResponseSerializer(data={'message': answer})
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    except openai.BadRequestError as e:
        return Response({"error": str(e)}, status=400)
    except Exception as e:
        return Response({"error": "An unexpected error occurred"}, status=500)
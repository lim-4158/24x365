# chatbot/views.py

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ChatResponseSerializer
import openai
import os
from datetime import datetime, timedelta
import json
from googlecalendar.views import create_google_calendar_event, delete_google_calendar_event, update_google_calendar_event, search_google_calendar_events
from zoneinfo import ZoneInfo

# Set your OpenAI API key here
openai.api_key = os.getenv('OPEN_AI_KEY')

SGT = ZoneInfo("Asia/Singapore")

def find_best_matching_event(events, user_description):
    if not events:
        return None
    
    prompt = f"""Given the following list of calendar events and a user's description, 
    determine which event best matches the user's description. Return the index of the best matching event.
    If no event matches well, return -1.

    Events:
    {json.dumps(events, indent=2)}

    User's description: {user_description}

    Best matching event index:"""

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10
    )

    try:
        index = int(response.choices[0].message.content.strip())
        return events[index] if 0 <= index < len(events) else None
    except (ValueError, IndexError):
        return None

def parse_date_range(date_description):
    today = datetime.now(SGT).replace(hour=0, minute=0, second=0, microsecond=0)
    
    if "tomorrow" in date_description.lower():
        start_date = today + timedelta(days=1)
        end_date = start_date + timedelta(days=1)
    elif "next week" in date_description.lower():
        start_date = today + timedelta(days=(7 - today.weekday()))
        end_date = start_date + timedelta(days=7)
    else:
        # Default to today if no specific time frame is mentioned
        start_date = today
        end_date = today + timedelta(days=1)
    
    return start_date, end_date

def get_events(date_description):
    start_date, end_date = parse_date_range(date_description)
    return search_google_calendar_events(start_date, end_date)

@api_view(['POST'])
def get_response(request):
    conversation = request.data.get('messages', [])

    timenow = datetime.now(SGT)
    daynow = timenow.strftime("%A")

    system_message = f"""
    You are an AI assistant specialized in managing Google Calendar events. Your primary functions include adding, retrieving, modifying, and deleting calendar events based on user requests. Aim for efficiency and directness in your responses.

    Current date and time: {timenow}
    Current day: {daynow}

    Key Responsibilities:
    1. Interpret user intentions accurately (Add, Retrieve, Modify, or Delete events).
    2. Extract relevant event details from user input.
    3. Handle date and time information precisely, including relative terms like "tomorrow" or "next week".
    4. Take immediate action when sufficient information is provided.
    5. Provide clear, concise responses.

    Guidelines:
    - For adding events: If the user provides an event name, date, and start time, assume a one-hour duration unless specified otherwise. Proceed to add the event immediately.
    - For retrieving events: If a specific date or range is mentioned, proceed to fetch the events without asking for confirmation.
    - For modifying events: If the user specifies the event to be changed and provides new details, proceed with the update.
    - For deleting events: If the user clearly identifies an event to be removed, proceed with the deletion after a brief confirmation.
    - Only ask for clarification if critical information is missing or ambiguous.
    - After each action, briefly confirm what was done and ask if anything else is needed.

    Remember: You don't have direct access to the calendar. Use the provided functions to interact with the calendar data. Always err on the side of action rather than excessive confirmation.
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
            "summary": {"type": "string", "description": "A brief description of the event"},
            "start": {"type": "string", "description": "Start date and time of the event in ISO 8601 format"},
            "end": {"type": "string", "description": "End date and time of the event in ISO 8601 format"}
        },
        "required": ["summary", "start", "end"]
    }

    search_and_delete_event_schema = {
        "type": "object",
        "properties": {
            "description": {"type": "string", "description": "Description of the event to be deleted"},
            "date_range": {"type": "string", "description": "Date or date range for the event (e.g., 'tomorrow', 'next week')"}
        },
        "required": ["description", "date_range"]
    }

    search_and_update_event_schema = {
        "type": "object",
        "properties": {
            "description": {"type": "string", "description": "Description of the event to be updated"},
            "date_range": {"type": "string", "description": "Date or date range for the event (e.g., 'tomorrow', 'next week')"},
            "new_summary": {"type": "string", "description": "Updated summary of the event"},
            "new_start": {"type": "string", "description": "Updated start date and time of the event in ISO 8601 format"},
            "new_end": {"type": "string", "description": "Updated end date and time of the event in ISO 8601 format"}
        },
        "required": ["description", "date_range", "new_summary", "new_start", "new_end"]
    }

    get_events_schema = {
        "type": "object",
        "properties": {
            "date_range": {"type": "string", "description": "Date or date range for which to retrieve events (e.g., 'tomorrow', 'next week')"}
        },
        "required": ["date_range"]
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
                },
                {
                    "type": "function",
                    "function": {
                        "name": "search_and_delete_event", 
                        "description": "Search for and delete an event from the user's Google Calendar",
                        "parameters": search_and_delete_event_schema
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "search_and_update_event", 
                        "description": "Search for and update an existing event in the user's Google Calendar",
                        "parameters": search_and_update_event_schema
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_events", 
                        "description": "Retrieve events from the user's Google Calendar for a specific date or date range",
                        "parameters": get_events_schema
                    }
                }
            ]
        )

        assistant_message = response.choices[0].message

        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                if function_name == "create_event":
                    print("create_event")
                    start_time = datetime.fromisoformat(function_args['start']).replace(tzinfo=SGT)
                    end_time = datetime.fromisoformat(function_args['end']).replace(tzinfo=SGT)
                    result = create_google_calendar_event(
                        function_args['summary'],
                        start_time.isoformat(),
                        end_time.isoformat()
                    )
                elif function_name == "search_and_delete_event":
                    print("search_and_delete_event")
                    search_result = get_events(function_args['date_range'])
                    
                    if 'events' in search_result and search_result['events']:
                        matching_event = find_best_matching_event(search_result['events'], function_args['description'])
                        
                        if matching_event:
                            result = delete_google_calendar_event(matching_event['id'])
                        else:
                            result = {"error": "No matching event found"}
                    else:
                        result = {"error": "No events found in the specified date range"}
                elif function_name == "search_and_update_event":
                    print("search_and_update_event")
                    search_result = get_events(function_args['date_range'])
                    
                    if 'events' in search_result and search_result['events']:
                        matching_event = find_best_matching_event(search_result['events'], function_args['description'])
                        
                        if matching_event:
                            new_start = datetime.fromisoformat(function_args['new_start']).replace(tzinfo=SGT)
                            new_end = datetime.fromisoformat(function_args['new_end']).replace(tzinfo=SGT)
                            result = update_google_calendar_event(
                                matching_event['id'],
                                function_args['new_summary'],
                                new_start.isoformat(),
                                new_end.isoformat()
                            )
                        else:
                            result = {"error": "No matching event found"}
                    else:
                        result = {"error": "No events found in the specified date range"}
                elif function_name == "get_events":
                    print("get_events")
                    result = get_events(function_args['date_range'])
                else: 
                    print("no function used")
                
                formatted_messages.append({"role": "function", "name": function_name, "content": json.dumps(result)})
                
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
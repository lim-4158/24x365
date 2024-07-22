import os
import json
import datetime
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.views.decorators.http import require_GET
from .models import User

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
FRONTEND_URL = os.getenv('FRONTEND_URL')
BACKEND_URL = os.getenv('BACKEND_URL')

SCOPES = ["https://www.googleapis.com/auth/calendar"]
REDIRECT_URI = f"{BACKEND_URL}googlecalendar/oauth2callback"
TOKEN_PATH = os.path.join(os.path.dirname(__file__), "token.json")

# Set the environment variable to allow HTTP connections
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

def get_google_credentials():
    credentials_json = os.getenv('GOOGLE_CREDENTIALS')
    if not credentials_json:
        raise ValueError("GOOGLE_CREDENTIALS environment variable is not set")
    return json.loads(credentials_json)

def google_calendar_events(request):
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        print("Loaded credentials from token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds_info = get_google_credentials()
            flow = Flow.from_client_config(creds_info, SCOPES)
            flow.redirect_uri = REDIRECT_URI
            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent'  # Force re-consent to get a refresh token
            )
            request.session['state'] = state
            print(f"State set in session: {state}")  # Debugging line
            return HttpResponseRedirect(authorization_url)

    try:
        service = build("calendar", "v3", credentials=creds)

        # Extract user info and save to the database
        user_info_service = build('oauth2', 'v2', credentials=creds)
        user_info = user_info_service.userinfo().get().execute()
        email = user_info['email']
        username = user_info.get('name', '')

        print(f"User info: {user_info}")  # Debugging line

        # Check if user exists in the database
        user, created = User.objects.get_or_create(email=email)
        if created:
            user.username = username
            user.save()
            print(f"User created: {username} ({email})")
        else:
            print(f"User exists: {username} ({email})")

        now = datetime.datetime.now().isoformat() + "Z"
        events_result = service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=10, singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        events_list = [
            {"start": event["start"].get("dateTime", event["start"].get("date")), "summary": event["summary"]}
            for event in events
        ]

        # Store events in session or any other storage to be accessed by the React app
        request.session['events'] = events_list

        # Redirect to React app route for displaying events
        return HttpResponseRedirect(f"{FRONTEND_URL}usercalendar")  # Adjust URL to your React app

    except HttpError as error:
        return JsonResponse({"error": str(error)}, status=500)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")  # Debugging line
        return JsonResponse({"error": str(e)}, status=500)

def create_google_calendar_event(summary, start, end):
    creds = None

    print("sheesh")
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        return {"error": "Credentials are not valid or expired."}

    try:
        service = build("calendar", "v3", credentials=creds)

        event = {
            'summary': summary,
            'start': {
                'dateTime': start,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end,
                'timeZone': 'UTC',
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        return {"message": "Event created successfully", "event": event}

    except HttpError as error:
        return {"error": str(error)}

@csrf_exempt
def create_event(request):
    if request.method == "POST":
        data = json.loads(request.body)
        result = create_google_calendar_event(data['summary'], data['start'], data['end'])
        print(data['start'])
        if 'error' in result:
            return JsonResponse(result, status=500)
        return JsonResponse(result)
    return JsonResponse({"error": "Invalid request method"}, status=400)

def oauth2callback(request):
    state = request.session.get('state')
    if not state:
        return JsonResponse({"error": "State parameter missing in session. Reauthenticate required."}, status=400)

    print(f"State retrieved from session: {state}")  # Debugging line

    creds_info = get_google_credentials()
    flow = Flow.from_client_config(creds_info, SCOPES, state=state)
    flow.redirect_uri = REDIRECT_URI

    authorization_response = request.build_absolute_uri()
    print(f"Authorization response: {authorization_response}")  # Debugging line

    try:
        flow.fetch_token(authorization_response=authorization_response)
        creds = flow.credentials
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
        return redirect('google-calendar-events')
    except Exception as e:
        print(f"An error occurred: {e}")
        return JsonResponse({"error": str(e)}, status=500)

def force_reauthentication(request):
    if os.path.exists(TOKEN_PATH):
        os.remove(TOKEN_PATH)
    return redirect('google-calendar-events')

@require_GET
def get_user_calendar_id(request):
    try:
        # Load credentials from token.json
        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        else:
            return JsonResponse({"error": "No valid credentials found."}, status=401)

        # Build the Google Calendar service
        service = build("calendar", "v3", credentials=creds)

        # Fetch the list of calendars
        calendar_list = service.calendarList().list().execute()

        # Get the primary calendar ID
        primary_calendar_id = None
        for calendar_entry in calendar_list.get('items', []):
            if calendar_entry.get('primary'):
                primary_calendar_id = calendar_entry.get('id')
                break

        if not primary_calendar_id:
            return JsonResponse({"error": "No primary calendar found."}, status=404)

        return JsonResponse({"calendar_id": primary_calendar_id})

    except HttpError as error:
        return JsonResponse({"error": str(error)}, status=500)
    
def check_google_auth(request):
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        if creds and creds.valid:
            return JsonResponse({"authenticated": True})
        else:
            return JsonResponse({"authenticated": False})
    else:
        return JsonResponse({"authenticated": False})
    
@csrf_exempt
def delete_google_calendar_event(event_id):
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        return {"error": "Credentials are not valid or expired."}

    try:
        service = build("calendar", "v3", credentials=creds)
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        return {"message": "Event deleted successfully"}

    except HttpError as error:
        return {"error": str(error)}
    
@csrf_exempt
def delete_event(request):
    if request.method == "POST":
        data = json.loads(request.body)
        event_id = data.get('event_id')
        if not event_id:
            return JsonResponse({"error": "event_id is required"}, status=400)
        result = delete_google_calendar_event(event_id)
        if 'error' in result:
            return JsonResponse(result, status=500)
        return JsonResponse(result)
    return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def update_google_calendar_event(event_id, summary, start, end):
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        return {"error": "Credentials are not valid or expired."}

    try:
        service = build("calendar", "v3", credentials=creds)

        event = service.events().get(calendarId='primary', eventId=event_id).execute()
        event['summary'] = summary
        event['start'] = {
            'dateTime': start,
            'timeZone': 'UTC',
        }
        event['end'] = {
            'dateTime': end,
            'timeZone': 'UTC',
        }

        updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
        return {"message": "Event updated successfully", "event": updated_event}

    except HttpError as error:
        return {"error": str(error)}

@csrf_exempt
def update_event(request):
    if request.method == "POST":
        data = json.loads(request.body)
        event_id = data.get('event_id')
        summary = data.get('summary')
        start = data.get('start')
        end = data.get('end')
        
        if not event_id or not summary or not start or not end:
            return JsonResponse({"error": "All fields (event_id, summary, start, end) are required"}, status=400)
        
        result = update_google_calendar_event(event_id, summary, start, end)
        if 'error' in result:
            return JsonResponse(result, status=500)
        return JsonResponse(result)
    return JsonResponse({"error": "Invalid request method"}, status=400)


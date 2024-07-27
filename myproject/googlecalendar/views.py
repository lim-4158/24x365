import os
import json
import datetime
from time import timezone
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
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import User, Event, GoogleAuthRecord

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
    
    creds = json.loads(credentials_json)
    try:
        credentials = Credentials.from_authorized_user_info(creds, SCOPES)
        # Check if the token is expired and refresh if needed
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            # Save the refreshed credentials back to the environment or update your storage
            os.environ['GOOGLE_CREDENTIALS'] = credentials.to_json()
            return credentials
    except:
        return creds

def update_calendar_events():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

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
                prompt='consent'
            )
            return {'redirect': authorization_url, 'state': state}

    try:
        service = build("calendar", "v3", credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=10, singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        # Clear existing events before updating
        Event.objects.all().delete()

        # Save new events to the database
        for event in events:
            Event.objects.create(
                summary=event.get('summary', 'No summary'),
                start=event['start'].get('dateTime', event['start'].get('date')),
                event_id=event['id']  # Save the event_id
            )

        return {'events': list(Event.objects.all().values('start', 'summary', 'event_id'))}

    except HttpError as error:
        return {'error': str(error)}


def list_events(request):
    result = update_calendar_events()
    if 'redirect' in result:
        request.session['state'] = result['state']
        return HttpResponseRedirect(result['redirect'])
    
    if 'error' in result:
        return JsonResponse({"error": result['error']}, status=500)

    return JsonResponse({"events": result['events']})

def google_calendar_events(request):
    creds = None
    # Check if the token file exists and load credentials
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # If credentials are not valid, handle refresh or re-authentication
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
                prompt='consent'
            )
            request.session['state'] = state
            return HttpResponseRedirect(authorization_url)

    try:
        # Build the Google Calendar service
        service = build("calendar", "v3", credentials=creds)
        now = datetime.datetime.now().isoformat() + "Z"
        events_result = service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=10, singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        # Clear existing events before updating
        Event.objects.all().delete()

        for event in events:
            Event.objects.create(
                summary=event.get('summary', 'No summary'),
                start=event['start'].get('dateTime', event['start'].get('date'))
            )

        return HttpResponseRedirect(f'{FRONTEND_URL}main')

    except HttpError as error:
        return JsonResponse({"error": str(error)}, status=500)

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
        elif creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                with open(TOKEN_PATH, 'w') as token_file:
                    token_file.write(creds.to_json())
                return JsonResponse({"authenticated": True})
            except Exception as e:
                return JsonResponse({"authenticated": False, "error": str(e)}, status=500)
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
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        event_ids = data.get('event_ids')
        if not event_ids:
            return JsonResponse({"error": "event_ids are required"}, status=400)

        results = []
        for event_id in event_ids:
            result = delete_google_calendar_event(event_id)
            results.append(result)

        if any('error' in result for result in results):
            return JsonResponse({"results": results}, status=500)
        
        return JsonResponse({"results": results})

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

@require_POST
def mark_event_done(request):
    event_id = request.POST.get('eventId')
    if not event_id:
        return JsonResponse({'error': 'No event ID provided'}, status=400)
    
    try:
        event = Event.objects.get(id=event_id)
        event.done = True  # Assuming you have a 'done' field in your model
        event.save()
        return JsonResponse({'success': 'Event marked as done'})
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)
    
def search_google_calendar_events(start_date, end_date):
    print("search_google_calendar_events")
    print(start_date)
    print(end_date)
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        print("Credentials are not valid or expired.")
        return {"error": "Credentials are not valid or expired."}

    try:
        service = build("calendar", "v3", credentials=creds)
        
        # Ensure start_date and end_date are datetime objects
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)
        
        # Convert to UTC and then to RFC3339 format
        time_min = start_date.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        time_max = end_date.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        events_result = service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        return {
            "events": [
                {
                    "id": event['id'],
                    "summary": event['summary'],
                    "start": event["start"].get("dateTime", event["start"].get("date")),
                    "end": event["end"].get("dateTime", event["end"].get("date"))
                }
                for event in events
            ]
        }

    except HttpError as error:
        print(f"An error occurred: {error}")
        return {"error": str(error)}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": f"An unexpected error occurred: {str(e)}"}
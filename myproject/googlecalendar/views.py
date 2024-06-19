import os
import json
import datetime
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]
REDIRECT_URI = "http://localhost:8000/googlecalendar/oauth2callback"
CREDS_PATH = os.path.join(os.path.dirname(__file__), "credentials.json")
TOKEN_PATH = os.path.join(os.path.dirname(__file__), "token.json")

# Set the environment variable to allow HTTP connections
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

def google_calendar_events(request):
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        print("Loaded credentials from token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_secrets_file(CREDS_PATH, SCOPES)
            flow.redirect_uri = REDIRECT_URI
            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true'
            )
            request.session['state'] = state
            return HttpResponseRedirect(authorization_url)

    try:
        service = build("calendar", "v3", credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + "Z"
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

        return JsonResponse(events_list, safe=False)

    except HttpError as error:
        return JsonResponse({"error": str(error)}, status=500)

@csrf_exempt
def create_event(request):
    if request.method == "POST":
        creds = None

        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

        if not creds or not creds.valid:
            return JsonResponse({"error": "Credentials are not valid or expired."}, status=401)

        try:
            service = build("calendar", "v3", credentials=creds)
            data = json.loads(request.body)

            # Print event data for debugging
            print("Event Data:", json.dumps(data, indent=2))

            event = {
                'summary': data['summary'],
                'start': {
                    'dateTime': data['start'],
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': data['end'],
                    'timeZone': 'UTC',
                },
            }

            # Print the formatted event object
            print("Formatted Event:", json.dumps(event, indent=2))

            event = service.events().insert(calendarId='primary', body=event).execute()
            return JsonResponse({"message": "Event created successfully", "event": event})

        except HttpError as error:
            print(f"HttpError: {error}")
            return JsonResponse({"error": str(error)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

def oauth2callback(request):
    state = request.session['state']
    flow = Flow.from_client_secrets_file(
        CREDS_PATH, SCOPES, state=state)
    flow.redirect_uri = REDIRECT_URI

    authorization_response = request.build_absolute_uri()
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

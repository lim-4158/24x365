from django.urls import path
from .views import google_calendar_events, oauth2callback, create_event, force_reauthentication, get_user_calendar_id, check_google_auth

urlpatterns = [
    path("events", google_calendar_events, name="google-calendar-events"),
    path("googlecalendar/oauth2callback", oauth2callback, name="oauth2callback"),
    path("calendar/createevents", create_event, name="create-event"),
    path("calendar/force_reauth", force_reauthentication, name="force-reauthentication"),
    path("calendar/displayevents", get_user_calendar_id, name="display-events"),
    path("calendar/checkauth", check_google_auth, name="check-auth")
]
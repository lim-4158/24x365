from django.urls import path
from .views import google_calendar_events, oauth2callback, create_event, force_reauthentication

urlpatterns = [
    path("calendar/events/", google_calendar_events, name="google-calendar-events"),
    path("googlecalendar/oauth2callback", oauth2callback, name="oauth2callback"),
    path("calendar/events/create/", create_event, name="create-event"),
    path("googlecalendar/force_reauth", force_reauthentication, name="force-reauthentication"),
]
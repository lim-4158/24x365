from django.urls import path
from .views import google_calendar_events, oauth2callback, create_event, force_reauthentication, get_user_calendar_id, check_google_auth, delete_event, update_event

urlpatterns = [
    path("events", google_calendar_events, name="google-calendar-events"),
    path("oauth2callback", oauth2callback, name="oauth2callback"),
    path("create_events", create_event, name="create-event"),
    path("force_reauth", force_reauthentication, name="force-reauthentication"),
    path("display_events", get_user_calendar_id, name="display-events"),
    path("check_auth", check_google_auth, name="check-auth"),
    path("delete_events", delete_event, name="delete-event"),
    path("update_events", update_event, name="update-event")
]
import os
import json
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from unittest.mock import mock_open, patch, MagicMock
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

class GoogleCalendarTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_events_url = reverse('list-event')
        self.google_calendar_events_url = reverse('google-calendar-events')
        self.create_event_url = reverse('create-event')
        self.oauth2callback_url = reverse('oauth2callback')
        self.delete_event_url = reverse('delete-event')
        self.update_event_url = reverse('update-event')
        self.mark_event_done_url = reverse('mark-event-done')
        self.get_user_calendar_id_url = reverse('display-events')
        self.check_google_auth_url = reverse('check-auth')

    @patch('googlecalendar.views.update_calendar_events')
    def test_list_events(self, mock_update_calendar_events):
        mock_update_calendar_events.return_value = {'events': []}
        response = self.client.get(self.list_events_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"events": []})

    @patch('googlecalendar.views.create_google_calendar_event')
    def test_create_event(self, mock_create_google_calendar_event):
        mock_create_google_calendar_event.return_value = {"message": "Event created successfully"}
        data = {
            'summary': 'Test Event',
            'start': '2024-07-24T10:00:00Z',
            'end': '2024-07-24T12:00:00Z'
        }
        response = self.client.post(self.create_event_url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Event created successfully"})

    @patch('googlecalendar.views.update_google_calendar_event')
    def test_update_event(self, mock_update_google_calendar_event):
        mock_update_google_calendar_event.return_value = {"message": "Event updated successfully"}
        data = {
            'event_id': '1234',
            'summary': 'Updated Event',
            'start': '2024-07-24T10:00:00Z',
            'end': '2024-07-24T12:00:00Z'
        }
        response = self.client.post(self.update_event_url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Event updated successfully"})

    @patch('googlecalendar.views.delete_google_calendar_event')
    def test_delete_event(self, mock_delete_google_calendar_event):
        mock_delete_google_calendar_event.return_value = {"message": "Event deleted successfully"}
        data = {
            'event_ids': ['1234']
        }
        response = self.client.post(self.delete_event_url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"results": [{"message": "Event deleted successfully"}]})

    @patch('googlecalendar.views.build')
    @patch('googlecalendar.views.Credentials.from_authorized_user_file')
    @patch('googlecalendar.views.get_google_credentials')
    def test_google_calendar_events(self, mock_get_google_credentials, mock_from_authorized_user_file, mock_build):
        # Mock credentials and service
        mock_creds = MagicMock(spec=Credentials)
        mock_from_authorized_user_file.return_value = mock_creds
        mock_service = mock_build.return_value
        mock_events = {
            'items': [
                {
                    'summary': 'Test Event',
                    'start': {'dateTime': '2024-07-24T10:00:00Z'},
                    'id': '1234'
                }
            ]
        }
        mock_service.events.return_value.list.return_value.execute.return_value = mock_events

        # Simulate the existence of a valid token
        with patch('builtins.open', mock_open(read_data=json.dumps({'token': 'mock_token'}))):
            response = self.client.get(self.google_calendar_events_url)
            self.assertEqual(response.status_code, 302)  # Assuming redirect happens to the frontend URL

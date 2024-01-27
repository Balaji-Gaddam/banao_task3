from googleapiclient.discovery import build
from datetime import datetime, timedelta,date
import os.path
import pytz
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.utils import timezone


def create_calendar_event(doctor_email, patient_name, appointment_date, start_time, end_time, specialty):
    # Load the credentials file for your Google Cloud project
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    creds = None
  
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "C:\\Users\\gadda\\Desktop\\projects\\task4\\myproject\\client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    start_datetime = datetime.strptime(f"{appointment_date} {start_time}", "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.utc)
    end_datetime = datetime.strptime(f"{appointment_date} {end_time}", "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.utc)
    
    # Convert datetime objects to ISO 8601 format strings
    start_datetime_str = start_datetime.isoformat()
    end_datetime_str = end_datetime.isoformat()
    
    # Build the Google Calendar API service
    service = build('calendar', 'v3', credentials=creds)
    
    # Construct the event description including patient's name, doctor's name, and specialty
    event_description = f'Appointment  {patient_name}, Doctor: {doctor_email}, Specialty: {specialty}'
    
    event = {
        'summary': f'Appointment with {patient_name}',
        'description': event_description,
        'start' : {
            'dateTime': start_datetime_str,
            'timeZone': 'UTC',  # Set to your desired timezone
        },
        'end' : {
            'dateTime': end_datetime_str,
            'timeZone': 'UTC',  # Set to your desired timezone
        },
        'recurrence': [],
        'attendees': [{'email': doctor_email}],
        'reminders': {},
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
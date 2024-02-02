import pickle
import os.path
from icalendar import Calendar, Event
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class GCalendar:
    def __init__(self, title, event_amount):
        self.title = title                         # The name of the calendar
        self.event_amount = event_amount           # How many events to load if update smaller than full sync
        self.credentials_file = 'credentials.json' # You should get this from the Google API Console (https://console.developers.google.com/)
        self.pickle = 'token.pickle'               # This file is automatically generated by the Google API Python Integration
        self.scopes = ['https://www.googleapis.com/auth/calendar'] # Scope of your API
        self.service = self._setup_service()        # Google API Service Object
        self.id = self.get_calendar_id()           # Google Calendar ID (not the name)
        self.events = None

    def _end_with_msg(msg):
        print(msg)
        exit()

    # Setup Google API Service Object to interact with Google Calendar
    def _setup_service(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.scopes)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build('calendar', 'v3', credentials=creds)

    # Get the ID of the calendar with the name self.title
    def get_calendar_id(self):
        print('>> Reading Google Calendar "%s"' % self.title)
        calendars_result = self.service.calendarList().list().execute()
        calendars = calendars_result.get('items', [])

        if not calendars:
            self._end_with_msg('[!] - No calendars found!')
        
        # Look out for the ominous target calendar
        for calendar in calendars:
            if calendar['summary'] == self.title:
                return calendar['id']
        
        if self.id is None:
            self._end_with_msg("[!] - The calendar could not be found. Please make sure it exists.")

    # Retrieve events from Google Calendar
    def load_events(self, full_sync):
        # 'Z' at the end means UTC time
        now = datetime.utcnow().isoformat() + 'Z'
        
        print('>> Getting everything there is') if full_sync else print('>> Getting list of', self.event_amount,'upcoming events')

        events_result = self.service.events().list(calendarId = self.id, 
                timeMin=now,
                maxResults = self.event_amount, 
                singleEvents=True,
                orderBy='startTime').execute()
        self.events = events_result.get('items', [])

    # Create new event in Google Calendar
    def create_event(self, event):
        start = event[4].isoformat()
        end = event[5].isoformat()
        try:
            _ = self.service.events().insert(calendarId = self.id,
            body={
                "summary": event[1],
                "location": event[2],
                "description": event[3] + " # [Created:" + event[0].strftime("%d-%m-%Y %H:%M:%S") + "] # [Pulled: " + datetime.now().strftime("%d-%m-%Y %H:%M:%S") + "]",
                "start": {"dateTime": start, "timeZone": 'Europe/Berlin'},
                "end": {"dateTime": end, "timeZone": 'Europe/Berlin'},
            }).execute()
        except:
            self._end_with_msg("[!] - Can't retrieve events - Google API is busy right now")

    # Delete existing event from Google Calendar
    def delete_google_event(self, event_id):
        try:
            self.service.events().delete(calendarId=self.id, eventId=event_id).execute()
        except:
            self._end_with_msg("[!] - Can't delete events - Google API is busy right now")

    # Mark existing event in Google Calendar as outdated (seems better to me than outright deleting it)
    def outdate_event(self, event_id, keep_history=True):
        if keep_history:
            try:
                event = self.service.events().get(calendarId=self.id, eventId=event_id).execute()
                description = event['description']
                if "OUTDATED" in description:
                    return
                event['description'] += " # OUTDATED"
                self.service.events().update(calendarId=self.id, eventId=event_id, body=event).execute()
            except:
                # Maybe the event was deleted in the meantime, so we don't need to update it
                pass
        else:
            self.delete_google_event(event_id)
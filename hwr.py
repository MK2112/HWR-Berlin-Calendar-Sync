import sys
import time
import argparse
import datetime
from datetime import datetime
from modules.ics_file import ICS_File
from modules.gcalendar import GCalendar

## Settings ##
# -----------------------
# ICS file link - CHANGE THIS FOR YOUR OWN CLASSES 
# Copy the link behind 'Stundenplan herunterladen (ICS)' on the HWR class schedule page
hwr_ics_link = 'https://moodle.hwr-berlin.de/fb2-stundenplan/download.php?doctype=.ics&url=./fb2-stundenplaene/informatik/semester6/kursb'
# Google Calendar name - CLASS SCHEDULE WILL BE IMPORTED TO/UPDATED HERE
google_calendar_name = 'HWR'
# How many events to update into the future (to not stress the GCal API)
update_depth = 50
# -----------------------
## END Settings ##

# Update Schedule (in seconds, to not stress both APIs)
scheduled_seconds = 8 * 60 ** 2

# Events have same start and end time and physical location
# ICS: [DTSTAMP, SUMMARY, LOCATION, DESCRIPTION, DTSTART, DTEND]
def identical_events(ics_event: list, cal_event: dict) -> bool:
    # Compare ICS and Google Calendar events for equality, robustly.
    # Handles whitespace, missing fields, and minor formatting differences.
    # (2021-01-19T17:00:00+01:00 -> 2021-01-19 17:00:00)
    try:
        # Parse calendar event times
        start_cal = datetime.fromisoformat(cal_event['start'].get('dateTime', cal_event['start'].get('date'))).replace(tzinfo=None)
        end_cal = datetime.fromisoformat(cal_event['end'].get('dateTime', cal_event['end'].get('date'))).replace(tzinfo=None)
        # Parse ICS event times
        start_ics = ics_event[4]
        end_ics = ics_event[5]
        # Compare summary (case-insensitive, strip whitespace)
        summary_cal = cal_event.get('summary', '').strip().lower()
        summary_ics = str(ics_event[1]).strip().lower() if len(ics_event) > 1 else ''
        # Compare location (case-insensitive, strip whitespace)
        location_cal = cal_event.get('location', '').strip().lower()
        location_ics = str(ics_event[2]).strip().lower() if len(ics_event) > 2 else ''
        # Compare times
        if start_cal != start_ics or end_cal != end_ics:
            return False
        # Compare summary
        if summary_cal != summary_ics:
            return False
        # If location exists in both, compare
        if location_cal and location_ics and location_cal != location_ics:
            return False
        return True
    except Exception as e:
        print(f"[identical_events] Warning: error comparing events: {e}")
        return False


def run(args: argparse.Namespace):
   hwr_ics = ICS_File(url=hwr_ics_link)
   hwr_cal = GCalendar(title=google_calendar_name, event_amount=update_depth)
   hwr_cal.load_events(not args.update)

   # Find ICS events not present in calendar
   event_index = 0
   for ics_event in hwr_ics.events:
      event_index += 1
      found = False
      for cal_event in hwr_cal.events:
         if identical_events(ics_event, cal_event):
            found = True
            break
      if not found and event_index <= update_depth and ics_event[4] >= datetime.now():
         hwr_cal.create_event(ics_event)

   # Update events in calendar that are not in ics
   # Keep them but append their description with # [Deleted: <date>]
   for cal_event in hwr_cal.events:
      found = False
      for ics_event in hwr_ics.events:
         if identical_events(ics_event, cal_event):
            found = True
            break
      if not found:
         # Pass the event ID to outdate_event, not the whole event
         hwr_cal.outdate_event(cal_event['id'])
   print('>> Update complete\n')


if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('--update', help=f'Update only the next {update_depth} events', action='store_true')
   args = parser.parse_args()
   # Scheduled loop
   while True:
      run(args)
      print(f'<< Sleeping for {scheduled_seconds / 60.0 / 60.0} hours...\n')
      time.sleep(scheduled_seconds)
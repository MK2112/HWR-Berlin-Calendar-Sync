import sys
import time
import datetime
from datetime import datetime
from modules.ics_file import ICS_File
from modules.gcalendar import GCalendar

## User Settings ##
# ------------------------------------------------------------

# ICS file link - CHANGE THIS FOR YOUR OWN CLASSES
hwr_ics_link = 'https://moodle.hwr-berlin.de/fb2-stundenplan/download.php?doctype=.ics&url=./fb2-stundenplaene/informatik/semester6/kursb'
# Google Calendar name - CLASS SCHEDULE WILL BE IMPORTED/UPDATED TO HERE
google_calendar_name = 'HWR'
# Update Schedule in seconds
scheduled_seconds = 28800
# How many events to update into the future
update_depth = 50

# ------------------------------------------------------------

# Events have same start and end time and physical location
# ICS: [DTSTAMP, SUMMARY, LOCATION, DESCRIPTION, DTSTART, DTEND]
def identical_events(ics_event, cal_event):
   # 2021-01-19T17:00:00+01:00 -> 2021-01-19 17:00:00
   start_cal = datetime.fromisoformat(cal_event['start'].get('dateTime', cal_event['start'].get('date'))).replace(tzinfo=None)
   end_cal   = datetime.fromisoformat(cal_event['end'].get('dateTime', cal_event['end'].get('date'))).replace(tzinfo=None)
   start_ics = ics_event[4]
   end_ics = ics_event[5]
   summary_cal = cal_event['summary']
   summary_ics = ics_event[1]

   if 'location' in cal_event:
      location_cal = cal_event['location']
      location_ics = ics_event[2]

      if start_cal == start_ics and \
         end_cal == end_ics and \
         location_cal == location_ics and \
         summary_cal == summary_ics:
         return True
   else:
      if start_cal == start_ics and \
         end_cal == end_ics and \
         summary_cal == summary_ics:
         return True
   return False


def main():
   if len(sys.argv) > 1 and sys.argv[1] == "update":
      full_sync = False
   else:
      full_sync = True

   hwr_ics = ICS_File(url=hwr_ics_link)
   hwr_cal = GCalendar(title=google_calendar_name, event_amount=update_depth)
   hwr_cal.load_events(full_sync)

   # Find ICS events not present in calendar
   counter = 0
   for ics_event in hwr_ics.events:
      counter += 1
      found = False
      for cal_event in hwr_cal.events:
         if identical_events(ics_event, cal_event):
            found = True
            break
      if not found and counter <= update_depth and ics_event[4] >= datetime.now():
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
         hwr_cal.outdate_event(cal_event)
   print('>> Update complete\n')

if __name__ == '__main__':
   while True:
      main()
      print(f'<< Sleeping for {scheduled_seconds / 60.0 / 60.0} hours...\n')
      time.sleep(scheduled_seconds)
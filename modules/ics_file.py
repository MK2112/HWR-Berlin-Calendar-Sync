from datetime import datetime
import requests

class ICS_File:
   def __init__(self, url):
      self.url = url
      self.events = self.get_ics(url)

   # Events look like [DTSTAMP, SUMMARY, LOCATION, DESCRIPTION, DTSTART, DTEND]
   def get_ics(self, url):
      # Read plain .ics data from the url
      data = requests.get(url).text.split("\n")
      active = False
      events = []
      current_event = []
      for line in data:
         if line.startswith("BEGIN:VEVENT"):
            active = True
            continue
         if line.startswith("END:VEVENT"):
            active = False
            events.append(current_event)
            current_event = []
            continue
         if active:
            if line.startswith("SUMMARY:") or line.startswith("LOCATION:") or line.startswith("DESCRIPTION:"):
               current_event.append(self.pretty_print(line[line.find(':')+1:-1]))
            elif line.startswith("DTSTAMP:") or line.startswith("DTSTART;TZID=Europe/Berlin:") or line.startswith("DTEND;TZID=Europe/Berlin:"):
               current_event.append(self.to_datetime(line[line.find(':')+1:-1]))
            elif line.startswith('\t'):
               current_event[-1] = current_event[-1] + self.pretty_print(line[line.find('\t')+1:-1])
               
      return events
   
   # Replace some characters with prettier ones
   def pretty_print(self, text):
      replacements = {
         "\\,": ", ",
         "\\;": "; ",
         "\\n": " # ",
         "\n": " # "
      }
      
      for old, new in replacements.items():
         text = text.replace(old, new)

      return text

   # Convert date and time to datetime object, 20220401T140000Z possible
   def to_datetime(self, time):
      if time.endswith('Z'):
         time = time[:-1]
      return datetime.strptime(time[6:8] + "/" + time[4:6] + "/" + time[2:4] + " " + time[9:11] + ":" + time[11:13] + ":" + time[13:15], '%d/%m/%y %H:%M:%S')
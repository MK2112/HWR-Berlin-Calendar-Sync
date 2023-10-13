from datetime import datetime
import requests

class ics_file:
   def __init__(self, url):
      self.url = url
      self.events = self.get_ics(url)

   # Events look like [DTSTAMP, SUMMARY, LOCATION, DESCRIPTION, DTSTART, DTEND]
   def get_ics(self, url):
      # read the plain .ics data from the url
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

   
   def to_datetime(self, time):
      # 20220401T140000Z possible
      if time.endswith('Z'):
         time = time[:-1]
      date_time_str = time[6:8] + "/" + time[4:6] + "/" + time[2:4] + " " + time[9:11] + ":" + time[11:13] + ":" + time[13:15]
      return datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
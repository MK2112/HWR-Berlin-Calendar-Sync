FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment variables 
# ICS calendar URL to pull from (Copy the link behind 'Stundenplan herunterladen (ICS)')
#ENV HWR_ICS_LINK="https://moodle.hwr-berlin.de/fb2-stundenplan/download.php?doctype=.ics&url=./fb2-stundenplaene/informatik/semester6/kursb"
# GCalendar name to sync to (default: "HWR")
#ENV GOOGLE_CALENDAR_NAME="HWR"
# Sync interval in hours (default: 8)
#ENV UPDATE_INTERVAL_HOURS=8
# Number of events to sync (default: 50)
#ENV UPDATE_DEPTH=50

CMD ["python", "hwr.py", "--update"]

# HWR Berlin - Google Calendar Lecture Sync

Sync lectures of the Berlin School of Economics and Law (HWR Berlin) with your Google Calendar.<br>
This script identifies new or changed calendar entries, updates your Google Calendar, and marks outdated events as such (without deleting them, just to be safe).

## Setup
1. Download/Clone this repository and navigate to it
2. [Download](https://www.python.org/downloads/) and install Python 3.11 or higher
3. Open a terminal in the repository's root folder, install required Python packages like so:<br>`pip install -r requirements.txt`
4. Log into your Google account and create a new,<br>empty Google Calendar; **Remember the calendar title**
5. Make your new calendar visible on your phone using the [Google Calendar Sync Settings](https://calendar.google.com/calendar/u/0/syncselect)
6. Google API Setup:
    - Head to the [Google API Console](https://console.developers.google.com/apis/dashboard), create a new project
    - Enable the `Google Calendar API`
    - Generate a new OAuth 2.0 Client ID
    - Download the json file with your credentials, rename it to `credentials.json` and move it to the project's root folder, next to `hwr.py`
7. Configure `config.yaml`:
    - Open `config.yaml` in a text editor and set:
        - `hwr_ics_link` - URL to the ICS file for your lecture plan
            - Go to the HWR Berlin's Lecture Plan
            - Select your course and semester, then right-click copy the link `Stundenplan herunterladen (ICS)`
        - `google_calendar_name` - Title of your Google Calendar
        - `update_depth` - (Optional) Number of events to sync (default: 50)
        - `update_interval_hours` - (Optional) Sync interval in hours (default: 8)

**Note:** The initial run will prompt you to grant your API project access to your Google Calendar.<br>
This is a one-time process fully controlled by Google. Google may inform you that the API project is not verified, which is true and normal.<br>
The script at no point shares your credentials with anybody but Google.<br>
Refer to the [Google Calendar API documentation](https://developers.google.com/calendar/api/quickstart/python) for more setup details.

## Usage
For a full sync, writing everything there is to the calendar, execute: 
```py
python hwr.py
```
Do this **once, for an initial run**, to populate your calendar with all events.<br>
From there on out, update for a specific number of future events (minimizing API usage and server load) like so:
```py
python hwr.py --update
```

**Note:** The script runs indefinitely, automatically updating the calendar at given intervals.

## Docker

Run in a container with environment variables:
```bash
docker build -t hwr-calendar-sync .
docker run -d \
  -e HWR_ICS_LINK="the-hwr-ics-url" \
  -e GOOGLE_CALENDAR_NAME="HWR" \
  -e UPDATE_INTERVAL_HOURS=8 \
  -e UPDATE_DEPTH=50 \
  -v $(pwd)/credentials.json:/app/credentials.json \
  -v $(pwd)/token.pickle:/app/token.pickle \
  hwr-calendar-sync
```

> **Note:** Run interactively first (`docker run -it ...`) to complete OAuth setup, then switch to detached mode.

## Systemd Service (Linux only)

A service file `hwr-calendar-sync.service` is included. To install:
```bash
# Edit paths in the service file first
sudo cp hwr-calendar-sync.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now hwr-calendar-sync
```

## License
MIT.

## Disclaimer
This script is provided as-is, without any warranties or guarantees.<br>
Users are responsible for ensuring compliance with applicable laws and regulations.

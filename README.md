# HWR Berlin - Google Calendar Lecture Sync

## Overview
This Python script synchronizes events from the lecture plan of the Hochschule für Wirtschaft und Recht Berlin (HWR Berlin) to your Google Calendar. It identifies new events and updates your Calendar accordingly. Outdated events in your Calendar are marked as such (not deleted) for transparency.

## Requirements
1. Download/Clone this project repository and navigate to it
2. Open a terminal in the project directory and install the required Python packages like so: `pip install -r requirements.txt`
3. Log into your Google account and create a new, empty Google Calendar; Note the calendar title
4. Go to the [Google API Console](https://console.developers.google.com/apis/dashboard)
5. Create a new project
6. Enable the Google Calendar API
7. Generate a new OAuth 2.0 Client ID
8. Download the credentials file and save it as `credentials.json` in the project directory
9. Open the `hwr.py` file in a text editor of your choice and modify the 'Settings' section:
    - `hwr_ics_link` - Set the URL to link to the ICS file for your lecture plan
    - `google_calendar_name` - Set the previously noted title of your Google Calendar
    - `scheduled_seconds` - Set the update interval in seconds (default: 28800 = 8 hours)
    - `update_depth` - Set the number of events to update into the future (default: 50)

## Usage
For a full sync, writing everything there is at the source to the calendar, execute: `python hwr.py`<br>
Do this once to populate your calendar with all events.<br>
Then, to update a specific number of future events (minimizing API usage), use: `python hwr.py update`

**Note:** The script runs indefinitely, automatically updating the calendar at given intervals.

## License
This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.

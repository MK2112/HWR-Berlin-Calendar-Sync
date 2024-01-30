# HWR Berlin - Google Calendar Lecture Sync

Synchronize lecture plan events of the Hochschule für Wirtschaft und Recht Berlin (HWR Berlin) with your Google Calendar. Stay organized as it identifies new events, updates your Calendar, and marks outdated events as such (without deletion).

## Setup
1. Download/Clone this project repository and navigate to it
2. [Download](https://www.python.org/downloads/) and install Python 3.11 or higher if not done already
3. Open a terminal in the project's root folder and install required Python packages:<br>`pip install -r requirements.txt`
4. Log into your Google account and create a new,<br>empty Google Calendar; **Remember the calendar title**
5. Make your new calendar visible on phones using the [Google Calendar Sync Settings](https://calendar.google.com/calendar/u/0/syncselect)

6. Google API Setup:
    - Head to the [Google API Console](https://console.developers.google.com/apis/dashboard), create a new project
    - Enable the `Google Calendar API`
    - Generate a new OAuth 2.0 Client ID
    - Download the credentials json file, rename it to `credentials.json` and move it to the project root folder, next to `hwr.py`
11. Configure `hwr.py`:
    - Open `hwr.py` in a text editor and modify the 'Settings' section:
        - `hwr_ics_link` - Set the URL to link to the ICS file for your lecture plan
            - Go to the HWR Berlin's Lecture Plan
            - Select your course and semester, then right-click copy the link `Stundenplan herunterladen (ICS)`
            - Replace the existing link in the `hwr.py` script with the copied link
        - `google_calendar_name` - Set this to the previously noted title of your Google Calendar
        - `scheduled_seconds` - OPTIONAL: Set the update interval in seconds (default: 28800 = 8 hours)
        - `update_depth` - OPTIONAL: Set the number of events to update into the future (default: 50)

**Note:** The initial run will prompt you to grant your API project access to your Google Calendar. This is a one-time process fully controlled by Google. Google may inform you that the API project is not verified, which is normal. Refer to the [Google Calendar API documentation](https://developers.google.com/calendar/api/quickstart/python) for more setup details.

## Usage
For a full sync, writing everything there is to the calendar, execute: `python hwr.py`<br>
Do this **once, for an initial run**, to populate your calendar with all events.<br>
From there on out, update for a specific number of future events (minimizing API usage and server load) like so: `python hwr.py update`

**Note:** The script runs indefinitely, automatically updating the calendar at given intervals.

## License
This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.

### Contributions
Contributions and feedback are welcome. Feel free to open issues or pull requests.

### Disclaimer
This script is provided as-is, without any warranties or guarantees.<br>
Users are responsible for ensuring compliance with applicable laws and regulations.

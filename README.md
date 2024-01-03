# HWR Berlin - Google Calendar Lecture Sync

This tool synchronizes events from the lecture plan of the Hochschule für Wirtschaft und Recht Berlin (HWR Berlin) to your Google Calendar. It identifies new events and updates your Calendar accordingly. Outdated events are marked as such (not deleted).

## Setup
1. Download/Clone this project repository and navigate to it
2. Install Python 3.11 or higher from [python.org](https://www.python.org/downloads/) if you don't have it already
3. Open a terminal in the project directory and install all required Python packages at once like so:<br>`pip install -r requirements.txt`
4. Open your browser, log into your Google account and create a new,<br>empty Google Calendar; **Note the calendar title**
5. Google will not yet make this calendar visible on your phone. Fix this here: [Google Calendar Sync Settings](https://calendar.google.com/calendar/u/0/syncselect)
6. Go to the [Google API Console](https://console.developers.google.com/apis/dashboard) and create a new project
8. Enable the `Google Calendar API`
9. Generate a new OAuth 2.0 Client ID
10. Download the credentials json file, save it as `credentials.json` in the project base directory, next to `hwr.py`
11. Open `hwr.py` in a text editor and modify the 'Settings' section:
    - `hwr_ics_link` - Set the URL to link to the ICS file for your lecture plan
        - Go to the [HWR Berlin Lecture Plan](https://moodle.hwr-berlin.de/fb2-stundenplan/stundenplan.php)
        - Select your course and semester, then right-click copy the link `Stundenplan herunterladen (ICS)`
        - Replace the existing link in the `hwr.py` script with the copied link
    - `google_calendar_name` - Set this to the previously noted title of your Google Calendar
    - `scheduled_seconds` - OPTIONAL: Set the update interval in seconds (default: 28800 = 8 hours)
    - `update_depth` - OPTIONAL: Set the number of events to update into the future (default: 50)

**Note:** On a very first run, you will be asked to grant your API project access to your Google Calendar. This is a one-time process, fully controlled by Google. Google will also inform you that the API project you created is not verified with them. This is normal. The [Google Calendar API](https://developers.google.com/calendar/api/quickstart/python) documentation provides more information on how to set up the API and generate the credentials file.

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

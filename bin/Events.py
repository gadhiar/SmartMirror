"""
Shows basic usage of the Google Calendar API. Creates a Google Calendar API
service object and outputs a list of the next 10 events on the user's calendar.
"""
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
import dateutil.parser

calendar = []


def get_events():
    # Setup the Calendar API
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=5, singleEvents=True,
                                          orderBy='startTime').execute()

    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
    # return events




    # find the date and time and name of each event

    for event in events:
        startTime1 = event['start'].get('dateTime')  # print start time
        endTime1 = event['end'].get('dateTime')  # print end time
        date1 = event['start'].get('dateTime')
        name = event['summary']

        # parse the start and end times into friendly elements and store them
        sT = dateutil.parser.parse(startTime1)
        eT = dateutil.parser.parse(endTime1)
        dT = dateutil.parser.parse(date1)
        startTime = sT.strftime('%I:%M %p')
        endTime = eT.strftime('%I:%M %p')
        dateTime = dT.strftime('%A')

        #give each object it's own array of info values
        temp_array = [dateTime, name, startTime, endTime]
        calendar.append(temp_array)

    return calendar


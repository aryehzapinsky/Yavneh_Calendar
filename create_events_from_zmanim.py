from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage

import datetime

import urllib.request
import json

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Yavneh Davening Calendar'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are
    invalid, the OAuth2 flow is completed to obtain the new
    credentials.

    Returns:
    Credentials, the obtained credentail.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'yavneh_cal_storage.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def create_event(service, cal_id, prayer_name, event_date, stime,
                 etime, location):
    TIMEZONE = 'America/New_York'
    event = {
        'summary': prayer_name,
        'start': {'dateTime': stime, 'timeZone': TIMEZONE},
        'end': {'dateTime': etime, 'timeZone': TIMEZONE},
        'location': location
    }
    e = service.events.insert(calendarId=cal_id, body=event).execute()
    return e


def get_zmanim_from_ou(start_date=None, end_date=None):
    # Friday - dayOfWeek == "5"
    # CANDLE_LIGHTING = candle_lighting
    # FRIDAY_MINCHA = -15 minutes from rounded zmanim.get('sunset')
    # FRIDAY_MINCHA = candle_lighting rounded to nearest 5 minutes

    # Shabbat - dayOfWeek == "6"
    # SOF_ZMAN_KRIYAT_SHEMA = zmanim.get('sof_sman_shema_gra')
    # SHKIYA = zmanim.get('sunset')
    # MINCHA = -30 minutes from Shkiya
    # HAVDALAH = zmanim.get('tzeis_850_degrees')
    # MAARIV = -10 from havdalah

    # Sunday - dayOfweek == "7"
    # MINCHA_MAARIV = -15 minutes from zmanim.get('sunset')
    if start_date == None:
        start_date = datetime.date.today().strftime('%m/%d/%y')
    if end_date == None:
        end_date = start_date

    with urllib.request.urlopen('http://db.ou.org/zmanim/getCalendarData.php?mode=drange&timezone=America/New_York&dateBegin={BEGIN}&dateEnd={END}&lat=40.8139&lng=-73.9624'.format(BEGIN=start_date, END=end_date)) as page:
        days = json.load(page).get('days')

    for day in days:
        day_of_week = day.get('dayOfWeek')
        engDateString = day.get('engDateString') #'10/27/17' --> 'dateTime': '2017-07-01T19:00:00'
        date = engDateString.split('/')
        date = '20{}-{}-{}T'.format(date[2], date[0], date[1])
        zmanim = day.get('zmanim')
        if day_of_week == 5:
            time_before_candle = 15
            candle_lighting = day.get('candle_lighting')
            friday_mincha = candle_lighting

        elif day_of_week == 6:
            sof_zman = zmanim.get('sof_zman_shema_gra')
            shikiya  = zmanim.get('sunset')
            havdalah = zmanim.get('tzeis_850_degrees')

        elif day_of_week == 7:
            shikiya = zmanim.get('sunset')


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    CALENDAR_ID = 'nbhice9ul1r07h5hrqbuvtuqjs@group.calendar.google.com'

    # get_zmanim_from_ou('09/12/17', '12/22/17')
    start_date = '10/21/17'#'09/12/17'
    end_date = '10/29/17' #'12/22/17'
    get_zmanim_from_ou(start_date, end_date)

if __name__ == "__main__":
    main()

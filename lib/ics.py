<<<<<<< HEAD
from datetime import datetime, timedelta, time, date

import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event

from lib.constants import RASP_TPU_BASE, dict_times
from lib.lib import getCurrentLink


def getICS(group, date_, number_):
    soup = BeautifulSoup(requests.get(getCurrentLink(group, date_)).text, "html.parser")
    ics_link = RASP_TPU_BASE + soup.find("div", class_="heading-text").find("a")["href"]
    open("{}.ics".format(group), 'wb').write(requests.get(ics_link, allow_redirects=True).content)

    time_ = dict_times[number_]

    out = list()
    with open("{}.ics".format(group), 'rb') as g:
        cal = Calendar.from_ical(g.read())
        for item in cal.walk():
            if isinstance(item, Event):
                if item['DTSTART'].dt.date() == date_ and time_ is None:
                    new_time = (datetime.combine(date.today(), item['DTSTART'].dt.time()) + timedelta(hours=7)).time()
                    out.append(f"В {new_time}\n{item['DESCRIPTION']}\n\n")

                elif item['DTSTART'].dt.date() == date_ and item['DTSTART'].dt.time() == time_:
                    out.append(f"{item['DESCRIPTION']}\n")
    return out
=======
from datetime import datetime, timedelta, time, date

import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event

from lib.constants import RASP_TPU_BASE, dict_times
from lib.lib import getCurrentLink


def getICS(group, date_, number_):
    soup = BeautifulSoup(requests.get(getCurrentLink(group, date_)).text, "html.parser")
    ics_link = RASP_TPU_BASE + soup.find("div", class_="heading-text").find("a")["href"]
    open("{}.ics".format(group), 'wb').write(requests.get(ics_link, allow_redirects=True).content)

    time_ = dict_times[number_]

    out = list()
    with open("{}.ics".format(group), 'rb') as g:
        cal = Calendar.from_ical(g.read())
        for item in cal.walk():
            if isinstance(item, Event):
                if item['DTSTART'].dt.date() == date_ and time_ is None:
                    new_time = (datetime.combine(date.today(), item['DTSTART'].dt.time()) + timedelta(hours=7)).time()
                    out.append(f"В {new_time}\n{item['DESCRIPTION']}\n\n")

                elif item['DTSTART'].dt.date() == date_ and item['DTSTART'].dt.time() == time_:
                    out.append(f"{item['DESCRIPTION']}\n")
    return out
>>>>>>> 8a05d9861055eb6edb00f5bb2f6d1cb4956d50b8

<<<<<<< HEAD
from datetime import datetime, timedelta, date

from lib.db import getFromDB
from lib.ics import getICS
from lib.returns import dateError, showRasp, numberError, weekError


def rasp(request, group):
    Yandex_DateTime = dict()
    Yandex_Number = list()
    for token in request["request"]["nlu"]["entities"]:
        if token["type"] == "YANDEX.DATETIME":
            if not Yandex_DateTime:
                Yandex_DateTime = token["value"]

        elif token["type"] == "YANDEX.NUMBER":
            Yandex_Number.append(token)

    try:
        if Yandex_DateTime["day_is_relative"]:
            date_ = datetime.now().date() + timedelta(days=Yandex_DateTime["day"])
        else:
            date_ = date(day=Yandex_DateTime["day"], month=Yandex_DateTime["month"], year=datetime.now().year)

    except KeyError:
        return dateError(request)

    Yandex_DateTime_numbers = [val for val in Yandex_DateTime.values() if str(val).isnumeric()]

    Yandex_Number_temp = []
    for val in Yandex_Number:
        if val["value"] in Yandex_DateTime_numbers:
            del Yandex_DateTime_numbers[Yandex_DateTime_numbers.index(val["value"])]
        else:
            Yandex_Number_temp.append(val)

    if len(Yandex_Number_temp) == 1:
        number_ = Yandex_Number_temp[0]["value"] - 1
    elif len(Yandex_Number_temp) == 0:
        number_ = None
    else:
        return numberError(request)

    if date_.isocalendar()[1] == datetime.now().isocalendar()[1]:
        return showRasp(request, getICS(group, date_, number_))

    elif date_.isocalendar()[1] == datetime.now().isocalendar()[1] + 1:
        return showRasp(request, getFromDB(group, date_, number_))

    else:
        return weekError(request)
=======
from datetime import datetime, timedelta, date

from lib.db import getFromDB
from lib.ics import getICS
from lib.returns import dateError, showRasp, numberError, weekError


def rasp(request, group):
    Yandex_DateTime = dict()
    Yandex_Number = list()
    for token in request["request"]["nlu"]["entities"]:
        if token["type"] == "YANDEX.DATETIME":
            if not Yandex_DateTime:
                Yandex_DateTime = token["value"]

        elif token["type"] == "YANDEX.NUMBER":
            Yandex_Number.append(token)

    try:
        if Yandex_DateTime["day_is_relative"]:
            date_ = datetime.now().date() + timedelta(days=Yandex_DateTime["day"])
        else:
            date_ = date(day=Yandex_DateTime["day"], month=Yandex_DateTime["month"], year=datetime.now().year)

    except KeyError:
        return dateError(request)

    Yandex_DateTime_numbers = [val for val in Yandex_DateTime.values() if str(val).isnumeric()]

    Yandex_Number_temp = []
    for val in Yandex_Number:
        if val["value"] in Yandex_DateTime_numbers:
            del Yandex_DateTime_numbers[Yandex_DateTime_numbers.index(val["value"])]
        else:
            Yandex_Number_temp.append(val)

    if len(Yandex_Number_temp) == 1:
        number_ = Yandex_Number_temp[0]["value"] - 1
    elif len(Yandex_Number_temp) == 0:
        number_ = None
    else:
        return numberError(request)

    if date_.isocalendar()[1] == datetime.now().isocalendar()[1]:
        return showRasp(request, getICS(group, date_, number_))

    elif date_.isocalendar()[1] == datetime.now().isocalendar()[1] + 1:
        return showRasp(request, getFromDB(group, date_, number_))

    else:
        return weekError(request)
>>>>>>> 8a05d9861055eb6edb00f5bb2f6d1cb4956d50b8

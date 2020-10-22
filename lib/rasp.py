from datetime import datetime, timedelta, date

from lib.new_parser import parse
from lib.returns import dateError, showRasp, numberError, sundayError


def rasp(request, group):
    Yandex_DateTime = dict()
    Yandex_Numbers = list()
    for token in request["request"]["nlu"]["entities"]:
        if token["type"] == "YANDEX.DATETIME":
            if not Yandex_DateTime:
                Yandex_DateTime = token

        elif token["type"] == "YANDEX.NUMBER":
            Yandex_Numbers.append(token)

    try:
        if Yandex_DateTime["value"]["day_is_relative"]:
            date_ = datetime.now().date() + timedelta(days=Yandex_DateTime["value"]["day"])
        else:
            date_ = date(day=Yandex_DateTime["value"]["day"], month=Yandex_DateTime["value"]["month"],
                         year=datetime.now().year)

        if date_.weekday() == 6:
            return sundayError(request)
    except KeyError:
        return dateError(request)

    Yandex_Number_temp = []
    for Yandex_Number in Yandex_Numbers:
        if not (Yandex_Number["tokens"]["start"] > Yandex_DateTime["tokens"]["start"]
                and Yandex_Number["tokens"]["end"] < Yandex_DateTime["tokens"]["end"]):
            Yandex_Number_temp.append(Yandex_Number)

    if len(Yandex_Number_temp) == 1:
        number_ = Yandex_Number_temp[0]["value"]
    elif len(Yandex_Number_temp) == 0:
        number_ = None
    else:
        return numberError(request)

    return showRasp(request, parse(group, date_, number_))

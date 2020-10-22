from datetime import date
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

from lib.constants import RASP_TPU_LESSON_TABLE_CLASS, dict_times, NO_RASP, NUMBER_ERROR_TEXT
from lib.decrypting import decrypt
from lib.lib import getCurrentLink


def get_tomsk_time(i):
    time_ = (datetime.combine(date.today(), dict_times[i]) + timedelta(hours=7)).time()
    return time_.strftime("%I:%M")


def parse_element(ele, key):
    if not ele.text:
        return ""
    elif "title" in ele.attrs.keys():
        return ele["title"]
    else:
        out = ""
        for div in ele.find_all("div"):
            if div.find("span"):
                out += decrypt(div.find("span")["data-title"], key) + "\n"
                if div.find("b"):
                    out += div.find("b")["title"] + "\n"
            elif div.find("a") and div.text[0:2] == "к.":
                out += div.text.replace("к.", "корпус").replace("ауд.", "аудитория") + "\n"
            elif div.find("a") and div.text[0:2] != "к." and not div.find("br"):
                out += div.text.replace(".", "") + "\n"
            elif div.find("a") and div.text[0:2] != "к." and div.find("br"):
                list_a = div.find_all("a")
                out += list_a[0].text.replace(".", "") + "\n"
                out += "корпус {}, аудитория {}".format(list_a[1].text, list_a[2].text) + "\n"
        return out


def parse(group, date_, number_):
    link = getCurrentLink(group, date_)
    soup = BeautifulSoup(requests.get(link).text, "lxml")

    # Parse main table to matrix (list of lists)
    data = []

    key = soup.find("meta", attrs={"name": "encrypt"})["content"]
    for row in soup.find('table', attrs={'class': RASP_TPU_LESSON_TABLE_CLASS}).find('tbody').find_all('tr'):
        cols = [ele for ele in row.find_all('td')]
        data.append([parse_element(ele, key) for ele in cols])  # Get rid of empty values

    # Transpose them and convert to tuple of tuples
    data = list(zip(*data))

    if number_ is None:
        data = "".join([f"{get_tomsk_time(i)}\n{row}\n" for i, row in enumerate(data[date_.weekday() + 1]) if row])
        if data:
            return data
        else:
            return NO_RASP
    else:
        try:
            if data[date_.weekday() + 1][number_ - 1]:
                return f"{get_tomsk_time(number_ - 1)}\n{data[date_.weekday() + 1][number_ - 1]}\n"
            else:
                return NO_RASP
        except IndexError:
            return NUMBER_ERROR_TEXT

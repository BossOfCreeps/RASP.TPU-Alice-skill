import json
from datetime import datetime

from bs4 import BeautifulSoup
import requests
from transliterate import translit

from lib.constants import RASP_TPU_GROUP_CLASS, RASP_TPU_SCHOOLS_CLASS, RASP_TPU_BASE


def firstMessage(text):
    return not bool(text)


def groupFromText(text):
    return translit(str(text).upper().replace(" ", "").replace("-", ""), "ru")


def getGroupLink(group):
    return "https://rasp.tpu.ru/gruppa_{}".format(json.load(open("getGruppa.json"))[group])


def getCurrentLink(group, date_):
    soup = BeautifulSoup(requests.get(RASP_TPU_BASE).text, "html.parser")
    soup = BeautifulSoup(requests.get(soup.find("a", class_=RASP_TPU_SCHOOLS_CLASS)["href"]).text, 'lxml')
    link = soup.find("a", class_=RASP_TPU_GROUP_CLASS)["href"]
    params = link[link.find("/", link.find("gruppa")):]

    year = params[:6]
    view = params[params.rfind("/"):]
    week = str(date_.isocalendar()[1] - datetime.now().date().isocalendar()[1] + int(params[len(year):-len(view)]))
    return getGroupLink(group) + year + week + view

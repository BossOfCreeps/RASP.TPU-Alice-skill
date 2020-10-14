<<<<<<< HEAD
from datetime import datetime

from bs4 import BeautifulSoup
import requests
from transliterate import translit

from lib.constants import RASP_TPU_GROUP_CLASS, RASP_TPU_SCHOOLS_CLASS, RASP_TPU_BASE
from lib.db import getGroupLink


def firstMessage(text):
    return not bool(text)


def groupFromText(text):
    return translit(str(text).upper().replace(" ", "").replace("-", ""), "ru")


def getCurrentLink(group, date_):
    soup = BeautifulSoup(requests.get(RASP_TPU_BASE).text, "html.parser")
    soup = BeautifulSoup(requests.get(soup.find("a", class_=RASP_TPU_SCHOOLS_CLASS)["href"]).text, 'lxml')
    link = soup.find("a", class_=RASP_TPU_GROUP_CLASS)["href"]
    params = link[link.find("/", link.find("gruppa")):]

    year = params[:6]
    view = params[params.rfind("/"):]
    week = str(date_.isocalendar()[1] - datetime.now().date().isocalendar()[1] + int(params[len(year):-len(view)]))
    return getGroupLink(group) + year + week + view
=======
from datetime import datetime

from bs4 import BeautifulSoup
import requests
from transliterate import translit

from lib.constants import RASP_TPU_GROUP_CLASS, RASP_TPU_SCHOOLS_CLASS, RASP_TPU_BASE
from lib.db import getGroupLink


def firstMessage(text):
    return not bool(text)


def groupFromText(text):
    return translit(str(text).upper().replace(" ", "").replace("-", ""), "ru")


def getCurrentLink(group, date_):
    soup = BeautifulSoup(requests.get(RASP_TPU_BASE).text, "html.parser")
    soup = BeautifulSoup(requests.get(soup.find("a", class_=RASP_TPU_SCHOOLS_CLASS)["href"]).text, 'lxml')
    link = soup.find("a", class_=RASP_TPU_GROUP_CLASS)["href"]
    params = link[link.find("/", link.find("gruppa")):]

    year = params[:6]
    view = params[params.rfind("/"):]
    week = str(date_.isocalendar()[1] - datetime.now().date().isocalendar()[1] + int(params[len(year):-len(view)]))
    return getGroupLink(group) + year + week + view
>>>>>>> 8a05d9861055eb6edb00f5bb2f6d1cb4956d50b8

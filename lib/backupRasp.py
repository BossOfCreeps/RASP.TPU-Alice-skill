from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from selenium import webdriver

from lib.constants import RASP_TPU_LESSON_TABLE_CLASS
from lib.db import insertRasp, deleteRasp
from lib.lib import getCurrentLink


def backupRasp(group):
    deleteRasp(group)

    browser = webdriver.Chrome(executable_path="chromedriver.exe")
    link = getCurrentLink(group, datetime.now() + timedelta(days=7))
    browser.get(link)
    soup = BeautifulSoup(browser.page_source, "lxml")
    browser.close()

    data = []
    for row in soup.find('table', attrs={'class': RASP_TPU_LESSON_TABLE_CLASS}).find('tbody').find_all('tr'):
        cols = [ele for ele in row.find_all('td')]
        data.append([ele for ele in cols if ele])

    rasp_matrix = tuple(zip(*data))

    for day, rasp_day in enumerate(rasp_matrix):
        if day != 0:
            for time, lesson in enumerate(rasp_day):
                insertRasp(group, day, time, lesson.text.replace("\n\n", "\n").rstrip())

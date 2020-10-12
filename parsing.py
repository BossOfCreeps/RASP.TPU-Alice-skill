import os
from datetime import datetime
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from constants import RASP_TPU_SCHOOLS_CLASS, RASP_TPU_COURSE_CLASS, RASP_TPU_BASE, RASP_TPU_GROUP_CLASS, \
    RASP_TPU_LESSON_TABLE_CLASS
from db import insert, delete
from ics import get_lesson


def parse_all_groups():
    """
    Parse group names and links from rasp.tpu.ru, delete previous records and update them
    :return:
    """

    # Parse school's links
    soup = BeautifulSoup(requests.get(RASP_TPU_BASE).text, "html.parser")
    schools = (item["href"] for item in soup.find_all("a", class_=RASP_TPU_SCHOOLS_CLASS))

    # Parse course's links
    courses = list()
    for school in schools:
        soup = BeautifulSoup(requests.get(school).text, 'lxml')
        for link_course in soup.find_all("ul", class_=RASP_TPU_COURSE_CLASS):
            for link_group in link_course.find_all("a"):
                courses.append(RASP_TPU_BASE + link_group["href"])

    # Parse group's links
    groups = dict()
    for course in courses:
        soup = BeautifulSoup(requests.get(course).text, 'lxml')
        for link in soup.find_all("a", class_=RASP_TPU_GROUP_CLASS):
            groups[link.text.rstrip()] = link["href"]

    # Delete previous records from table in database
    delete()
    # Insert new values to table
    for name, link in groups.items():
        insert(name.replace("-", ""), link[:link.find("/", link.find("gruppa"))])


def parse_rasp(link):
    """
    Parse lessons page

    :param link: link to rasp
    :return: matrix with rasp
    """
    # Get chrome webdriver
    browser = webdriver.Chrome(executable_path=r"C:\RASP.TPU-Alice-skill\chromedriver.exe")
    # Open them
    browser.get(link)
    # Parse page to BS
    soup = BeautifulSoup(browser.page_source, "lxml")
    # Close browser
    browser.close()

    # Parse main table to matrix (list of lists)
    data = []
    for row in soup.find('table', attrs={'class': RASP_TPU_LESSON_TABLE_CLASS}).find('tbody').find_all('tr'):
        cols = [ele for ele in row.find_all('td')]
        data.append([ele for ele in cols if ele])  # Get rid of empty values

    # Transpose them, convert to tuple of tuples and return
    return tuple(zip(*data))


def get_cur_page_params():
    soup = BeautifulSoup(requests.get(RASP_TPU_BASE).text, "html.parser")
    school = soup.find("a", class_=RASP_TPU_SCHOOLS_CLASS)["href"]
    soup = BeautifulSoup(requests.get(school).text, 'lxml')
    link = soup.find("a", class_=RASP_TPU_GROUP_CLASS)["href"]
    return link[link.find("/", link.find("gruppa")):]


def parse_ics(link, date, time):
    params = get_cur_page_params()
    year = params[:6]
    view = params[params.rfind("/"):]
    week_param = datetime.now().date().isocalendar()[1] - int(params[len(year):-len(view)])
    week = str(date.isocalendar()[1] - week_param)
    print(date, time, link + year + week + view)
    soup = BeautifulSoup(requests.get(link + year + week + view).text, "html.parser")
    ics_link = RASP_TPU_BASE + soup.find("div", class_="heading-text").find("a")["href"]
    file = r"C:\RASP.TPU-Alice-skill\facebook.ics"
    open(file, 'wb').write(requests.get(ics_link, allow_redirects=True).content)
    return get_lesson(file, date, time)


if __name__ == '__main__':
    pprint(parse_rasp("https://rasp.tpu.ru/gruppa_35397/2020/3/view.html"))
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from constants import RASP_TPU_SCHOOLS_CLASS, RASP_TPU_COURSE_CLASS, RASP_TPU_BASE, RASP_TPU_GROUP_CLASS, \
    RASP_TPU_LESSON_TABLE_CLASS
from db import insert, delete, select_group


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


def parse_rasp(group, day, time):
    """
    Parse lessons page

    :param group: group's name (without " " and "-") in upper register in russian
    :param day: number of day (0 - monday ... 5 - saturday)
    :param time: number of time 0...6 in LESSONS_TIME
    :return: text to speech
    """

    # Get chrome webdriver
    browser = webdriver.Chrome()
    # Open them
    browser.get(select_group(group)+get_cur_page_params())
    # Parse page to BS
    soup = BeautifulSoup(browser.page_source, "lxml")
    # Close browser
    browser.close()

    # Parse main table to matrix (list of lists)
    data = []
    for row in soup.find('table', attrs={'class': RASP_TPU_LESSON_TABLE_CLASS}).find('tbody').find_all('tr'):
        cols = [ele for ele in row.find_all('td')]
        data.append([ele for ele in cols if ele])  # Get rid of empty values
    # Transpose them and convert to tuple of tuples
    data = tuple(zip(*data))

    # Return value
    return data[day + 1][time].text.replace("\n\n", "\n").rstrip()


def get_cur_page_params():
    soup = BeautifulSoup(requests.get(RASP_TPU_BASE).text, "html.parser")
    school = soup.find("a", class_=RASP_TPU_SCHOOLS_CLASS)["href"]

    soup = BeautifulSoup(requests.get(school).text, 'lxml')
    link = soup.find("a", class_=RASP_TPU_GROUP_CLASS)["href"]
    return link[link.find("/", link.find("gruppa")):]

import sqlite3

import requests
from bs4 import BeautifulSoup

from lib.constants import RASP_TPU_BASE, RASP_TPU_SCHOOLS_CLASS, RASP_TPU_COURSE_CLASS, RASP_TPU_GROUP_CLASS, DB_FILE, \
    DB_GROUPS_TABLE, DB_GROUPS_NAME, DB_GROUPS_LINK


def updateGroups():
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
    conn = sqlite3.connect(DB_FILE)
    conn.cursor().execute(f"DELETE FROM {DB_GROUPS_TABLE}")
    conn.commit()

    # Insert new values to table
    conn = sqlite3.connect(DB_FILE)
    for name, link in groups.items():
        conn.cursor().execute(f"INSERT INTO {DB_GROUPS_TABLE}({DB_GROUPS_NAME},{DB_GROUPS_LINK}) "
                              f"VALUES('{name.replace('-', '')}','{link[:link.find('/', link.find('gruppa'))]}')")
    conn.commit()

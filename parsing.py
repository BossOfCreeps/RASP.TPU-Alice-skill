import requests
from bs4 import BeautifulSoup

from constants import RASP_TPU_SCHOOLS_CLASS, RASP_TPU_COURSE_CLASS, RASP_TPU_BASE, RASP_TPU_GROUP_CLASS
from db import insert, delete


def parse():
    """
    Parse group names and links from rasp.tpu.ru, delete previous records and update them
    :return:
    """

    # Parse school's links
    soup = BeautifulSoup(requests.get(RASP_TPU_BASE).text, "lxml")
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
        insert((name.replace("-", ""), link))

import requests
from bs4 import BeautifulSoup

import constants as const

soup = BeautifulSoup(requests.get(const.RASP_TPU_BASE).text, "lxml")

schools = (item["href"] for item in soup.find_all("a", class_=const.RASP_TPU_SCHOOLS_CLASS))

courses = list()
for school in schools:
    soup = BeautifulSoup(requests.get(school).text, 'lxml')
    for link_course in soup.find_all("ul", class_=const.RASP_TPU_COURSE_CLASS):
        for link_group in link_course.find_all("a"):
            courses.append(const.RASP_TPU_BASE + link_group["href"])

groups = dict()

for course in courses:
    soup = BeautifulSoup(requests.get(course).text, 'lxml')
    for link in soup.find_all("a", class_=const.RASP_TPU_GROUP_CLASS):
        groups[link.text.rstrip()] = link["href"]

print(groups)

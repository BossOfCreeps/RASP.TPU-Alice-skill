from datetime import time

ASK_GROUP_TEXT = "Здравствуйте. Мы не знакомы. Скажите, пожалуйства вашу группу."
ERROR_GROUP_TEXT = "Извините, но группы {} не существует"
SET_GROUP_TEXT = "Замечательно. Установлена группа {}"
SHOW_GROUP_TEXT = "Здравствуйте. Ваша группа {}"
DATE_ERROR_TEXT = "Извините, но я не могу заспознать дату"
NO_RASP = "Занятий нет"
NUMBER_ERROR_TEXT = "Извините, но я не могу заспознать номер пары"
WEEK_ERROR_TEXT = "Извините, но я могу рабоать только с текущей неделей и со следующей"

DB_FILE = r"db.sqlite3"
DB_USERS_TABLE = "users"
DB_USERS_ID = "id"
DB_USERS_GROUP = "group_"
DB_GROUPS_TABLE = "groups"
DB_GROUPS_NAME = "name"
DB_GROUPS_LINK = "link"
DB_LESSONS_TABLE = "lessons"
DB_LESSONS_NAME = "name"
DB_LESSONS_DAY = "day"
DB_LESSONS_TIME = "time"
DB_LESSONS_RASP = "rasp"

RASP_TPU_BASE = "https://rasp.tpu.ru"
RASP_TPU_SCHOOLS_CLASS = "departments-list__item"
RASP_TPU_COURSE_CLASS = "nav nav-tabs nav-tabs-bottom"
RASP_TPU_GROUP_CLASS = "group-catalog__list-link"
RASP_TPU_LESSON_TABLE_CLASS = "table table-bordered table-condensed timetable table-gray-border"

LESSONS_TIME = ["08:30-10:05", "10:25-12:00", "12:40-14:15", "14:35-16:10", "16:30-18:05", "18:25-20:00", "20:20-21:55"]

dict_times = {
    0: time(hour=1, minute=30),
    1: time(hour=3, minute=5),
    2: time(hour=5, minute=20),
    3: time(hour=7, minute=15),
    4: time(hour=9, minute=10),
    5: time(hour=11, minute=5),
    6: time(hour=13, minute=0),
    None: None,
}
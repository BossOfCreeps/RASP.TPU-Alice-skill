from datetime import datetime

from db import select_all, insert_lesson
from parsing import get_cur_page_params, parse_rasp


def backup_rasp(name, link):
    rasp_matrix = parse_rasp(link)
    for day, rasp_day in enumerate(rasp_matrix):
        if day != 0:
            for time, lesson in enumerate(rasp_day):
                insert_lesson(name, day, time, lesson.text.replace("\n\n", "\n").rstrip())


if __name__ == '__main__':
    start = datetime.now()
    print(start)
    backup_rasp('8ВМ92', "https://rasp.tpu.ru/gruppa_35397/2020/4/view.html")
    end = datetime.now()
    print(end)
    print(end - start)

import json
from datetime import datetime, timedelta
from threading import Thread

import flask
from transliterate import translit

from backuping import backup_rasp
from db import user_exist, add_user, get_user_group, is_group, select_group, delete_lesson
from parsing import parse_ics

app = flask.Flask(__name__)


def end(text):
    response = {
        "version": flask.request.json['version'],
        "session": flask.request.json['session'],
        "response": {
            "text": text,
            # "tts": tts,
            "end_session": False
        }
    }
    return json.dumps(response, ensure_ascii=False, indent=2)


@app.route("/", methods=['POST'])
def main():
    request = flask.request.json

    user_id = request['session']['user_id']
    text = request["request"]["original_utterance"]

    # User enter skill and he has group
    if not text and user_exist(user_id):
        group = get_user_group(user_id)
        delete_lesson(group)
        thread1 = Thread(target=backup_rasp, args=(group, "https://rasp.tpu.ru/gruppa_35397/2020/4/view.html",))
        thread1.start()

        return end(f"Приветствую. Ваша группа: {group}")

    # User enter skill and he hasn't group
    if not text and not user_exist(user_id):
        return end("Здравствуйте. Какая у вас группа?")

    # If wait group
    if text and not user_exist(user_id):
        # Check them

        group = translit(str(text).upper().replace(" ", "").replace("-", ""), "ru")
        if is_group(group):
            add_user(user_id, group)
            return end(f"Отлично! Ваша группа {group}.")
        else:
            return end(f"Группы {group} нет.")

    # If work
    if text and user_exist(user_id):
        Yandex_DateTime = dict()
        Yandex_Number = list()
        for token in request["request"]["nlu"]["entities"]:
            if token["type"] == "YANDEX.DATETIME":
                if not Yandex_DateTime:
                    Yandex_DateTime = token

            elif token["type"] == "YANDEX.NUMBER":
                Yandex_Number.append(token)
        try:
            if not Yandex_DateTime and not Yandex_Number:
                return end("Не смогла обнаружить указание на день недели или время пары")

            elif Yandex_DateTime and not Yandex_Number:
                today = datetime.now().date()
                day = today + timedelta(days=int(Yandex_DateTime["value"]["day"]))

                if day.isocalendar()[1] != today.isocalendar()[1]:
                    return end("Прости, но я могу работать только с текущей неделей")

                values = parse_ics(select_group(get_user_group(user_id)), day, None)
                out = ""
                for value in values:
                    out += value
                return end(out)

            elif not Yandex_DateTime and Yandex_Number:
                if len(Yandex_Number) > 1:
                    return end("Номер пары сформулирован не чётко")

                time = Yandex_Number[0]["value"]
                if time < 1 or time > 7:
                    return end(f"Пары {time} нет")

                values = sorted(parse_ics(select_group(get_user_group(user_id)), None, time - 1))

                out = ""
                for value in values:
                    out += value

                return end(out)

            elif Yandex_DateTime and Yandex_Number:
                today = datetime.now().date()
                day = today + timedelta(days=int(Yandex_DateTime["value"]["day"]))

                if day.isocalendar()[1] != today.isocalendar()[1]:
                    return end("Прости, но я могу работать только с текущей неделей")

                if len(Yandex_Number) > 1:
                    return end("Номер пары сформулирован не чётко")

                time = Yandex_Number[0]["value"]
                if time < 1 or time > 7:
                    return end(f"Пары {time} нет")

                values = parse_ics(select_group(get_user_group(user_id)), day, time - 1)
                out = ""
                for value in values:
                    out += value
                return end(out)

        except:
            return end("Произошла ошибка. Скорее всегда данный функционал всё ещё находится в разработке")

        return end(f"Все говорят '{text}', а ты купи слона!")


if __name__ == '__main__':
    app.run("0.0.0.0", 5000, ssl_context=(r'C:\RASP.TPU-Alice-skill\full.pem', r'C:\RASP.TPU-Alice-skill\priv.pem'))

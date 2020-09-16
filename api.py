import json

import flask

from db import user_exist, add_user, get_user_group, is_group

app = flask.Flask(__name__)


def end(text):
    response = {
        "version": flask.request.json['version'],
        "session": flask.request.json['session'],
        "response": {
            "text": text,
            "end_session": False
        }
    }
    return json.dumps(response, ensure_ascii=False, indent=2)


@app.route("/", methods=['POST'])
def main():
    request = flask.request.json

    user_id = request['session']['user_id']
    # User enter skill
    if not request["request"]["original_utterance"]:
        # If he has group
        if user_exist(user_id):
            return end(f"Приветствую. Ваша группа: {get_user_group(user_id)}")

        # If no group
        else:
            return end("Здравствуйте. Какая у вас группа?")

    # If wait group
    if request["request"]["original_utterance"] and not user_exist(user_id):
        group = str(request["request"]["original_utterance"]).upper().replace(" ", "").replace("-", "")

        # Check them
        if is_group(group):
            add_user(user_id, group)
            return end(f"Отлично! Ваша группа {group}.")
        else:
            return end(f"Группы {group} нет.")

    # If work
    if request["request"]["original_utterance"] and user_exist(user_id):
        return end(f'Все говорят "{request["request"]["original_utterance"]}", а ты купи слона!')


if __name__ == '__main__':
    app.run("0.0.0.0", 5000, ssl_context='adhoc')

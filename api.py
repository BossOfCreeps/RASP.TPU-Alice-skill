import json

import flask

app = flask.Flask(__name__)


# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])
def main():
    request = flask.request.json
    user_id = request['session']['user_id']

    # Функция получает тело запроса и возвращает ответ.
    response = {
        "version": request['version'],
        "session": request['session'],
        "response": {
            "text": "",
            "end_session": False
        }
    }

    # Это новый пользователь.
    if request['session']['new']:
        response['response']['text'] = "Привет! Купи слона!"

    # Обрабатываем ответ пользователя. Если пользователь согласился, прощаемся.
    elif request['request']['original_utterance'].lower() in ['ладно', 'куплю', 'покупаю', 'хорошо', ]:
        response['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'

    # Если нет, то убеждаем его купить слона!
    else:
        response['response']['text'] = f'Все говорят "{request["request"]["original_utterance"]}", а ты купи слона!'

    return json.dumps(response, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    app.run("0.0.0.0", 5000, ssl_context='adhoc')

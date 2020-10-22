import os
from sys import platform

import flask

from lib.db import isFamiliar, isGroup, setGroup, getGroup
from lib.lib import firstMessage, groupFromText
from lib.rasp import rasp
from lib.returns import askGroup, errorGroup, setGroupMessage, showGroup

app = flask.Flask(__name__)


@app.route("/", methods=['POST'])
def main():
    request = flask.request.json
    user = request['session']['user_id']
    text = request["request"]["command"]

    if isFamiliar(user):
        group = getGroup(user)
        if firstMessage(text):
            return showGroup(request, group)
        else:
            return rasp(request, group)
    else:
        if firstMessage(text):
            return askGroup(request)
        else:
            group = groupFromText(text)
            if isGroup(group):
                setGroup(user, group)
                return setGroupMessage(request, group)
            else:
                return errorGroup(request, group)


if __name__ == '__main__':
    if platform == "win32":
        os.chdir(r"C:\RASP.TPU-Alice-skill")
    app.run("0.0.0.0", 5000, ssl_context='adhoc')

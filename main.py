import json
from threading import Thread

import flask

from lib.backupRasp import backupRasp
from lib.db import isFamiliar, isGroup, setGroup, getGroup
from lib.lib import firstMessage, groupFromText
from lib.rasp import rasp
from lib.returns import askGroup, errorGroup, setGroupMessage, showGroup
from lib.updateGroups import updateGroups

app = flask.Flask(__name__)


@app.route("/update_groups", methods=['GET'])
def update_groups():
    updateGroups()
    return "OK"


@app.route("/", methods=['POST'])
def main():
    request = flask.request.json
    print(request)
    user = request['session']['user_id']
    text = request["request"]["command"]

    if isFamiliar(user):
        group = getGroup(user)
        if firstMessage(text):
            Thread(target=backupRasp, args=(group,)).start()
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
                Thread(target=backupRasp, args=(group,)).start()
                return setGroupMessage(request, group)
            else:
                return errorGroup(request, group)


if __name__ == '__main__':
    app.run("0.0.0.0", 5001, ssl_context=('pem.full', 'pem.priv'))

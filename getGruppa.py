import json

import requests

from lib.constants import getGruppa_url

if __name__ == '__main__':
    data = dict()
    for record in requests.get(getGruppa_url).text.split("\n"):
        if len(record.split("|")) == 1:
            continue

        group, number = record.split("|")

        if group not in data.keys() or (group in data.keys() and int(number) > data[group]):
            data[group] = int(number)

    open("getGruppa.json", "w").write(json.dumps(data))

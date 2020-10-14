<<<<<<< HEAD
import json

from lib.constants import ASK_GROUP_TEXT, ERROR_GROUP_TEXT, SET_GROUP_TEXT, SHOW_GROUP_TEXT, DATE_ERROR_TEXT, NO_RASP, \
    NUMBER_ERROR_TEXT, WEEK_ERROR_TEXT


def __get_response(request, text):
    return {
        "version": request['version'],
        "session": request['session'],
        "response": {
            "text": text,
            "end_session": False
        }
    }


def askGroup(request):
    return json.dumps(__get_response(request, ASK_GROUP_TEXT), ensure_ascii=False, indent=2)


def errorGroup(request, group):
    return json.dumps(__get_response(request, ERROR_GROUP_TEXT.format(group)), ensure_ascii=False, indent=2)


def setGroupMessage(request, group):
    return json.dumps(__get_response(request, SET_GROUP_TEXT.format(group)), ensure_ascii=False, indent=2)


def showGroup(request, group):
    return json.dumps(__get_response(request, SHOW_GROUP_TEXT.format(group)), ensure_ascii=False, indent=2)


def dateError(request):
    return json.dumps(__get_response(request, DATE_ERROR_TEXT), ensure_ascii=False, indent=2)


def numberError(request):
    return json.dumps(__get_response(request, NUMBER_ERROR_TEXT), ensure_ascii=False, indent=2)


def weekError(request):
    return json.dumps(__get_response(request, WEEK_ERROR_TEXT), ensure_ascii=False, indent=2)


def showRasp(request, data):
    return json.dumps(__get_response(request, ''.join(data) if data else NO_RASP), ensure_ascii=False, indent=2)
=======
import json

from lib.constants import ASK_GROUP_TEXT, ERROR_GROUP_TEXT, SET_GROUP_TEXT, SHOW_GROUP_TEXT, DATE_ERROR_TEXT, NO_RASP, \
    NUMBER_ERROR_TEXT, WEEK_ERROR_TEXT


def __get_response(request, text):
    return {
        "version": request['version'],
        "session": request['session'],
        "response": {
            "text": text,
            "end_session": False
        }
    }


def askGroup(request):
    return json.dumps(__get_response(request, ASK_GROUP_TEXT), ensure_ascii=False, indent=2)


def errorGroup(request, group):
    return json.dumps(__get_response(request, ERROR_GROUP_TEXT.format(group)), ensure_ascii=False, indent=2)


def setGroupMessage(request, group):
    return json.dumps(__get_response(request, SET_GROUP_TEXT.format(group)), ensure_ascii=False, indent=2)


def showGroup(request, group):
    return json.dumps(__get_response(request, SHOW_GROUP_TEXT.format(group)), ensure_ascii=False, indent=2)


def dateError(request):
    return json.dumps(__get_response(request, DATE_ERROR_TEXT), ensure_ascii=False, indent=2)


def numberError(request):
    return json.dumps(__get_response(request, NUMBER_ERROR_TEXT), ensure_ascii=False, indent=2)


def weekError(request):
    return json.dumps(__get_response(request, WEEK_ERROR_TEXT), ensure_ascii=False, indent=2)


def showRasp(request, data):
    return json.dumps(__get_response(request, ''.join(data) if data else NO_RASP), ensure_ascii=False, indent=2)
>>>>>>> 8a05d9861055eb6edb00f5bb2f6d1cb4956d50b8

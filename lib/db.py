import sqlite3

from lib.constants import DB_FILE, DB_USERS_TABLE, DB_GROUPS_TABLE, DB_GROUPS_NAME, DB_USERS_ID, DB_USERS_GROUP, \
    DB_LESSONS_TABLE, DB_LESSONS_DAY, DB_LESSONS_TIME, DB_LESSONS_RASP, DB_LESSONS_NAME, dict_times


def isFamiliar(user):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor().execute(f"SELECT * FROM {DB_USERS_TABLE} WHERE {DB_USERS_ID}='{user}'")
    return bool(cur.fetchall())


def isGroup(group):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor().execute(f"SELECT * FROM {DB_GROUPS_TABLE} WHERE {DB_GROUPS_NAME}='{group}'")
    return bool(cur.fetchall())


def setGroup(user, group):
    conn = sqlite3.connect(DB_FILE)
    conn.cursor().execute(f"INSERT INTO {DB_USERS_TABLE}({DB_USERS_ID},{DB_USERS_GROUP}) VALUES('{user}','{group}')")
    conn.commit()


def getGroup(user):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor().execute(f"SELECT * FROM {DB_USERS_TABLE} WHERE {DB_USERS_ID}='{user}'")
    return cur.fetchall()[0][1]


def getGroupLink(group):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor().execute(f"SELECT * FROM {DB_GROUPS_TABLE} WHERE {DB_GROUPS_NAME}='{group}'")
    return cur.fetchall()[0][1]


def insertRasp(group, day, time, rasp):
    conn = sqlite3.connect(DB_FILE)
    conn.cursor().execute(f"INSERT INTO {DB_LESSONS_TABLE}({DB_LESSONS_NAME},{DB_LESSONS_DAY},{DB_LESSONS_TIME},"
                          f"{DB_LESSONS_RASP}) VALUES('{group}','{day}','{time}','{rasp}')")
    conn.commit()


def deleteRasp(group):
    conn = sqlite3.connect(DB_FILE)
    conn.cursor().execute(f"DELETE FROM {DB_LESSONS_TABLE} WHERE {DB_LESSONS_NAME}='{group}'")
    conn.commit()


def getFromDB(group, date_, number_):
    day = date_.isoweekday()
    conn = sqlite3.connect(DB_FILE)
    if number_ is None:
        sql = f"SELECT * FROM {DB_LESSONS_TABLE} WHERE {DB_LESSONS_NAME}='{group}' AND {DB_LESSONS_DAY}='{day}'"
    else:
        sql = f"SELECT * FROM {DB_LESSONS_TABLE} WHERE {DB_LESSONS_NAME}='{group}' AND {DB_LESSONS_DAY}='{day}' " \
              f"AND {DB_LESSONS_TIME}='{number_}'"
    cur = conn.cursor().execute(sql)
    data = []
    for row in cur.fetchall():
        if row[3]:
            data.append(f"В {dict_times[row[2]]}\n{row[3]}\n\n")
    return data

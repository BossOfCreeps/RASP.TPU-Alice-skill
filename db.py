import sqlite3

from constants import DB_FILE, DB_GROUPS_TABLE, DB_GROUPS_NAME, DB_GROUPS_LINK, DB_USERS_TABLE, DB_USERS_ID, \
    DB_USERS_GROUP


def insert(name: str, link: str):
    """
    Create a new record in database

    :param name: group's name
    :param link: part of link to group
    """
    conn = sqlite3.connect(DB_FILE)
    conn.cursor().execute(f"INSERT INTO {DB_GROUPS_TABLE}({DB_GROUPS_NAME},{DB_GROUPS_LINK}) VALUES({name},{link})")
    conn.commit()


def select_all() -> list:
    """
    Query all rows in the table
    :return: rows in table
    """
    cur = sqlite3.connect(DB_FILE).cursor()
    cur.execute(f"SELECT * FROM {DB_GROUPS_TABLE}")
    return cur.fetchall()


def select_group(group) -> str:
    """
    Query all rows in the table
    :return: rows in table
    """
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor().execute(f"SELECT * FROM {DB_GROUPS_TABLE} WHERE {DB_GROUPS_NAME}='{group}'")
    return cur.fetchall()[0][1]


def delete():
    """
    Delete all record in table
    """
    conn = sqlite3.connect(DB_FILE)
    conn.cursor().execute(f"DELETE FROM {DB_GROUPS_TABLE}")
    conn.commit()


def user_exist(user_id: str) -> bool:
    """
    Check user in DB
    :param user_id: user id
    :return: true/false
    """
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor().execute(f"SELECT * FROM {DB_USERS_TABLE} WHERE {DB_USERS_ID}='{user_id}'")
    return bool(cur.fetchall())


def add_user(user_id: str, group: str):
    """
    Insert user in DB
    :param user_id: user's id
    :param group: gropu name
    """
    conn = sqlite3.connect(DB_FILE)
    conn.cursor().execute(f"INSERT INTO {DB_USERS_TABLE}({DB_USERS_ID},{DB_USERS_GROUP}) VALUES('{user_id}','{group}')")
    conn.commit()


def get_user_group(user_id: str) -> str:
    """
    Get group of user
    :param user_id: user's id
    :return: group
    """
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor().execute(f"SELECT * FROM {DB_USERS_TABLE} WHERE {DB_USERS_ID}='{user_id}'")
    return cur.fetchall()[0][1]


def update_user(user_id: str, group: str):
    """
    Update user in DB
    :param user_id: user's id
    :param group: group's name
    """
    conn = sqlite3.connect(DB_FILE)
    conn.cursor().execute(f"UPDATE {DB_USERS_TABLE} SET {DB_USERS_GROUP}='{group}' WHERE {DB_USERS_ID}='{user_id}'")
    conn.commit()


def is_group(group: str) -> bool:
    """
    Check is str is group
    :param group: group's name
    :return: true/false
    """
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor().execute(f"SELECT * FROM {DB_GROUPS_TABLE} WHERE {DB_GROUPS_NAME}='{group}'")
    return bool(cur.fetchall())

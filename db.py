import sqlite3

from constants import DB_FILE, DB_GROUPS_TABLE, DB_GROUPS_NAME, DB_GROUPS_LINK


def insert(task: tuple):
    """
    Create a new record in database
    :param task: tuple(name, link)
    """
    conn = sqlite3.connect(DB_FILE)
    sql = f"INSERT INTO {DB_GROUPS_TABLE}({DB_GROUPS_NAME},{DB_GROUPS_LINK}) VALUES(?,?)"
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()


def select_all():
    """
    Query all rows in the table
    :return: rows in table
    """
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {DB_GROUPS_TABLE}")
    rows = cur.fetchall()
    return rows


def select_group(group):
    """
    Query all rows in the table
    :return: rows in table
    """
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {DB_GROUPS_TABLE} WHERE {DB_GROUPS_NAME}='{group}'")
    rows = cur.fetchall()
    return rows[0][1]


def delete():
    """
    Delete all record in table
    """
    conn = sqlite3.connect(DB_FILE)
    sql = f"DELETE FROM {DB_GROUPS_TABLE}"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

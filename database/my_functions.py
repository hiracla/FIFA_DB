import sqlite3
from prettytable import PrettyTable


def open_database(dbname):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    return conn, cursor


def close_database(cursor, conn):
    cursor.close()
    conn.close()


def print_players_prettytable(sql):
    conn, cursor = open_database("fifa23.db")
    cursor.execute(sql)
    data = cursor.fetchall()
    table = PrettyTable(["name", "level", "club", "position"])
    for (
        LEVEL,
        NAME,
        COUNTRY,
        LEAGUE,
        CLUB,
        POSITION,
        PACE,
        SHOOT,
        PASS,
        DRIBBLE,
        DEFENSE,
        PHYSICAL,
    ) in data:
        table.add_row([LEVEL, NAME, CLUB, POSITION])

    print(table)
    cursor.close()
    conn.close()

import csv
import sqlite3

dbpath = "fifa23.db"
conn = sqlite3.connect(dbpath)
cursor = conn.cursor()
sql = """
CREATE TABLE IF NOT EXISTS teams(
    team_id TEXT PRIMARY KEY,
    team_name TEXT,
    system TEXT,
    director TEXT
)"""

cursor.execute(sql)
conn.commit()

with open("FIFA23Switch_teams.csv", "r", encoding="utf-8") as f:
    rows = csv.reader(f)
    header = next(rows)
    data = []
    for row in rows:
        data.append(row)

sql = """INSERT INTO teams (TEAM_ID,TEAM_NAME,SYSTEM,DIRECTOR) VALUES(?,?,?,?)"""

cursor.executemany(sql, data)
conn.commit()
cursor.close()
conn.close()

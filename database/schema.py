import sqlite3

dbpath='fifa23.db'

conn=sqlite3.connect(dbpath)
cursor=conn.cursor()
sql="""PRAGMA TABLE_INFO('players')"""

db_info=cursor.execute(sql).fetchall()

print(db_info)
cursor.close()
conn.close()
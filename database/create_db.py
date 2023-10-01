import sqlite3

dbpath='fifa23.db'
conn=sqlite3.connect(dbpath)

conn.close()
import sqlite3

conn = sqlite3.connect('clarity.db', check_same_thread=False)
c = conn.cursor()


# users table
c.execute('''CREATE TABLE users (gender TEXT, rank INTEGER, username TEXT PRIMARY KEY, password TEXT, name TEXT, voted TEXT)''')
#c.execute('''INSERT INTO users VALUES ('male', 1, 'admin', 'gtf0myface', 'Timothy Ong')''')


# answers table
# date stored in UNIX time for easy conversion in Python
# SQL will auto increment aid to prevent collisions
c.execute('''CREATE TABLE answers (upvotes INTEGER,
                                   adate INTEGER,
                                   aid INTEGER PRIMARY KEY AUTOINCREMENT,
                                   atext TEXT,
                                   qid INTEGER,
                                   username TEXT)''')
"""
c.execute('''INSERT INTO answers (upvotes, adate, atext, qid, username)
              VALUES (1337, 1457822190, 'por que no los dos?', 1, 'admin')''')
c.execute('''INSERT INTO answers (upvotes, adate, atext, qid, username)
              VALUES (-1337, 1457822193, 'asdf', 1, 'admin')''')
"""


c.execute('''CREATE TABLE questions (title TEXT,
                                     qdate INTEGER,
                                     qtext TEXT,
                                     qid INTEGER PRIMARY KEY AUTOINCREMENT,
                                     category TEXT,
                                     username TEXT)''')

#admins table
#contains a list of the admins usernames
#c.execute('''CREATE TABLE admins (username TEXT)''')


#add admins
#c.execute('''INSERT INTO admins VALUES ('admin')''')


conn.commit()
conn.close()

import sqlite3

conn = sqlite3.connect('clarity.db', check_same_thread=False)
c = conn.cursor()

def getUser(username):
    c.execute('SELECT gender, rank, username, name FROM users WHERE username=:username', {"username":username})
    return c.fetchone()

def getQuestionById(qid):
    c.execute('SELECT * FROM questions WHERE qid=?', qid)
    return c.fetchone()

def getQuestionsByCategory(category):
    c.execute('SELECT * FROM questions WHERE category=:category ORDER BY qdate DESC', {"category":category})
    return c.fetchall()

def getQuestionsByUser(username, order):
    c.execute('SELECT * FROM questions WHERE username=:username ORDER BY :order DESC',
              {"username":username, "order":order})
    return c.fetchall()

def getAllQuestions():
    c.execute('SELECT * FROM questions ORDER BY qdate DESC')
    return c.fetchall()

def getAnswersByQuestion(qid):
    c.execute('SELECT * FROM answers WHERE qid=? ORDER BY upvotes DESC', qid)
    return c.fetchall()

def getAnswerById(aid):
    c.execute('SELECT * FROM answers WHERE aid=:aid', {"aid":aid})
    return c.fetchone()

def getAnswersByUser(username, order):
    c.execute('SELECT * FROM answers WHERE username=:username ORDER BY :order DESC', 
              {"username":username, "order":order})
    return c.fetchall()

def insertQuestion(title, qdate, qtext, category, username):
    c.execute('''INSERT INTO questions (title, qdate, qtext, category, username)
                 VALUES (:title, :qdate, :qtext, :category, :username)''',
              {"title":title, "qdate":qdate, "qtext":qtext, "category":category, "username":username})
    conn.commit()
    return True

def deleteQuestion(qid):
    c.execute('DELETE FROM questions WHERE qid=:qid', {"qid":qid})
    c.execute('DELETE FROM answers WHERE qid=:qid', {"qid":qid})
    conn.commit()
    return True

def insertAnswer(adate, atext, qid, username):
    c.execute('''INSERT INTO answers (upvotes, adate, atext, qid, username)
                 VALUES (0, :adate, :atext, :qid, :username)''',
              {"adate":adate, "atext":atext, "qid":qid, "username":username})
    conn.commit()
    return True

def deleteAnswer(aid):
    c.execute('DELETE FROM answers WHERE aid=:aid', {"aid":aid})
    conn.commit()
    return True

def insertUser(gender, rank, username, password, name):
    c.execute('''INSERT INTO users VALUES (:gender, :rank, :username, :password, :name)''',
              {"gender":gender, "rank":rank, "username":username, "password":password, "name":name})
    conn.commit()
    return True

def login(username, password):
    c.execute('SELECT * FROM users WHERE username=:username',
              {"username":username})
    x = c.fetchone()
    if x == None:
        return "Username not found"
    elif x[3] != password:
        return "Invalid username/password combination"
    else:
        return "True"

def register(gender, username, password, name):
    if login(username, password) != "Username not found":
        return "Username is already taken"
    else:
        x = insertUser(gender, 0, username, password, name)
        conn.commit()
        if x:
            return "True"
        else:
            return "Failed"

def changePassword(username, password, newpassword):
    c.execute('SELECT * FROM users WHERE username=:username',
              {"username":username})
    x = c.fetchone()
    if x[3] != password:
        return "Incorrect password entered"
    else:
        c.execute('UPDATE users SET password=:newpassword WHERE username=:username',
                  {"newpassword":newpassword, "username":username})
        conn.commit()
        return "Password successfully changed"

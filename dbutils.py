import sqlite3

conn = sqlite3.connect('clarity.db', check_same_thread=False)
c = conn.cursor()

def getUser(username):
    c.execute('SELECT gender, rank, username, name FROM users WHERE username=:username', {"username":username})
    return c.fetchone()

def getVotes(username):
    c.execute('SELECT voted FROM users WHERE username=:username', {"username":username})
    return c.fetchone()

def updateVoted(username, voted):
    c.execute('UPDATE users SET voted=:voted WHERE username=:username', {"voted":voted, "username":username})
    conn.commit()
    return True

def getCategories():
    c.execute('SELECT DISTINCT category FROM questions')
    return c.fetchall()

def getQuestionById(qid):
    c.execute('SELECT * FROM questions WHERE qid=:qid', {"qid":qid})
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
    c.execute('SELECT * FROM answers WHERE qid=:qid ORDER BY upvotes DESC', {"qid":qid})
    return c.fetchall()

def getAnswerById(aid):
    c.execute('SELECT * FROM answers WHERE aid=:aid', {"aid":aid})
    return c.fetchone()

def getAnswersByUser(username, order):
    c.execute('SELECT * FROM answers WHERE username=:username ORDER BY :order DESC', 
              {"username":username, "order":order})
    return c.fetchall()

def insertQuestion(title, qdate, qtext, category, username, minReq):
    c.execute('''INSERT INTO questions (title, qdate, qtext, category, username, minReq)
                 VALUES (:title, :qdate, :qtext, :category, :username, :minReq)''',
              {"title":title, "qdate":qdate, "qtext":qtext, "category":category, "username":username, "minReq":minReq})
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

def updateAnswer(aid, votes):
    c.execute('UPDATE answers SET upvotes=:votes WHERE aid=:aid', {"votes":votes, "aid":aid})
    conn.commit()
    return True

def getUserRank(user):
    c.execute('SELECT rank FROM users WHERE username=:username', {"username":user})
    return c.fetchone()[0]

def updateUserRank(user, rank):
    c.execute('UPDATE users SET rank=:rank WHERE username=:username', {"rank":rank, "username":user})
    conn.commit()
    return True

def getUserCredits(user):
    c.execute('SELECT credits FROM users WHERE username=:username', {"username":user})
    return c.fetchone()[0]

def updateCredit(user, credit):
    c.execute('UPDATE users SET credits=:credits WHERE username=:username', {"credits":credit, "username":user})
    conn.commit()
    return True

def insertUser(gender, rank, username, password, name):
    c.execute('''INSERT INTO users VALUES (:gender, :rank, :username, :password, :name, :voted, :credits)''',
              {"gender":gender, "rank":rank, "username":username, "password":password, "name":name, "voted":"", "credits":0})
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
        
def getKey(item):
    return item[0]
    
def searchQuestions(searchTokens, categories):
    
    c.execute('SELECT * FROM questions')
    questionList = c.fetchall();
    
    results = []
    
    for entry in questionList: # for questions
        matchStrength = 0
        postWords = entry[0] + " " + entry[2] # title + " " + question_text
        
        c.execute('SELECT * FROM answers WHERE qid=:qid', {"qid":entry[3]})
        answerList = c.fetchall();
        
        answersString = ""
        upvoteSum = 0 # total upvotes by answers in this question
        for answer in answerList:
            upvoteSum += answer[0]
            answersString += " " + answer[3]
            
        postWords += " " + answersString
        
        for word in searchTokens: # for search token
            matches = postWords.lower().count(word.lower())
            if(matches != 0):
                matchStrength += matches
            
        if matchStrength != 0:
            results.append((matchStrength * (upvoteSum+1), entry[0], entry[3]))
    sort = []
    sort = sorted(results, key=getKey, reverse=True)
    return sort
        
'''
def isUserAdmin(username):
    return False'''
'''
    c.execute('SELECT * FROM admins WHERE username=:username',
              {"username":username})
    x = c.fetchone()

    if x == None:
        return False
    else:
        return True
'''
    

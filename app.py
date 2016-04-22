from flask import Flask, render_template, url_for, redirect, request, session
import dbutils, sqlite3
import time, calendar

app = Flask(__name__)
app.secret_key = "el em eff ay oh"

@app.route("/",methods=["GET", "POST"])
@app.route("/<category>", methods=["GET", "POST"])
def forum(category = None):
    if request.method == "GET":
        allCategories = dbutils.getCategories()
        if category is None:
            allQuestions = dbutils.getAllQuestions()
            if 'username' in session:
                return render_template("forum.html", username=session['username'], questions=allQuestions, categories=allCategories)
            else:
                return render_template("forum.html", questions=allQuestions,categories=allCategories)
        else:
            questions = dbutils.getQuestionsByCategory(category)
            if 'username' in session:
                return render_template("forum.html", username=session['username'], questions=questions, category=category,categories=allCategories )
            else:
                return render_template("forum.html", questions=questions, category=category,categories=allCategories)
    else:
        searchString = request.form['searchfield'].encode('ascii', 'ignore').strip()
        searchTokens = searchString.split(' ')

        sort = dbutils.searchQuestions(searchTokens)

        searchResults = []
        for entry in sort:
            searchResults.append(entry)
        if 'username' in session:
            return render_template("search.html", results=searchResults, username=session['username'])
        else:
            return render_template("search.html", results=searchResults)

@app.route("/login", methods=["GET", "POST"])
def login(redirectTo = None):
    if 'username' in session:
        return redirect(url_for("forum"))
    else:
        if request.method == "GET":
            return render_template("login.html")
        else:
            username = request.form['username'].encode('ascii', 'ignore')
            password = request.form['password'].encode('ascii', 'ignore')

            retval = dbutils.login(username, password)
            if retval == 'True':
                session['username'] = username
                if redirectTo is None:
                    return redirect(url_for("forum"))
                else:
                    return redirect(url_for(redirectTo))
            else:
                return render_template("login.html", error = retval)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for("forum"))

@app.route("/register", methods=["GET", "POST"])
def register(redirectTo = None):
    if 'username' in session:
        return redirect(url_for("forum"))
    else:
        if request.method == "GET":
            return render_template("register.html")
        else:
            # default gender to 'M' cus who cares about gender.
            gender = 'M'
            #gender = request.form['gender']
            #assert (gender in ["M", "F"])
            name = request.form['name'].encode('ascii', 'ignore')
            if len(name) < 3:
                return render_template("register.html", error = "Please include first and last name")
            username = request.form['username'].encode('ascii', 'ignore').strip()
            if len(username) < 4:
                return render_template("register.html", error = "Username must be at least 4 characters long")
            password = request.form['password'].encode('ascii', 'ignore')
            if len(password) < 6:
                return render_template("register.html", error = "Password must be at least 6 characters long")
            passwordconf = request.form['passwordconf'].encode('ascii', 'ignore')
            if passwordconf != password:
                return render_template("register.html", error = "Passwords did not match")


            retval = dbutils.register(gender, username, password, name)
            if retval == "True":
                session['username'] = username
                if redirectTo is None:
                    return redirect(url_for("forum"))
                else:
                    return redirect(url_for(redirectTo))
            else:
                return render_template("register.html", error = retval)

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if 'username' not in session:
        return redirect(url_for("login"))
    else:
        if request.method == "GET":
            userinfo = dbutils.getUser(session['username'])
            return render_template("settings.html", username=session['username'],userinfo=userinfo)
        else:
            userinfo = dbutils.getUser(session['username'])
            password = request.form['password'].encode('ascii', 'ignore')
            newpassword = request.form['newpassword'].encode('ascii', 'ignore')
            retval = dbutils.changePassword(session['username'], password, newpassword)
            return render_template("settings.html", userinfo=userinfo, retval=retval, username=session['username'])


'''
@app.route("/forum")
@app.route("/forum/<category>")
def forum(category = None):
    isAdmin = False
    if 'username' in session:
        isAdmin = dbutils.isUserAdmin(session['username'])
    if category is None:
        allQuestions = dbutils.getAllQuestions()
        if 'username' in session:
            return render_template("forum.html", username=session['username'], questions=allQuestions, isAdmin=isAdmin)
        else:
            return render_template("forum.html", questions=allQuestions)
    else:
        questions = dbutils.getQuestionsByCategory(category)
        if 'username' in session:
            return render_template("forum.html", username=session['username'], questions=questions, category=category, isAdmin=isAdmin)
        else:
            return render_template("forum.html", questions=questions, category=category)
'''


@app.route("/postquestion", methods=["GET", "POST"])
def postquestion():
    if 'username' not in session:
        return redirect(url_for("error"))
    else:
        cred = dbutils.getUserCredits(session['username'])
        if request.method == "GET":
            return render_template("postquestion.html", username=session['username'], credit=cred)
        else:
            if request.form['submit'] == 'Post':
                questionTitle = request.form['questionTitle'].encode('ascii', 'ignore')
                questionText = request.form['questionText'].encode('ascii', 'ignore')
                category = request.form['category']
                if category == 'other':
                    category = request.form['other']
                minReq = 0
                if request.form['min'] != "":
                    try:
                        minReq = int(request.form['min'])
                    except:
                        return redirect(url_for("error"))

                cred = dbutils.getUserCredits(session['username'])
                if (cred < 1):
                    minReq = 0
                else:
                    cred -= 1
                dbutils.updateCredit(session['username'], cred)
                dbutils.insertQuestion(questionTitle, calendar.timegm(time.gmtime()), questionText,
                                       category, session['username'], minReq)
                return redirect(url_for("forum"))
            elif request.form['submit'] == 'Find Answer':
                searchString = request.form['questionTitle'].encode('ascii', 'ignore').strip()
                searchTokens = searchString.split(' ')

                sort = dbutils.searchQuestions(searchTokens)

                results = []
                numResults = min(5, len(sort))
                for i in range(numResults):
                    results.append(sort[i])

                return render_template("postquestion.html", results=results, username=session['username'])

@app.route("/deletequestion/<qid>")
def deletequestion(qid = None):
    if qid is None:
        return redirect(url_for("error"))
    else:
        question = dbutils.getQuestionById(str(qid))
        if session['username'] == question[5]:
            dbutils.deleteQuestion(str(qid))
            return redirect(url_for("forum"))
        else:
            return redirect(url_for("error"))

@app.route("/deleteanswer/<aid>/<qid>")
def deleteanswer(aid = None, qid = None):
    if qid is None or aid is None:
        return redirect(url_for("error"))
    else:
        answer = dbutils.getAnswerById(str(aid))
        if session['username'] == answer[5]:
            dbutils.deleteAnswer(str(aid))
            return redirect(url_for("question", qid=qid))
        else:
            return redirect(url_for("error"))

@app.route("/question/<qid>", methods=["GET", "POST"])
def question(qid = None):
    if qid is None:
        return redirect(url_for("error"))
    else:
        if request.method == "GET":
            question = dbutils.getQuestionById(str(qid))
            questionArr = []
            for x in question:
                questionArr.append(x)
            questionArr[1] = time.ctime(questionArr[1])

            answers = dbutils.getAnswersByQuestion(str(qid))
            answersArr = []
            for x in answers:
                newArr = []
                for y in x:
                    newArr.append(y)
                newArr[1] = time.ctime(newArr[1])
                answersArr.append(newArr)
            if 'username' in session:
                minReq = question[6]
                rank = dbutils.getUserRank(session['username'])
                if rank >= minReq:
                    return render_template("question.html", username=session['username'],
                                           question=questionArr, answers=answersArr)
                else:
                    return render_template("question.html", username=session['username'],
                                           question=questionArr, answers=answersArr,
                                           error="You do not meet the minimum reputation that this user requested to answer this question")
            else:
                return render_template("question.html", question=questionArr, answers=answersArr)
        else:
            answerText = request.form['answer'].encode('ascii', 'ignore')
            dbutils.insertAnswer(calendar.timegm(time.gmtime()), answerText, qid, session['username'])
            return redirect(url_for("question", qid=qid))

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        if 'username' in session:
            return render_template("search.html", username=session['username'])
        else:
            return render_template("search.html")
    else:
        searchString = request.form['searchfield'].encode('ascii', 'ignore').strip()
        searchTokens = searchString.split(' ')

        sort = dbutils.searchQuestions(searchTokens)

        searchResults = []
        for entry in sort:
            searchResults.append(entry)
        if 'username' in session:
            return render_template("search.html", results=searchResults, username=session['username'], searchString=searchString)
        else:
            return render_template("search.html", results=searchResults, searchString=searchString)

@app.route("/vote/<aid>/<updown>")
def vote(aid = None, updown = None):
    if aid is None or updown is None or 'username' not in session:
        return redirect(url_for("error"))
    else:
        user = session['username']
        answer = dbutils.getAnswerById(aid)
        voted = dbutils.getVotes(user)[0].split()
        question = answer[4]
        userUp = answer[5]
        rank = dbutils.getUserRank(userUp)
        upvotes = answer[0]
        cred = dbutils.getUserCredits(userUp)
        if updown == "up":
            upvotes += 1
            rank += 1
            cred += .2
        elif updown == "down":
            upvotes -= 1
            rank -= 1
        if aid in voted:
            return redirect(url_for("question", qid=question))
        else:
            dbutils.updateAnswer(answer[2], upvotes)
            dbutils.updateUserRank(userUp, rank)
            dbutils.updateCredit(userUp, cred)
            voted.append(aid)
            putback = " ".join(voted)
            dbutils.updateVoted(user, putback)
            return redirect(url_for("question", qid=question))

@app.route("/user/<username>")
def user(username):
    if username == None:
        return redirect(url_for("error"))
    userinfo = dbutils.getUser(username)
    recentAnswers = dbutils.getAnswersByUser(username, "adate")[0:5]
    topAnswers = dbutils.getAnswersByUser(username, "upvotes")[0:5]
    recentQuestions = dbutils.getQuestionsByUser(username, "qdate")[0:5]
    if 'username' in session:
        return render_template("user.html", username = session['username'], userinfo=userinfo,
                               recentAnswers=recentAnswers, topAnswers = topAnswers, recentQuestions=recentQuestions)
    else:
        return render_template("user.html", userinfo=userinfo,
                               recentAnswers=recentAnswers, topAnswers = topAnswers, recentQuestions=recentQuestions)

@app.route("/user/<username>/allQuestions")
def allQuestions(username):
    if username == None:
        return redirect(url_for("error"))
    userinfo = dbutils.getUser(username)
    recentQuestions = dbutils.getQuestionsByUser(username, "date")
    if 'username' in session:
        return render_template("userQuestions.html", username = session['username'], recentQuestions=recentQuestions)
    else:
        return render_template("userQuestions.html", recentQuestions=recentQuestions)

@app.route("/user/<username>/allAnswers")
def allAnswers(username):
    if username == None:
        return redirect(url_for("error"))
    userinfo = dbutils.getUser(username)
    recentAnswers = dbutils.getAnswersByUser(username, "date")
    if 'username' in session:
        return render_template("userAnswers.html", username =session['username'], recentAnswers=recentAnswers)
    else:
        return render_template("userAnswers.html", recentAnswers=recentAnswers)

@app.route("/user/<username>/topAnswers")
def topAnswers(username):
    if username == None:
        return redirect(url_for("error"))
    userinfo = dbutils.getUser(username)
    topAnswers = dbutils.getAnswersByUser(username, "date")
    if 'username' in session:
        return render_template("userAnswers.html", username =session['username'], topAnswers=topAnswers)
    else:
        return render_template("userAnswers.html", topAnswers=topAnswers)

@app.route("/error")
def error():
    return render_template("error.html")

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=5000)

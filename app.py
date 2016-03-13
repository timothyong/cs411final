from flask import Flask, render_template, url_for, redirect, request, session
import dbutils
import time, calendar

app = Flask(__name__)
app.secret_key = "el em eff ay oh"

@app.route("/")
def index():
    if 'username' in session:
        return render_template("index.html", username=session['username'])
    else:
        return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login(redirectTo = None):
    if 'username' in session:
        return redirect(url_for("index"))
    else:
        if request.method == "GET":
            return render_template("login.html")
        else:
            username = request.form['username'].encode('ascii', 'ignore')
            password = request.form['password'].encode('ascii', 'ignore')

            retval = dbutils.login(username, password)
            if retval == "True":
                session['username'] = username
                if redirectTo == None:
                    redirect(url_for("index"))
                else:
                    redirect(url_for(redirectTo))
            else:
                return render_template("login.html", error = retval)

@app.route("/register", methods=["GET", "POST"])
def register(redirectTo = None):
    if 'username' in session:
        return redirect(url_for("index"))
    else:
        if request.method == "GET":
            return render_template("register.html")
        else:
            gender = request.form['gender']
            assert (gender in ["M", "F"])
            username = request.form['username'].encode('ascii', 'ignore')
            password = request.form['password'].encode('ascii', 'ignore')
            name = request.form['name'].encode('ascii', 'ignore')

            retval = dbutils.register(gender, username, password, name)
            if retval == "True":
                session['username'] = username
                if redirectTo == None:
                    redirect(url_for("index"))
                else:
                    redirect(url_for(redirectTo))
            else:
                return render_template("login.html", error = retval)

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if 'username' not in session:
        return redirect(url_for("login"))
    else:
        if request.method == "GET":
            userinfo = dbutils.getUser(session['username'])
            return render_template("settings.html", userinfo=userinfo)
        else:
            userinfo = dbutils.getUser(session['username'])
            password = request.form['password'].encode('ascii', 'ignore')
            newpassword = request.form['newpassword'].encode('ascii', 'ignore')
            retval = dbutils.changePassword(session['username'], password, newpassword)
            return render_template("settings.html", userinfo=userinfo, retval=retval)

@app.route("/forum")
@app.route("/forum/<category>")
def forum(category = None):
    if category == None:
        allQuestions = dbutils.getAllQuestions()
        if 'username' in session:
            return render_template("forum.html", username=session['username'], questions=allQuestions)
        else:
            return render_template("forum.html", questions=allQuestions)
    else:
        questions = dbutils.getQuestionsByCategory(category)
        if 'username' in session:
            return render_template("forum.html", username=session['username'], questions=questions)
        else:
            return render_template("forum.html", questions=questions)

@app.route("/question/<qid>", methods=["GET", "POST"])
def question(qid):
    if qid == None:
        return redirect(url_for("error"))
    else:
        if request.method == "GET":
            question = getQuestionById(qid)
            answers = getAnswersByQuestion(qid)
            if 'username' in session:
                return render_template("question.html", username=session['username'], question=question, answers=answers)
            else:
                return render_template("question.html", question=question, answers=answers)
        else:
            answerText = request.form['answer'].encode('ascii', 'ignore')
            dbutils.insertAnswer(calendar.timegm(time.gmtime()), answerText, qid, session['username'])
            question = getQuestionById(qid)
            answers = getAnswersByQuestion(qid)
            return render_template("question.html", username=session['username'], question=question, answers=answers)

@app.route("/user/<username>")
def user(username):
    if username == None:
        return redirect(url_for("error"))
    userinfo = dbutils.getUser(username)
    recentAnswers = dbutils.getAnswersByUser(username, "date")[0:5]
    topAnswers = dbutils.getAnswersByUser(username, "upvotes")[0:5]
    recentQuestions = dbutils.getQuestionsByUser(username, "date")[0:5]
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

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=5000)

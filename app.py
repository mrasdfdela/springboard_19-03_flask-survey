from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    return render_template("index.html", survey=satisfaction_survey)


@app.route('/',methods=['POST'])
def start_session():
    session['responses'] = []
    return redirect('/questions/0')


@app.route('/questions/<int:idx>')
def questions(idx):
    if len(session['responses']) >= len(satisfaction_survey.questions):
      return redirect('/thank-you')
    elif len(session['responses']) != idx:
      flash('You are trying to access an invalid question; redirecting to next question.','error')
      curr_responses = session['responses']
      return redirect(f'/questions/{len(curr_responses)}')
    else:
      question = satisfaction_survey.questions[idx]
      return render_template("question.html",survey=satisfaction_survey, idx=idx, question=question)


@app.route('/answers/<int:idx>', methods=['POST'])
def answers(idx):
    curr_responses = session['responses']
    curr_responses.append(request.form['survey_question'])
    session['responses'] = curr_responses

    new = int(idx) + 1
    if len(session['responses']) < len(satisfaction_survey.questions):
      return redirect(f"/questions/{new}")
    else:
      return redirect("/thank-you")


@app.route('/thank-you')
def thank_you():
    return render_template("thank_you.html")
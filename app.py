from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def home_page():
    return render_template("index.html", survey=satisfaction_survey)


@app.route('/questions/<int:idx>')
def questions(idx):
    if len(responses) >= len(satisfaction_survey.questions):
      return redirect('/thank-you')
    elif len(responses) != idx:
      flash('You are trying to access an invalid question; redirecting to next question.','error')
      return redirect(f'/questions/{len(responses)}')
    else:
      question = satisfaction_survey.questions[idx]
      return render_template("question.html",survey=satisfaction_survey, idx=idx, question=question)


@app.route('/answers/<int:idx>', methods=['POST'])
def answers(idx):
    new = int(idx) + 1
    responses.append(request.form['survey_question'])
    if len(responses) < len(satisfaction_survey.questions):
      return redirect(f"/questions/{new}")
    else:
      return redirect("/thank-you")


@app.route('/thank-you')
def thank_you():
    return render_template("thank_you.html")
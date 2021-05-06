from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def home_page():
    return render_template("index.html", survey=satisfaction_survey)

@app.route('/questions/<int:idx>')
def questions(idx):
  question = satisfaction_survey.questions[idx]
  return render_template("question.html",survey=satisfaction_survey,idx=idx, question=question)
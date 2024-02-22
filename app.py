from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES = []

@app.get("/")
def render_homepage():
    return render_template("survey_start.html", survey_title = survey.title,
                           survey_instructions = survey.instructions)

@app.post("/begin")
def change_page():
    return redirect("/questions/0")

@app.get("/questions/<int:index>")
def render_question_page(index):

    question = survey.questions[index]
    return render_question_page("question.html",
                                question = question)
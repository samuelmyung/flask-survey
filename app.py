from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES = []


@app.get("/")
def create_homepage():
    """Create homepage with a start of a survey"""
    RESPONSES.clear()
    return render_template("survey_start.html", survey_title=survey.title,
                           survey_instructions=survey.instructions)


@app.post("/begin")
def change_page():
    """Redirects us to the first question"""
    return redirect("/questions/0")


@app.get("/questions/<int:index>")
def create_question_page(index):
    """Create each subsequent question page and redirects to thank you page if
    no more questions"""
    if index >= len(survey.questions):
        return redirect("/thank_you")

    question = survey.questions[index]
    return render_template("question.html",
                           question=question)


@app.post("/answer")
def handle_answer():
    """Keeps track of user answers and redirects to next question"""
    RESPONSES.append(request.form['answer'])
    next_question_index = len(RESPONSES)

    return redirect(f"/questions/{next_question_index}")


@app.get("/thank_you")
def create_thank_you():
    """Creates a thank you page with the answered questions"""
    return render_template("completion.html", responses=RESPONSES, questions=survey.questions)

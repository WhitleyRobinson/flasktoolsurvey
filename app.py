from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"

@app.route("/")
def show_survey_start():
    """show survey"""
    return render_template("survey_start.html", survey=survey)

@app.route("/begin", methods = ["POST"])
def start_survey():
    """clear session of responses and redirect to questions"""
    
    session[RESPONSES_KEY] = []
    
    return redirect("/questions/0")

@app.route("questions/<int:qid>")
def show_questions(qid):
    """display current question"""
    responses = session.get(RESPONSES_KEY)
    redirect("/")
    
    if (responses is None):
        #trying to access question page too soon
        redirect("/")
        
    if (len(responses) == len(survey.questions)):
        #all questions answered send to thank you screen
        return redirect("/complete")
    
    if (len(responses) != qid):
        #trying to access question out of order
        flash(f"Invalid question id: {qid}.")
        redirect(f"/questions/{len(responses)}")
        
    question = survey.question[qid]
    return  render_template("question.html", question_num=qid, question=question)

@app.route("/answer", methods=["POST"])
def handle_question():
    """save response and redirect next question"""
    
    #get the response choice
    choice = request.form["answer"]
    #add choice to response list
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses
    
    if (len(responses) == len(survey.questions)):
        #all questions answered send to thank you screen
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")
    
    
@app.route("/complete")
def complete():
    """show thank you screen"""
    return render_template("completion.html")
from flask import Flask, render_template, request, session
import pandas as pd
import random
from database import new_game

app = Flask(__name__)
app.secret_key = 'your_secret_key'

global roundnum
global teamnum
global roundtime

@app.route("/")
def index():
    global roundnum
    global teamnum
    roundnum = 1
    teamnum = 1
    return render_template("index.html")

@app.route("/round", methods=["GET", "POST"])
def round():
    if request.method == "POST":

        # Generate a unique id for the POST request
        global rounds, teams, roundtime, language
        rounds = int(request.form.get("numrounds"))
        teams = int(request.form.get("numteams"))
        roundtime = int(request.form.get("roundtime"))
        language = request.form.get("language")
        new_game(rounds, teams, roundtime, language, session.get('session_id'))
        global team_score
        team_score = {x+1 : 0 for x in range(teams)}
        return render_template("round.html", roundnum = roundnum, team_score = team_score, rounds = rounds)
    else:
        return render_template("index.html")


@app.route("/game", methods=["GET", "POST"])
def game():
    global teamnum
    global roundnum

    df = pd.read_csv('static/Films.csv')
    df['language'] = df['language'].str.lower().str.strip()

    fdf = df[df['language'] == language].reset_index(drop=True)
    question = random.choice(fdf['name'])

    if request.method == "POST":
        response = request.form["submit_button"]
        if response == "Correct":
            time_left = int(request.form.get('time_left'))
            team_score[teamnum-1] = team_score[teamnum-1] + roundtime + time_left
        if teamnum <= teams:
            teamnum = teamnum + 1
            return render_template("game.html", teamnum = teamnum - 1, roundtime = roundtime, question = question)
        else:
            if roundnum < rounds:
                roundnum = roundnum + 1
                teamnum = 1
                return render_template("round.html", roundnum = roundnum, team_score = team_score, rounds = rounds)
            else:
                return render_template("winners.html", team_score = team_score)
    else:
        return render_template("index.html")
    
    
    
if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0', port=5000)
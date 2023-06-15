from flask import Flask, render_template, request, session
import pandas as pd
from database import new_game, execute, scores

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def random_question(language):
    df = pd.read_csv('static/Films.csv')
    df['language'] = df['language'].str.lower().str.strip()
    filtered_df = df[df['language'] == language]
    random_name = filtered_df['name'].sample().item()
    df = df[df['name'] != random_name].reset_index(drop=True)
    return random_name

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

@app.route("/round")
def round():
      global rounds, teams, roundtime, language
      rounds = int(request.args.get("numrounds"))
      teams = int(request.args.get("numteams"))
      roundtime = int(request.args.get("roundtime"))
      language = request.args.get("language")
      new_game(rounds, teams, roundtime, language, session.get('session_id'))
      game_id = execute("select max(id) as game_id from game_details")[0]['game_id']
      scores(game_id, teams)
      global team_score
      team_score = {x+1 : 0 for x in range(teams)}
      return render_template("round.html", roundnum = roundnum, team_score = team_score, rounds = rounds, game_id = game_id)


@app.route("/game/<game_id>", methods=["POST"])
def game(game_id):
    global teamnum
    global roundnum
    question = random_question(language)
    response = request.form["submit_button"]
    if response == "Correct":
        time_left = int(request.form.get('time_left'))
        team_score[teamnum-1] = team_score[teamnum-1] + roundtime + time_left
    if teamnum <= teams:
        teamnum = teamnum + 1
        return render_template("game.html", teamnum=teamnum-1, roundtime=roundtime, question=question, game_id=game_id)
    else:
        if roundnum < rounds:
            roundnum = roundnum + 1
            teamnum = 1
            return render_template("round.html", roundnum=roundnum, team_score=team_score, rounds=rounds, game_id=game_id)
        else:
            return render_template("winners.html", team_score=team_score)

    
    
    
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)
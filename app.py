from flask import Flask, render_template, request, session
import pandas as pd
from database import new_game, execute, scores, scores_dict, increase_team_score

app = Flask(__name__)
app.secret_key = 'desidesidesi'

def random_question(language):
    df = pd.read_csv('static/Films.csv')
    df['language'] = df['language'].str.lower().str.strip()
    filtered_df = df[df['language'] == language]
    random_name = filtered_df['name'].sample().item()
    df = df[df['name'] != random_name].reset_index(drop=True)
    return random_name

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/round")
def round():
      session.clear()
      session['rounds'] = int(request.args.get("numrounds"))
      session['teams'] = int(request.args.get("numteams"))
      session['roundtime'] = int(request.args.get("roundtime"))
      session['language'] = request.args.get("language")
      new_game(session['rounds'], session['teams'], session['roundtime'], session['language'], '101')
      session['game_id'] = execute("select max(id) as game_id from game_details")[0]['game_id']
      session['teamnum'] =  1
      session['roundnum'] =  1
      scores(session.get('game_id'), session['teams'])
      scores_dict(session.get('game_id'))
      return render_template("round.html", roundnum = session['roundnum'], team_score = scores_dict(session.get('game_id')), rounds = session.get('rounds'), game_id = session.get('game_id'))


@app.route("/game/<game_id>", methods=["POST"])
def game(game_id):
    question = random_question(session['language'])
    response = request.form["submit_button"]
    if response == "Correct":
        time_left = int(request.form.get('time_left'))
        increase_team_score(session.get('game_id'), session['teamnum'] - 1, session['roundtime']  + time_left)
    if session['teamnum'] <= session['teams']:
        session['teamnum'] = session['teamnum'] + 1
        return render_template("game.html", teamnum=session['teamnum']-1, roundtime=session.get('roundtime'), question=question, game_id=session.get('game_id'))
    else:
        if session['roundnum'] < session['rounds']:
            session['roundnum'] = session['roundnum'] + 1
            session['teamnum']  = 1
            return render_template("round.html", roundnum=session['roundnum'], team_score=scores_dict(session.get('game_id')), rounds=session.get('rounds'), game_id=session.get('game_id'))
        else:
            return render_template("winners.html", team_score=scores_dict(session.get('game_id')))

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0', port=5000)
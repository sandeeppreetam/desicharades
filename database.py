from sqlalchemy import create_engine, text
import os

# Create an engine
connection_string = os.getenv("connection_string")
engine = create_engine(connection_string)


def execute(sql):
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        columns = result.keys()
        rows = result.fetchall()
        output = [dict(zip(columns, row)) for row in rows]
        return output

def new_game(rounds, teams, roundtime, language, session_id):
    with engine.begin() as conn:
        query = text("INSERT INTO game_details (rounds, teams, roundtime, language, session_id) VALUES (:rounds, :teams, :roundtime, :language, :session_id)")

        try:
            conn.execute(query, {"rounds": rounds, "teams": teams, "roundtime": roundtime, "language": language, "session_id": session_id})
            conn.commit()  # Manually commit the transaction
            print("Values inserted successfully!")
        except Exception as e:
            conn.rollback()  # Rollback the transaction
            print(f"Error: {e}")

def scores(game_id, teamnum):
  curr_team = 1
  while curr_team <= teamnum:
    new_score(game_id, curr_team)
    curr_team = curr_team + 1
          
def new_score(game_id, team_id):
    with engine.begin() as conn:
        query = text("INSERT INTO scores (game_id, team_id, score) VALUES (:game_id, :team_id, :score)")
        try:
            conn.execute(query, {"game_id": game_id, "team_id": team_id, "score": 0})
            conn.commit()  # Manually commit the transaction
            print("Values inserted successfully!")
        except Exception as e:
            conn.rollback()  # Rollback the transaction
            print(f"Error: {e}")

def scores_dict(game_id):
  with engine.begin() as conn:
      query = text("SELECT team_id, score FROM scores WHERE game_id = :game_id")
      result = conn.execute(query, {"game_id": game_id})
      scores_dict = {row.team_id: row.score for row in result}
      return scores_dict

def increase_team_score(game_id, team_id, increase_amount):
    with engine.begin() as conn:
        query = text("UPDATE scores SET score = score + :increase_amount WHERE game_id = :game_id AND team_id = :team_id")
        conn.execute(query, {"increase_amount": increase_amount, "game_id": game_id, "team_id": team_id})

def current_game_details(id):
    with engine.begin() as conn:
      query = text("SELECT * FROM game_details WHERE id = :id")
      result = conn.execute(query, {"id": id})
      rows = result.fetchall()
      columns = result.keys()
      list = [dict(zip(columns, row)) for row in rows]
      return list[0]

print(current_game_details(47))
from sqlalchemy import create_engine, text
import os

# Create an engine
connection_string = os.getenv("connection_string")
engine = create_engine(connection_string, echo=True)


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


    
  
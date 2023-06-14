from sqlalchemy import create_engine, text
import os

# Create an engine
connection_string = os.getenv("connection_string")
engine = create_engine(connection_string, echo=True)


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


new_game(2, 3, 60, 'telugu', '10acwdd22')

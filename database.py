from sqlalchemy import create_engine, text
import os

# Create an engine
connection_string = os.getenv("connection_string")
engine = create_engine(connection_string, echo=True)

def execute(engine, sql):
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        columns = result.keys()
        rows = result.fetchall()
        output = [dict(zip(columns, row)) for row in rows]
        return output

films = execute(engine, "select * from films")
print(films[0])



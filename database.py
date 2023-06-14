from sqlalchemy import create_engine, text

# Create an engine
connection_string = 'mysql+mysqlconnector://up0zrppdknffht0xiwnj:pscale_pw_iI37EzH1qKEL7HFOHc22Xsty9pBBmhkFkdR0BL210sW@aws.connect.psdb.cloud/desicharades'
engine = create_engine(connection_string, echo=True)
conn = engine.connect()

# Execute SQL code
sql = text("SELECT * FROM films")
result = conn.execute(sql)

# Process the results
for row in result:
    print(row)

# Close the connection
conn.close()

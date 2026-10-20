def create_schema(connection):
    connection.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)")
    connection.execute("PRAGMA user_version = 1")
    connection.commit()

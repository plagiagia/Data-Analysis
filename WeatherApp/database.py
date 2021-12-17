import config
import psycopg2


def connect_to_database():
    """
    Creates the connection to the database and returns a cursor for query executions.
    """

    # Take the variables from the configuration file
    host = config.DB_HOST
    user = config.DB_USER
    password = config.DB_PASSWORD
    dbname = config.DB_NAME
    dbport = config.DB_PORT

    connection_template = "host={host} port={dbport} dbname={dbname} user={user} password={password} sslmode=disable".format(
        host=host, dbname=dbname, user=user, password=password, dbport=dbport)

    # Establish connection with an existing database
    connection = psycopg2.connect(connection_template)

    # Make cursor to execute queries
    connection.set_session(autocommit=True)
    cursor = connection.cursor()
    # Fetch DB name and print a message if connection is established.
    cursor.execute("SELECT current_database()")
    db_name = cursor.fetchone()
    print("You are connected with {} database".format(db_name))

    # Returns the cursors and the connections object
    return cursor, connection


# Insert data into the  weather table
def insert_data(city_name, wind_speed, clouds, temperature, pressure, humidity, temp_min, temp_max, description):
    """
    Insert data into the weather table.
    """

    # Create cursor and connection
    cursor, connection = connect_to_database()

    # Insert data into the database
    cursor.execute(
        """
        INSERT INTO data (city_name, wind_speed, clouds, temperature, pressure, humidity, temp_min, temp_max, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (city_name, wind_speed, clouds, temperature, pressure, humidity, temp_min, temp_max, description))


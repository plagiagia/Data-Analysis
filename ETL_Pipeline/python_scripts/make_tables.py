import os

import psycopg2


def connect_to_database():
    """
    Creates the connection to the database and returns a cursor for query executions.

    Because we need to connect to a DB to execute queries it is necessary either
    to have already our DB or to connect first to another DB and then create the
    actual DB and reset the connection to point to the newly created one.
    """

    # Take the variables from the environment
    host = os.environ.get("HOST", "")
    dbname = os.environ.get("DATABASE_NAME", "")
    user = os.environ.get("DB_USER", "")
    password = os.environ.get("DB_PASSWORD", "")

    connection_template = "host={host} dbname={dbname} user={user} password={password} sslmode=disable".format(
        host=host, dbname=dbname, user=user, password=password)

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


def drop_tables(cur, conn):
    """
    Drop the tables in case the function is called more than one time to avoid
    conflicts.
    """
    q = """
    DROP TABLE IF EXISTS restaurants RESTRICT;
    DROP TABLE IF EXISTS postal_codes RESTRICT;
    DROP TABLE IF EXISTS categories RESTRICT;
    """
    cur.execute(q)
    conn.commit()


def create_tables(cur, conn):
    q_table_postal_codes = """
    CREATE TABLE IF NOT EXISTS postal_codes (
    PostalCodeID SERIAL CONSTRAINT post_pk PRIMARY KEY,
    PostalCode VARCHAR (10));
    """

    q_table_categories = """
    CREATE TABLE IF NOT EXISTS categories (
    CategoryID SERIAL CONSTRAINT category_pk PRIMARY KEY,
    Category VARCHAR (50));
    """

    q_table_restaurants = """
    CREATE TABLE IF NOT EXISTS restaurants_ifo (
    id VARCHAR CONSTRAINT restaurant_pk PRIMARY KEY,
    RestaurantName VARCHAR (50),
    Reviews INT CONSTRAINT positive_reviews CHECK (reviews > 0),
    Rating DECIMAL (2, 1) CONSTRAINT positive_rating CHECK (rating > 0),
    Price VARCHAR(5),
    RestaurantPhone VARCHAR(20),
    RestaurantAddress VARCHAR(50),
    RestaurantLatitude DECIMAL (8, 6),
    RestaurantLongitude DECIMAL (8, 6),
    RestaurantDistance DECIMAL (7, 3) CONSTRAINT positive_distance CHECK (RestaurantDistance > 0),
    PostalCodeID INT,
    FOREIGN KEY (PostalCodeID) REFERENCES postal_codes (PostalCodeID),
    );
    """

    q_table_restaurants_and_categories = """
    CREATE TABLE IF NOT EXISTS rest_cats (
    RestaurantID VARCHAR,
    CategoryID INT,
    FOREIGN KEY (RestaurantID) REFERENCES restaurants_ifo (id),
    FOREIGN KEY (CategoryID) REFERENCES categories (CategoryID)
    );
"""

    q_list = [q_table_postal_codes,
              q_table_categories,
              q_table_restaurants,
              q_table_restaurants_and_categories]

    for each in q_list:
        cur.execute(each)
        conn.commit()


def close_connection(conn):
    """
    Closes the connection with the database
    """
    conn.close()


if __name__ == "__main__":
    cur, conn = connect_to_database()

    drop_tables(cur, conn)
    print("All tables are droped")

    create_tables(cur, conn)
    print("All tables are created")

    # Close the connection with the database
    close_connection(conn)

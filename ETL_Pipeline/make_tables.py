import psycopg2
import os


def connect_to_database():
    """
    Creates the connection to the database and returns a cursor for query executions.

    Because we need to connect to a DB to execute queries it is necessary either
    to have already our DB or to connect first to another DB and then create the
    actual DB and reset the connection to point to the newly created one.
    """

    # Take the variables from the environmnet
    host = os.environ.get("HOST", "127.0.0.1")
    dbname = os.environ.get("DATABASE_NAME", "the name of an existing DB")
    user = os.environ.get("DB_USER", "the actual user of the DB")
    password = os.environ.get("DB_PASSWORD", "the db password")

    connection_template = "host={host} dbname={dbname} user={user} password={password} sslmode=disable".format(
        host=host, dbname=dbname, user=user, password=password)

    # Establish connection with an existing database
    connection = psycopg2.connect(connection_template)

    # Make cursor to execute queries
    connection.set_session(autocommit=True)
    cursor = connection.cursor()
    # Fetch DB name and print a messege if connection is established.
    cursor.execute("SELECT current_database()")
    db_name = cursor.fetchone()
    print("You are connected with {} database".format(db_name))

    # Returns the cursos and the connections object
    return cursor, connection


def drop_tables(cur, conn):
    """
    Drop the tables in case the function is called more than one time to avoid
    conflicts.
    """
    q = """
    DROP TABLE IF EXISTS restaurants CASCADE;
    DROP TABLE IF EXISTS postal_codes CASCADE;
    DROP TABLE IF EXISTS categories CASCADE;
    """
    cur.execute(q)
    conn.commit()


def create_tables(cur, conn):

    q_table_postal_codes = """
    CREATE TABLE IF NOT EXISTS postal_codes (
    postal_code_id SERIAL CONSTRAINT post_key PRIMARY KEY,
    postal_code VARCHAR (10));
    """

    q_table_categories = """
    CREATE TABLE IF NOT EXISTS categories (
    category_id SERIAL CONSTRAINT category_key PRIMARY KEY,
    category VARCHAR (50));
    """

    q_table_restaurants = """
    CREATE TABLE IF NOT EXISTS restaurant (
    id VARCHAR CONSTRAINT restaurant_pk PRIMARY KEY,
    restaurant_name VARCHAR (100),
    reviews INT CHECK (reviews > 0),
    rating DECIMAL (2, 1),
    coordinates_latitude DECIMAL (8, 6),
    coordinates_longitude DECIMAL (8, 6),
    postal_code_id INT,
    category_id INT,
    FOREIGN KEY (postal_code_id) REFERENCES postal_codes (postal_code_id),
    FOREIGN KEY (category_id) REFERENCES categories (category_id)
    );
    """

    q_list = [q_table_postal_codes,
              q_table_categories,
              q_table_restaurants]

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

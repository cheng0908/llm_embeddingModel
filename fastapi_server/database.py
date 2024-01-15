# database.py
from mysql.connector import connect, Error
import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")

MYSQL_CONNECTION_CONFIG = {
    "host": "localhost",
    "user": MYSQL_USERNAME,
    "password": MYSQL_PASSWORD,
    "database": DATABASE_NAME,
    "port": 3306,
}

def get_db():
    try:
        connection = connect(**MYSQL_CONNECTION_CONFIG)
        cursor = connection.cursor(dictionary=True)
        yield connection, cursor
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise
    finally:
        cursor.close()
        connection.close()



def create_table():
    try:
        connection = connect(**MYSQL_CONNECTION_CONFIG)
        cursor = connection.cursor()

        # Define your table creation SQL statement here
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS upload_record (
            uid VARCHAR(36) PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            location VARCHAR(255),
            uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """

        cursor.execute(create_table_sql)
        connection.commit()
    except Error as e:
        print(f"Error creating table: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

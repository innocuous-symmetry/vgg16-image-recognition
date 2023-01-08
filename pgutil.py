import psycopg2, json
from config import Config

class PGUTIL:
    def __init__(self, config_file: Config = None):
        if config_file is None:
            load_config = Config()
            config_file = load_config.run()

        pg_dsn = config_file['pg_dsn']

        if pg_dsn is None:
            raise Exception("Insufficient data to establish PostgreSQL connection.")

        self.config_file = config_file

    def create_tables(self):
        pg_dsn = self.config_file['pg_dsn']

        print("Connecting to PostgreSQL...")

        # establish connection and create cursor
        conn = psycopg2.connect(pg_dsn)
        cur = conn.cursor()

        # create base tables
        create_label_table = """
        CREATE TABLE IF NOT EXISTS label (
            id INT PRIMARY KEY,
            name varchar
        );
        """
        
        create_photo_table = """
        CREATE TABLE IF NOT EXISTS photo (
            id INT PRIMARY KEY,
            path varchar,
            label varchar,
            matchstrength decimal,
            labelid INT REFERENCES label(id)
        );
        """

        # attempt to insert new tables
        print("Creating tables...")

        try:
            cur.execute(create_label_table)
            cur.execute(create_photo_table)
        except psycopg2.Error:
            raise Exception("Problem executing database table creation")

        print("Success!")

        # commit changes and close connection
        conn.commit()
        cur.close()
        conn.close()

        print("Connection closed.")
    
    def insert_data(self):
        pass
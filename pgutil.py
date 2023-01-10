import psycopg2, json
from config import Config

class PGUTIL:
    def __init__(self, config_file: Config = None, json_path: str = None):
        if config_file is None:
            load_config = Config()
            self.config_file = load_config.run()

        self.pg_dsn = config_file['pg_dsn']

        if json_path:
            self.json_path = json_path
        if config_file['pg_dsn'] is None:
            raise Exception("Insufficient data to establish PostgreSQL connection.")

    def create_tables(self):
        print("Connecting to PostgreSQL...")

        # establish connection and create cursor
        conn = psycopg2.connect(self.__dict__['pg_dsn'])
        cur = conn.cursor()

        # create base tables
        create_label_table = """
        CREATE TABLE IF NOT EXISTS label (
            id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name varchar UNIQUE,
            photocount INT
        );
        """
        
        create_photo_table = """
        CREATE TABLE IF NOT EXISTS photo (
            id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            filename varchar,
            guesslabel varchar,
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
    
    def insert_data(self, cur, analysis):
        self.create_tables()

        insert_label = """
        INSERT INTO label (name) VALUES (%s)
        ON CONFLICT (name) DO NOTHING;
        """

        filename = analysis['filename']
        guesslabel = analysis['topprediction']
        matchstrength = analysis['matchaccuracy']

        insert_photo = """
        INSERT INTO photo (filename, guesslabel, matchstrength, labelid) VALUES (
            %s, %s, %s, (
                SELECT id FROM label
                WHERE name = %s
            )
        );
        """

        update_label_count = """
        UPDATE label
        SET photocount = (
            SELECT COUNT(*) FROM photo
            WHERE guesslabel = %s
        )
        WHERE name = %s
        """

        try:
            cur.execute(insert_label, [guesslabel])
            cur.execute(insert_photo, [filename, guesslabel, matchstrength, guesslabel])
            cur.execute(update_label_count, [guesslabel, guesslabel])
        except psycopg2.Error:
            raise Exception("Problem inserting data for photo " + analysis['filename'])
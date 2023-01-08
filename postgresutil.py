import psycopg2
from config import Config

def postgresutil(config: Config):
    pg_config = config.pg_config

    if pg_config is None:
        raise Exception("Insufficient data to establish PostgreSQL connection.")

    conn = psycopg2.connect(pg_config.dsn)

    # TO DO: script to create these tables and interact with them

    """
    CREATE TABLE IF NOT EXISTS label (
        id INT PRIMARY KEY,
        name varchar
    );

    CREATE TABLE IF NOT EXISTS photo (
        id INT PRIMARY KEY,
        path varchar,
        label varchar,
        matchstrength decimal,
        labelid INT REFERENCES label(id)
    );
    """

    return conn
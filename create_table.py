import psycopg2
import os
import dotenv

dotenv.load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def create_table():
    conn = psycopg2.connect(DATABASE_URL)

    with conn.cursor() as cur:
        with open('database.sql') as f:
            cur.execute(f.read())

    conn.commit()
    conn.close()


create_table()

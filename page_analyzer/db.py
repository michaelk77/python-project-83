import psycopg2
import os
import dotenv

dotenv.load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def add_site(site):
    conn = psycopg2.connect(DATABASE_URL)

    with conn.cursor() as cur:
        cur.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s)",
                    (site["url"], 'now()'))
        conn.commit()
    conn.close()


def all_sites():
    conn = psycopg2.connect(DATABASE_URL)

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM urls")
        ans = cur.fetchall()
    conn.close()
    return ans


def get_site(site_id):
    conn = psycopg2.connect(DATABASE_URL)

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM urls WHERE id = %s", (site_id,))
        ans = cur.fetchone()
    conn.close()
    return ans


def get_site_by_name(site_name):
    conn = psycopg2.connect(DATABASE_URL)

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM urls WHERE name = %s", (site_name,))
        ans = cur.fetchone()
    conn.close()
    return ans

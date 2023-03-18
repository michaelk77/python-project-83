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
        cur.execute("""SELECT u.*, c.status_code, c.created_at
FROM urls u
LEFT JOIN (
  SELECT DISTINCT ON (url_id) *
  FROM url_checks
  ORDER BY url_id, id DESC
) c ON u.id = c.url_id
""")
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


def get_info_by_id(site_id):
    conn = psycopg2.connect(DATABASE_URL)

    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, status_code, created_at, h1, title, description "
            "FROM url_checks WHERE url_id = %s",
            (site_id,))
        ans = cur.fetchall()
    conn.close()
    return ans


def get_id_by_name(site_name):
    conn = psycopg2.connect(DATABASE_URL)

    with conn.cursor() as cur:
        cur.execute("SELECT id FROM urls WHERE name = %s", (site_name,))
        ans = cur.fetchone()
    conn.close()
    return ans


def add_check(site_id, status_code, h1, title, description):
    conn = psycopg2.connect(DATABASE_URL)

    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO url_checks (url_id, status_code, created_at, h1, "
            "title, description)"
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (site_id, status_code, 'now()', h1, title, description))
        conn.commit()
    conn.close()

import psycopg

import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")

logging.getLogger("psycopg").setLevel(logging.DEBUG)

DBCONSTR = "postgresql://postgres:secret@sam-db/sam-user-data"

def fetch_username_password_raw(username: str, password: str):
    with psycopg.connect(DBCONSTR) as connection:
        with connection.cursor() as cur:
            cur.execute(
            """
            SELECT *
            FROM USERS 
            WHERE username=%s AND password=%s
            """, (username, password))
            return cur.fetchone()

def fetch_userprofile_raw(username: str):
    with psycopg.connect(DBCONSTR) as connection:
        with connection.cursor() as cur:
            cur.execute(
            """
            SELECT userid, username, nationid, allianceid, title 
            FROM USERS 
            WHERE username=%s
            """, (username, ))
            return cur.fetchone()

#select_username_password("Jewma", "wrongpasswd")
#select_username_password("Jewma", "test")

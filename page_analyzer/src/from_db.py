import logging
import os
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
from typing import Optional

log = logging.getLogger(__name__)

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


def get_site(id: int) -> dict:
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        query = "SELECT * FROM urls WHERE id=%s"
        cursor.execute(query, (id,))
        site = cursor.fetchone()
        site = {} if site is None else dict(site)
    return site


def get_site_id(site_name: str) -> Optional[int]:
    with conn.cursor() as cursor:
        query = "SELECT id FROM urls WHERE name LIKE %s"
        cursor.execute(query, (site_name,))
        id = cursor.fetchone()
        id = id if id is None else id[0]
    return id


def add_site(site_name: str) -> int:
    with conn.cursor() as cursor:
        query = '''INSERT INTO urls (name, created_at)
            VALUES (% s, NOW()) RETURNING id'''
        cursor.execute(query, (site_name,))
        conn.commit()
        id = cursor.fetchone()[0]
    return id


def get_all_site() -> list:
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        query = "SELECT * FROM urls"
        cursor.execute(query)
        sites = cursor.fetchall()
        result = []
        if sites is not None:
            result = list(map(dict, sites))
    return result

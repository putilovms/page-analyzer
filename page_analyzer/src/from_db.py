import logging
import os
import psycopg2
from psycopg2.extras import NamedTupleCursor
from dotenv import load_dotenv
from typing import Optional, Any

log = logging.getLogger(__name__)

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


def get_site(id: int) -> Any:
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        query = "SELECT * FROM urls WHERE id=%s"
        cursor.execute(query, (id,))
        site = cursor.fetchone()
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
            VALUES (%s, NOW()) RETURNING id'''
        cursor.execute(query, (site_name,))
        conn.commit()
        id = cursor.fetchone()[0]
    return id


def get_all_site(sorting_asc: bool = False) -> list:
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        sort = 'ASC' if sorting_asc else 'DESC'
        query = f"SELECT * FROM urls ORDER BY created_at {sort}"
        cursor.execute(query)
        sites = cursor.fetchall()
    return sites

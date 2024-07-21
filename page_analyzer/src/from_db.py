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
        site = cursor.fetchmany(1)
        site = site[0] if site else None
    return site


def get_id_site(site_name: str) -> Optional[int]:
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


def get_all_sites(sorting_asc: bool = False) -> list:
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        sort = 'ASC' if sorting_asc else 'DESC'
        # query = f"SELECT * FROM urls ORDER BY created_at {sort}"
        query = f'''SELECT
                urls.id as id,
                urls.name as name,
                url_checks.status_code as status_code,
                url_checks.created_at as url_checks_created_at
            FROM
                urls
            INNER JOIN url_checks ON
                urls.id = url_checks.url_id
            WHERE
                url_checks.created_at in
            (
                SELECT
                    max(created_at) as created_at
                FROM
                    url_checks
                GROUP BY
                    url_id
            )
            ORDER BY urls.created_at {sort}'''
        cursor.execute(query)
        sites = cursor.fetchall()
    return sites


def add_check_site(url_id: int, check_data: dict) -> None:
    with conn.cursor() as cursor:
        query = '''INSERT INTO url_checks
                (url_id, status_code, h1, title, description, created_at)
            VALUES
                (%s, %s, %s, %s, %s, NOW())'''
        data = (
            url_id,
            check_data['status_code'],
            check_data['h1'],
            check_data['title'],
            check_data['description']
        )
        cursor.execute(query, data)
        conn.commit()
    return None


def get_checks(url_id: int, sorting_asc: bool = False) -> list:
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        sort = 'ASC' if sorting_asc else 'DESC'
        query = f'''SELECT * FROM url_checks
            WHERE url_id=%s
            ORDER BY created_at {sort}'''
        cursor.execute(query, (url_id,))
        checks = cursor.fetchall()
    return checks

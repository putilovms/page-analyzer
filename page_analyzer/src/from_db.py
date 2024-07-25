import logging
import os
import psycopg2
from psycopg2.extras import NamedTupleCursor
from psycopg2.extensions import connection
from dotenv import load_dotenv
from typing import Any

log = logging.getLogger(__name__)


def connect_to_db() -> connection:
    load_dotenv()
    DATABASE_URL = os.getenv('DATABASE_URL')
    return psycopg2.connect(DATABASE_URL)


def close_connection(conn: connection) -> None:
    conn.close()


def get_site(id: int, conn: connection) -> Any:
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        query = "SELECT * FROM urls WHERE id=%s"
        cursor.execute(query, (id,))
        site = cursor.fetchmany(1)
        site = site[0] if site else None
    return site


def get_id_site(site_name: str, conn: connection) -> int | None:
    with conn.cursor() as cursor:
        query = "SELECT id FROM urls WHERE name LIKE %s"
        cursor.execute(query, (site_name,))
        id = cursor.fetchone()
        id = id if id is None else id[0]
    return id


def add_site(site_name: str, conn: connection) -> int:
    with conn.cursor() as cursor:
        query = '''INSERT INTO urls (name, created_at)
            VALUES (%s, NOW()) RETURNING id'''
        cursor.execute(query, (site_name,))
        conn.commit()
        id = cursor.fetchone()[0]
    return id


def get_all_sites(conn: connection) -> list:
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        # query = f"SELECT * FROM urls ORDER BY created_at {sort}"
        query = '''SELECT
                    urls.id as id,
                    urls.name as name,
                    url_checks.status_code as status_code,
                    url_checks.created_at as url_checks_created_at
                FROM
                    urls
                LEFT JOIN url_checks ON
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
                ) or url_checks.created_at is Null
                ORDER BY urls.created_at DESC'''
        cursor.execute(query)
        sites = cursor.fetchall()
    return sites


def add_check_site(url_id: int, check_data: dict, conn: connection) -> None:
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


def get_checks(url_id: int, conn: connection) -> list:
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        query = '''SELECT * FROM url_checks
            WHERE url_id=%s
            ORDER BY created_at DESC'''
        cursor.execute(query, (url_id,))
        checks = cursor.fetchall()
    return checks

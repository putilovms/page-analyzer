import logging
import psycopg2
from psycopg2.extras import NamedTupleCursor
from psycopg2.extensions import connection
from typing import Any
from ..config import app

log = logging.getLogger(__name__)


def connect_to_db() -> connection:
    return psycopg2.connect(app.config['DATABASE_URL'])


def close_connection(conn: connection) -> None:
    conn.close()


def get_site(id: int, conn: connection) -> Any:
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        query = "SELECT * FROM urls WHERE id=%s"
        cursor.execute(query, (id,))
        site = cursor.fetchone()
    return site


def get_id_by_name(site_name: str, conn: connection) -> int | None:
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
        # query = '''SELECT
        #             urls.id as id,
        #             urls.name as name,
        #             url_checks.status_code as status_code,
        #             url_checks.created_at as url_checks_created_at
        #         FROM
        #             urls
        #         LEFT JOIN url_checks ON
        #             urls.id = url_checks.url_id
        #         WHERE
        #             url_checks.created_at in
        #         (
        #             SELECT
        #                 max(created_at) as created_at
        #             FROM
        #                 url_checks
        #             GROUP BY
        #                 url_id
        #         ) or url_checks.created_at is Null
        #         ORDER BY urls.created_at DESC'''
        query_to_urls = "SELECT * FROM urls ORDER BY created_at DESC"
        cursor.execute(query_to_urls)
        sites = cursor.fetchall()
        query_to_url_checks = '''SELECT DISTINCT ON (url_id)
                    url_id,
                    status_code,
                    created_at
                FROM
                    url_checks
                ORDER BY url_id, created_at DESC'''
        cursor.execute(query_to_url_checks)
        cheks = cursor.fetchall()
        result = []
        for site in sites:
            record = {}
            record['id'] = site.id
            record['name'] = site.name
            record['status_code'] = None
            record['url_checks_created_at'] = None
            for check in cheks:
                if site.id == check.url_id:
                    record['status_code'] = check.status_code
                    record['url_checks_created_at'] = check.created_at
            result.append(record)
    return result


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

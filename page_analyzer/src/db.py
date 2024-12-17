from typing import Any

import page_analyzer.constants as const
import psycopg2
from psycopg2.extensions import connection
from psycopg2.extras import NamedTupleCursor


def connect_to_db(dsn: str) -> connection:
    return psycopg2.connect(dsn)


def close_connection(conn: connection) -> None:
    conn.close()


def get_site_by_id(id: int, conn: connection) -> Any | None:
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        query = "SELECT * FROM urls WHERE id=%s"
        cursor.execute(query, (id,))
        site = cursor.fetchone()
    return site


def get_site_by_name(site_name: str, conn: connection) -> Any | None:
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        query = "SELECT * FROM urls WHERE name LIKE %s"
        cursor.execute(query, (site_name,))
        site = cursor.fetchone()
    return site


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
            record[const.SITE_ID] = site.id
            record[const.SITE_NAME] = site.name
            record[const.STATUS_CODE] = None
            record[const.URL_CHECKS_CREATED_AT] = None
            for check in cheks:
                if site.id == check.url_id:
                    record[const.STATUS_CODE] = check.status_code
                    record[const.URL_CHECKS_CREATED_AT] = check.created_at
                    break
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
            check_data[const.STATUS_CODE],
            check_data[const.HEADER],
            check_data[const.TITLE],
            check_data[const.DESCRIPTION]
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

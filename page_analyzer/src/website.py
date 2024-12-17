import logging
import urllib.parse
import validators
import page_analyzer.constants as const
from requests import get
from typing import Any
from requests import Response
from . import db
from ..src import parser

log = logging.getLogger(__name__)


def validate(site_name: str) -> str | None:
    if len(site_name) > 255:
        return 'URL превышает 255 символов'
    if not validators.url(site_name):
        return 'Некорректный URL'


def normalize(site_name: str) -> str:
    site_name = site_name.lower()
    url = urllib.parse.urlparse(site_name)
    parts = (url.scheme, url.hostname, '', '', '', '')
    new_url = urllib.parse.urlunparse(parts)
    return new_url


def add_new_site(site_name: str, dsn: str) -> tuple[int, bool]:
    site_name = normalize(site_name)
    conn = db.connect_to_db(dsn)
    site = db.get_site_by_name(site_name, conn)
    log.debug(f'Сайт = {site}')
    if site is None:
        id = db.add_site(site_name, conn)
        log.debug(f'Сайт добавлен. ID = {id}')
    else:
        id = site.id
    db.close_connection(conn)
    return id, site is not None


def get_all_sites(dsn: str) -> list:
    conn = db.connect_to_db(dsn)
    sites = db.get_all_sites(conn)
    db.close_connection(conn)
    log.debug(f'Данные о сайтах получены: {sites}')
    return sites


def check_site(id: int, dsn: str) -> Any:
    conn = db.connect_to_db(dsn)
    site = db.get_site_by_id(id, conn)
    log.debug(f'Данные сайта - {site}')
    if site:
        response = get(site.name)
        response.raise_for_status()
        check_data = get_check_data(response)
        log.debug(f'Данные проверки: {check_data}')
        db.add_check_site(id, check_data, conn)
        log.debug(f'Добавлена проверка для ID = {id}')
    db.close_connection(conn)
    return site


def get_check_data(response: Response) -> dict:
    check_data = {}
    check_data[const.STATUS_CODE] = response.status_code
    parsing_data = parser.parsing_site(response.content)
    check_data.update(parsing_data)
    return check_data


def get_site_and_checks(id: int, dsn: str) -> tuple:
    conn = db.connect_to_db(dsn)
    site = db.get_site_by_id(id, conn)
    log.debug(f'Данные сайта - {site}')
    checks = db.get_checks(id, conn)
    log.debug(f'Данные о проверках получены: {checks}')
    db.close_connection(conn)
    return site, checks

import logging
import urllib.parse
import validators
from typing import Any
from requests import Response
from ..src import from_db
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


def get_site(id: int) -> Any:
    conn = from_db.connect_to_db()
    site = from_db.get_site(id, conn)
    from_db.close_connection(conn)
    log.debug(f'Данные сайта - {site}')
    return site


def get_id_or_add(site_name: str) -> tuple:
    site_name = normalize(site_name)
    conn = from_db.connect_to_db()
    id = from_db.get_id_site(site_name, conn)
    log.debug(f'ID = {id}')
    is_exists = True
    if id is None:
        is_exists = False
        id = from_db.add_site(site_name, conn)
    log.debug(f'Сайт добавлен. ID = {id}')
    from_db.close_connection(conn)
    return id, is_exists


def get_all_sites() -> list:
    conn = from_db.connect_to_db()
    sites = from_db.get_all_sites(conn)
    from_db.close_connection(conn)
    log.debug(f'Данные о сайтах получены: {sites}')
    return sites


def check_site(id: int, response: Response) -> None:
    check_data = get_check_data(response)
    log.debug(f'Данные проверки: {check_data}')
    conn = from_db.connect_to_db()
    from_db.add_check_site(id, check_data, conn)
    from_db.close_connection(conn)
    log.debug(f'Добавлена проверка для ID = {id}')


def get_check_data(response: Response) -> dict:
    check_data = {}
    check_data['status_code'] = response.status_code
    parse = parser.parsing_site(response.content)
    check_data['h1'] = parser.get_h1(parse)
    check_data['title'] = parser.get_title(parse)
    check_data['description'] = parser.get_description(parse)
    return check_data


def get_checks(url_id: int) -> list:
    conn = from_db.connect_to_db()
    checks = from_db.get_checks(url_id, conn)
    from_db.close_connection(conn)
    log.debug(f'Данные о проверках получены: {checks}')
    return checks

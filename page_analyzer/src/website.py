import logging
import urllib.parse
from typing import Optional

log = logging.getLogger(__name__)


def normalize(site_name: str) -> str:
    site_name = site_name.lower()
    url = urllib.parse.urlparse(site_name)
    parts = [url.scheme, url.hostname, '', '', '', '']
    new_url = urllib.parse.urlunparse(parts)
    return new_url


def get_site(id: int, source) -> dict:
    site = source.get_site(id)
    log.debug(f'Данные сайта - {site}')
    return site


def get_site_id(site_name: str, source) -> Optional[int]:
    site_name = normalize(site_name)
    id = source.get_site_id(site_name)
    log.debug(f'ID = {id}')
    return id


def add_site(site_name: str, source) -> int:
    site_name = normalize(site_name)
    id = source.add_site(site_name)
    log.debug(f'Сайт успешно добавлен. ID = {id}')
    return id


def get_all_site(source) -> list:
    sites = source.get_all_site()
    return sites

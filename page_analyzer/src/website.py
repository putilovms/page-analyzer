import logging
import urllib.parse
import validators
from typing import Optional

log = logging.getLogger(__name__)


def is_valid(site_name: str) -> bool:
    if len(site_name) > 255:
        return False
    if not validators.url(site_name):
        return False
    return True


def normalize(site_name: str) -> str:
    site_name = site_name.lower()
    url = urllib.parse.urlparse(site_name)
    url = url.scheme + '://' + url.hostname
    return url


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

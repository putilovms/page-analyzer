import logging
import urllib.parse
from typing import Optional, Any

log = logging.getLogger(__name__)


def normalize(site_name: str) -> str:
    site_name = site_name.lower()
    url = urllib.parse.urlparse(site_name)
    parts = (url.scheme, url.hostname, '', '', '', '')
    new_url = urllib.parse.urlunparse(parts)
    return new_url


def get_site(id: int, source: Any) -> Any:
    site = source.get_site(id)
    log.debug(f'Данные сайта - {site}')
    return site


def get_id_site(site_name: str, source: Any) -> Optional[int]:
    site_name = normalize(site_name)
    id = source.get_id_site(site_name)
    log.debug(f'ID = {id}')
    return id


def add_site(site_name: str, source: Any) -> int:
    site_name = normalize(site_name)
    id = source.add_site(site_name)
    log.debug(f'Сайт добавлен. ID = {id}')
    return id


def get_all_sites(source: Any) -> list:
    sites = source.get_all_sites()
    log.debug(f'Данные о сайтах получены: {sites}')
    return sites


def check_site(site_id: int, source: Any) -> bool:
    site = source.get_site(site_id)
    if not site:
        return False
    source.check_site(site_id)
    log.debug(f'Проверка для ID = {site_id}')
    return True


def get_checks(url_id: int, source: Any) -> list:
    checks = source.get_checks(url_id)
    log.debug(f'Данные о проверках получены: {checks}')
    return checks

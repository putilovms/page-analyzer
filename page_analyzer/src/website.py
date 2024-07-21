import logging
import urllib.parse
from typing import Optional, Any
from requests import Response
from bs4 import BeautifulSoup

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


def check_site(id: int, response: Response, source: Any) -> None:
    check_data = get_check_data(response)
    log.debug(f'Данные проверки: {check_data}')
    source.add_check_site(id, check_data)
    log.debug(f'Добавлена проверка для ID = {id}')
    return None


def get_check_data(response: Response) -> dict:
    check_data = {}
    check_data['status_code'] = response.status_code
    soup = BeautifulSoup(response.content)
    h1 = '' if soup.h1 is None else soup.h1.string
    check_data['h1'] = h1
    title = '' if soup.title is None else soup.title.string
    check_data['title'] = title
    description = soup.find('meta', attrs={"name": "description"})
    description = '' if description is None else description.attrs['content']
    check_data['description'] = description
    return check_data


def get_checks(url_id: int, source: Any) -> list:
    checks = source.get_checks(url_id)
    log.debug(f'Данные о проверках получены: {checks}')
    return checks

from bs4 import BeautifulSoup
import page_analyzer.constants as const


def parsing_site(content: str) -> dict:
    bs = BeautifulSoup(content)
    result = {}
    h1 = '' if bs.h1 is None else bs.h1.text
    result[const.HEADER] = h1[:255]
    title = '' if bs.title is None else bs.title.text
    result[const.TITLE] = title[:255]
    description = bs.find('meta', attrs={"name": "description"})
    description = '' if description is None else description.attrs['content']
    result[const.DESCRIPTION] = description[:255]
    return result

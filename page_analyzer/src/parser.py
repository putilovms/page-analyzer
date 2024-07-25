from bs4 import BeautifulSoup


def parsing_site(content: str) -> BeautifulSoup:
    return BeautifulSoup(content)


def get_h1(parse: BeautifulSoup) -> str:
    h1 = '' if parse.h1 is None else parse.h1.string
    return h1[:255]


def get_title(parse: BeautifulSoup) -> str:
    title = '' if parse.title is None else parse.title.string
    return title[:255]


def get_description(parse: BeautifulSoup) -> str:
    description = parse.find('meta', attrs={"name": "description"})
    description = '' if description is None else description.attrs['content']
    return description[:255]

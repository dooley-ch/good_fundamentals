# *******************************************************************************************
#  File:  _wikipedia.py
#
#  Created: 01-06-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  01-06-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['SpEntry', 'get_sp600', 'get_sp400', 'get_sp500', 'get_sp100_tickers']

import attrs
import attrs.validators as validators
import requests
from bs4 import BeautifulSoup
from gf_lib.errors import RequestFailedError


@attrs.frozen
class SpEntry:
    ticker: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('^[A-Z.-]{1,12}$')],
                              converter=lambda value: value.upper())
    name: str = attrs.field(eq=False, validator=[validators.instance_of(str)])
    cik: str = attrs.field(eq=False, validator=[validators.instance_of(str)])
    sub_industry: str = attrs.field(eq=False, validator=[validators.instance_of(str)])


def _get_page(url: str) -> str:
    """
    This function downloads the page specified by the URL
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.text

    raise RequestFailedError(url, response.status_code)


def get_sp600(url: str) -> list[SpEntry] | None:
    contents = _get_page(url)

    if contents:
        constituuents: list[SpEntry] = list()

        soup = BeautifulSoup(contents, 'html.parser')
        table = soup.find('table', attrs={'id': 'constituents'})
        if table:
            tbody = table.find('tbody')
            if tbody:
                rows = tbody.find_all('tr')
                if rows:
                    for row in rows:
                        name = str(row.contents[1].text).strip()
                        ticker = str(row.contents[3].text).strip()
                        sub_industry = str(row.contents[7].text).strip()
                        cik = str(row.contents[11].text).strip()

                        if name == 'Company':
                            continue

                        constituuents.append(SpEntry(ticker, name, cik, sub_industry))
        return constituuents


def get_sp400(url: str) -> list[SpEntry] | None:
    contents = _get_page(url)

    if contents:
        constituuents: list[SpEntry] = list()

        soup = BeautifulSoup(contents, 'html.parser')
        table = soup.find('table', attrs={'id': 'constituents'})
        if table:
            tbody = table.find('tbody')
            if tbody:
                rows = tbody.find_all('tr')
                if rows:
                    for row in rows:
                        name = str(row.contents[1].text).strip()
                        ticker = str(row.contents[3].text).strip()
                        sub_industry = str(row.contents[7].text).strip()

                        if name == 'Security':
                            continue

                        constituuents.append(SpEntry(ticker, name, '0000000000', sub_industry))
        return constituuents


def get_sp500(url: str) -> list[SpEntry] | None:
    contents = _get_page(url)

    if contents:
        constituuents: list[SpEntry] = list()

        soup = BeautifulSoup(contents, 'html.parser')
        table = soup.find('table', attrs={'id': 'constituents'})
        if table:
            tbody = table.find('tbody')
            if tbody:
                rows = tbody.find_all('tr')
                if rows:
                    for row in rows:
                        name = str(row.contents[3].text).strip()
                        ticker = str(row.contents[1].text).strip()
                        sub_industry = str(row.contents[9].text).strip()
                        cik = str(row.contents[15].text).strip()

                        if name == 'Security':
                            continue

                        constituuents.append(SpEntry(ticker, name, cik, sub_industry))
        return constituuents


def get_sp100_tickers(url: str) -> list[str] | None:
    contents = _get_page(url)

    if contents:
        constituuents: list[str] = list()

        soup = BeautifulSoup(contents, 'html.parser')
        table = soup.find('table', attrs={'id': 'constituents'})
        if table:
            tbody = table.find('tbody')
            if tbody:
                rows = tbody.find_all('tr')
                if rows:
                    for row in rows:
                        name = str(row.contents[3].text).strip()
                        ticker = str(row.contents[1].text).strip()

                        if name == 'Name':
                            continue

                        constituuents.append(ticker)
        return constituuents

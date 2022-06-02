# *******************************************************************************************
#  File:  _sec.py
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
__all__ = ['get_sec_map']

import attrs
import attrs.validators as validators
import orjson
import requests
import orjson as json
from gf_lib.errors import RequestFailed

def _get_page(url: str) -> str:
    """
    This function downloads the page specified by the URL
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.text

    raise RequestFailed(url, response.status_code)


@attrs.frozen
class SecMap:
    cik_str: str = attrs.field(eq=False, validator=[validators.instance_of(str)],
                               converter=lambda value: str(value).zfill(10))
    ticker: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('^[A-Z.-]{1,12}$')],
                              converter=lambda value: value.upper())
    title: str = attrs.field(eq=False, validator=[validators.instance_of(str)])


def get_sec_map(url: str) -> list[SecMap] | None:
    contents = _get_page(url)

    if contents:
        data = json.loads(contents)

        records: list[SecMap] = list()

        for _, row in data.items():
            records.append(SecMap(**row))

        return records

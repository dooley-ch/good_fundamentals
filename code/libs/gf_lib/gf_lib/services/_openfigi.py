# *******************************************************************************************
#  File:  _openfigi.py
#
#  Created: 03-06-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  03-06-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['get_openfigi_code']

import orjson
import requests
from gf_lib.errors import RequestFailedError, RequestMaxFailedError, RequestResponseError


def get_openfigi_code(url: str, key: str, ticker: str) -> str | None:
    query = [{'idType': 'TICKER', 'idValue': ticker, 'exchCode': 'US'}]
    headers = {'Content-Type': 'text/json', 'X-OPENFIGI-APIKEY': key}

    response = requests.post(url=url, headers=headers, json=query)

    if response.status_code == 429:
        raise RequestMaxFailedError(url, response.status_code)

    if response.status_code != 200:
        raise RequestFailedError(url, response.status_code)

    content = orjson.loads(response.text)

    if 'error' in content[0]:
        msg: str = content[0]['error']
        if msg == 'No identifier found.':
            return None
        raise RequestResponseError(f"Error while seeking FIGI code for: {ticker} - {msg}")

    record = content[0]['data'][0]

    return record['figi']

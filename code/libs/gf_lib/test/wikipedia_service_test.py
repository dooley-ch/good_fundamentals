# *******************************************************************************************
#  File:  wikipedia_service_test.py
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

import gf_lib.services as services


def test_get_sp600() -> None:
    data = services.get_sp600('https://en.wikipedia.org/wiki/List_of_S%26P_600_companies')
    assert len(data) >= 595


def test_get_sp400() -> None:
    data = services.get_sp400('https://en.wikipedia.org/wiki/List_of_S%26P_400_companies')
    assert len(data) >= 395


def test_get_sp500() -> None:
    data = services.get_sp500('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    assert len(data) >= 495


def test_get_sp100() -> None:
    data = services.get_sp100_tickers('https://en.wikipedia.org/wiki/S%26P_100')
    assert len(data) >= 95

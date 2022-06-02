# *******************************************************************************************
#  File:  sec_service_test.py
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

from gf_lib.services import get_sec_map


def test_get_sec_map() -> None:
    data = get_sec_map('https://www.sec.gov/files/company_tickers.json')
    assert len(data) > 12_000

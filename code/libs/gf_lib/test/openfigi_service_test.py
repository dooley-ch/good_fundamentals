# *******************************************************************************************
#  File:  openfigi_service_test.py
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

import gf_lib.services as svc


class TestOpenFigi:
    def test_valid_values(self) -> None:
        codes: list[str] | None = svc.get_openfigi_codes('https://api.openfigi.com/v1/mapping',
                                                 'fe11251c-d169-441b-bcf9-2afbc914d806', ['IBM', 'JNJ', 'AAPL'])
        assert len(codes) == 3

    def test_missing_value(self) -> None:
        codes: list[svc.FigiCode] | None = svc.get_openfigi_codes('https://api.openfigi.com/v1/mapping',
                                                 'fe11251c-d169-441b-bcf9-2afbc914d806', ['IBM', 'JNJ', 'AAPL', 'XX45'])
        assert len(codes) == 4

        entry = codes[3]
        assert entry.ticker == 'XX45' and entry.figi is None


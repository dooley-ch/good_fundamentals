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
    def test_valid_value(self) -> None:
        code: str | None = svc.get_openfigi_code('https://api.openfigi.com/v1/mapping',
                                                 'fe11251c-d169-441b-bcf9-2afbc914d806', 'IBM')
        assert code == 'BBG000BLNNH6'

    def test_missing_value(self) -> None:
        code: str | None = svc.get_openfigi_code('https://api.openfigi.com/v1/mapping',
                                                 'fe11251c-d169-441b-bcf9-2afbc914d806', 'IBMABC')
        assert code is None

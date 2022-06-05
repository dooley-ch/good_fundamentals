# *******************************************************************************************
#  File:  validators_test.py
#
#  Created: 05-06-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  05-06-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

from gf_lib.datastore import get_master_list_validator


def test_master_list_validator() -> None:
    validator = get_master_list_validator()
    assert validator

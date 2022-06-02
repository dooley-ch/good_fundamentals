# *******************************************************************************************
#  File:  targets_test.py
#
#  Created: 02-06-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  02-06-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

import gf_loader.src.tasks as tasks


def test_collection_empty_target() -> None:
    target = tasks.CollectionPopulatedTarget('mongodb://localhost:27017', 'good_fundamentals_test', 'master_list')
    assert target.exists()

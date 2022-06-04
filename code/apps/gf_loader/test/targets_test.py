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

import pytest
from pymongo.database import Database
from pymongo.collection import Collection
import gf_lib.model as model
import gf_lib.datastore as ds
import gf_loader.src.tasks as tasks


class TestCollectionEmptyTarget:
    COLLECTION_NAME = 'master_list'

    @pytest.fixture
    def clear_collection(self, mongodb_connection, mongodb_database) -> None:
        db: Database = mongodb_connection[mongodb_database]
        coll: Collection = db[TestCollectionEmptyTarget.COLLECTION_NAME]
        coll.delete_many({})

    def test_collection_empty_target(self, clear_collection, mongodb_connection, mongodb_url, mongodb_database) -> None:
        db: Database = mongodb_connection[mongodb_database]
        store = ds.MasterListDatastore(db)
        record = model.Master(ticker='IBM', name='International Business Machines Corp.', cik='0123456789',
                        figi='012345678912', sector='Technology', sub_industry='Information Technology Services')

        record.indexes.append('SP500')
        record.indexes.append('SP100')
        assert store.insert(record)

        target = tasks.CollectionPopulatedTarget(mongodb_url, mongodb_database,
                                                 TestCollectionEmptyTarget.COLLECTION_NAME)
        assert target.exists()

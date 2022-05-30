# *******************************************************************************************
#  File:  _masterlist_datastore.py
#
#  Created: 30-05-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  30-05-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['MasterListDatastore']

from attrs import asdict
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertManyResult
from pymongo.errors import DuplicateKeyError
from gf_lib.model import Master, DocumentMetaData
from gf_lib.errors import DuplicateRecordError


class MasterListDatastore:
    _collection: Collection

    def __init__(self, database: Database) -> None:
        self._collection = database['master_list']

    def _to_master_record(self, value: dict) -> Master:
        value['metadata'] = DocumentMetaData(**value['metadata'])
        return Master(**value)

    def insert(self, value: Master) -> bool:
        try:
            results: InsertManyResult = self._collection.insert_one(asdict(value))
        except DuplicateKeyError:
            raise DuplicateRecordError(value.ticker)
        else:
            return results.acknowledged

    def get(self, ticker: str) -> Master | None:
        raw_data = self._collection.find_one({'ticker': ticker}, {'_id': 0})

        if raw_data:
            return self._to_master_record(raw_data)

    def find_by_sector(self, sector: str) -> list[Master] | None:
        raw_data = self._collection.find({'sector': sector}, {'_id': 0})

        if raw_data:
            return [self._to_master_record(row) for row in raw_data]

    def find_by_industry(self, sector: str, industry: str) -> list[Master] | None:
        raw_data = self._collection.find({'sector': sector, 'industry': industry}, {'_id': 0})

        if raw_data:
            return [self._to_master_record(row) for row in raw_data]

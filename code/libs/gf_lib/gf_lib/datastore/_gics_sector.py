# *******************************************************************************************
#  File:  _gics_sector.py
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
__all__ = ['GicsSectorDatastore']

from attrs import asdict
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertManyResult
from pymongo.errors import DuplicateKeyError
from gf_lib.model import GICSSector
from gf_lib.errors import DuplicateRecordError


class GicsSectorDatastore:
    _collection: Collection

    def __init__(self, database: Database) -> None:
        self._collection = database['gics_sector']

    def insert(self, value: GICSSector) -> bool:
        try:
            results: InsertManyResult = self._collection.insert_one(asdict(value))
        except DuplicateKeyError:
            raise DuplicateRecordError(value.name)
        else:
            return results.acknowledged

    def get(self, sector: str) -> GICSSector | None:
        raw_data = self._collection.find_one({'name': sector}, {'_id': 0})

        if raw_data:
            return GICSSector(**raw_data)

    def get_all(self) -> list[GICSSector] | None:
        raw_data = self._collection.find({}, {'_id': 0})

        if raw_data:
            return [GICSSector(**row) for row in raw_data]

    def clear(self) -> None:
        self._collection.delete_many({})

    def count(self) -> int:
        row_count = self._collection.count_documents({})
        if row_count is None:
            return 0

        return row_count

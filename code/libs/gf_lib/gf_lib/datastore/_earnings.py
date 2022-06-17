# *******************************************************************************************
#  File:  _earnings.py
#
#  Created: 15-06-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  15-06-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['EarningsFileDatastore']

from attrs import asdict
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertManyResult, DeleteResult
from pymongo.errors import DuplicateKeyError
from gf_lib.model import Earnings
from gf_lib.errors import DuplicateRecordError


class EarningsFileDatastore:
    _collection: Collection

    def __init__(self, database: Database) -> None:
        self._collection = database['earnings']

    def insert(self, value: Earnings) -> bool:
        try:
            results: InsertManyResult = self._collection.insert_one(asdict(value))
        except DuplicateKeyError:
            raise DuplicateRecordError(value.ticker)
        else:
            return results.acknowledged

    def get(self, ticker: str) -> Earnings | None:
        raw_data = self._collection.find_one({'ticker': ticker}, {'_id': 0})

        if raw_data:
            return Earnings(**raw_data)

    def clear(self) -> bool:
        result: DeleteResult = self._collection.delete_many({})
        return result.acknowledged

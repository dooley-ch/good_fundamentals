# *******************************************************************************************
#  File:  _statement.py
#
#  Created: 31-05-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  31-05-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['AccountingStatemetDatastore']

from attrs import asdict
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertManyResult
from pymongo.errors import DuplicateKeyError
from gf_lib.model import AccountingStatement, PeriodType
from gf_lib.errors import DuplicateRecordError


class AccountingStatemetDatastore:
    _collection: Collection

    def __init__(self, database: Database, collection: str) -> None:
        self._collection = database[collection]

    def insert(self, value: AccountingStatement) -> bool:
        try:
            results: InsertManyResult = self._collection.insert_one(asdict(value))
        except DuplicateKeyError:
            raise DuplicateRecordError(value.ticker)
        else:
            return results.acknowledged

    def get(self, ticker: str, period: PeriodType) -> AccountingStatement | None:
        raw_data = self._collection.find_one({'ticker': ticker, 'period_type': period.value}, {'_id': 0})

        if raw_data:
            return AccountingStatement(**raw_data)

    def clear(self) -> None:
        self._collection.delete_many({})

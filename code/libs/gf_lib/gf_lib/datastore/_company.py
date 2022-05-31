# *******************************************************************************************
#  File:  _company.py
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
__all__ = ['CompanyDatastore']

from attrs import asdict
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertManyResult
from pymongo.errors import DuplicateKeyError
from gf_lib.model import Company
from gf_lib.errors import DuplicateRecordError


class CompanyDatastore:
    _collection: Collection

    def __init__(self, database: Database) -> None:
        self._collection = database['companies']

    def insert(self, value: Company) -> bool:
        try:
            results: InsertManyResult = self._collection.insert_one(asdict(value))
        except DuplicateKeyError:
            raise DuplicateRecordError(value.ticker)
        else:
            return results.acknowledged

    def get(self, ticker: str) -> Company | None:
        raw_data = self._collection.find_one({'ticker': ticker}, {'_id': 0})

        if raw_data:
            return Company(**raw_data)

    def clear(self) -> None:
        self._collection.delete_many({})

# *******************************************************************************************
#  File:  _master.py
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
__all__ = ['MasterDatastore']

from attrs import asdict
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database
from pymongo.results import InsertManyResult, DeleteResult, UpdateResult
from pymongo.errors import DuplicateKeyError
from gf_lib.model import Master
from gf_lib.errors import DuplicateRecordError


class MasterDatastore:
    _collection: Collection

    def __init__(self, database: Database) -> None:
        self._collection = database['master']

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
            return Master(**raw_data)

    def get_tickers(self) -> list[str] | None:
        cursor: Cursor = self._collection.find({},{'ticker': 1})

        if cursor:
            return [row['ticker'] for row in cursor]

    def update_cik(self, ticker: str, value: str) -> bool:
        record = self.get(ticker)

        if record:
            record.metadata.prep_for_update()

            filter = {'ticker': record.ticker}
            new_values = {'$set': {'cik': value, 'metadata.lock_version': record.metadata.lock_version,
                                   'metadata.updated_at': record.metadata.updated_at}}

            result: UpdateResult = self._collection.update_one(filter, new_values)
            return result.acknowledged

        return False

    def update_figi(self, ticker: str, value: str) -> bool:
        record = self.get(ticker)

        if record:
            record.metadata.prep_for_update()

            filter = {'ticker': record.ticker}
            new_values = {'$set': {'figi': value, 'metadata.lock_version': record.metadata.lock_version,
                                   'metadata.updated_at': record.metadata.updated_at}}

            result: UpdateResult = self._collection.update_one(filter, new_values)
            return result.acknowledged

        return False

    def clear(self) -> bool:
        result: DeleteResult = self._collection.delete_many({})
        return result.acknowledged
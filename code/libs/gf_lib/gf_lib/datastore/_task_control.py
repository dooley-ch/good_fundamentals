# *******************************************************************************************
#  File:  _task_control.py
#
#  Created: 04-06-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  04-06-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['TaskTrackingDatastore']

from attrs import asdict
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertManyResult, UpdateResult, DeleteResult
from pymongo.errors import DuplicateKeyError
from gf_lib.model import TaskTracking
from gf_lib.errors import DuplicateRecordError


class TaskTrackingDatastore:
    _collection: Collection

    def __init__(self, database: Database) -> None:
        self._collection = database['task_tracking']

    def insert(self, value: TaskTracking) -> bool:
        try:
            results: InsertManyResult = self._collection.insert_one(asdict(value))
        except DuplicateKeyError:
            raise DuplicateRecordError(value.sector)
        else:
            return results.acknowledged

    def get(self) -> TaskTracking | None:
        raw_data = self._collection.find_one({}, {'_id': 0})

        if raw_data:
            return TaskTracking(**raw_data)

    def update_cik_flag(self, value: bool) -> bool:
        new_value = {'$set': {'cik_loaded': value}}
        result: UpdateResult = self._collection.update_one({}, new_value)
        return result.acknowledged

    def update_figi_flag(self, value: bool) -> bool:
        new_value = {'$set': {'figi_loaded': value}}
        result: UpdateResult = self._collection.update_one({}, new_value)
        return result.acknowledged

    def update_master_flag(self, value: bool) -> bool:
        new_value = {'$set': {'master_loaded': value}}
        result: UpdateResult = self._collection.update_one({}, new_value)
        return result.acknowledged

    def update_earnings_flag(self, value: bool) -> bool:
        new_value = {'$set': {'earnings_file_loaded': value}}
        result: UpdateResult = self._collection.update_one({}, new_value)
        return result.acknowledged

    def clear(self) -> bool:
        result: DeleteResult =self._collection.delete_many({})
        return result.acknowledged

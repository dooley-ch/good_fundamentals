# *******************************************************************************************
#  File:  _gics_classification.py
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
__all__ = ['GicsClassificationDatastore']

from attrs import asdict
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertManyResult
from pymongo.errors import DuplicateKeyError
from gf_lib.model import GicsClassification, DocumentMetaData
from gf_lib.errors import DuplicateRecordError


class GicsClassificationDatastore:
    _collection: Collection

    def __init__(self, database: Database) -> None:
        self._collection = database['gics_classifications']

    def _to_gics_classification_record(self, value: dict) -> GicsClassification:
        value['metadata'] = DocumentMetaData(**value['metadata'])
        return GicsClassification(**value)

    def insert(self, value: GicsClassification) -> bool:
        try:
            results: InsertManyResult = self._collection.insert_one(asdict(value))
        except DuplicateKeyError:
            raise DuplicateRecordError(value.sector)
        else:
            return results.acknowledged

    def get(self, sector: str) -> GicsClassification | None:
        raw_data = self._collection.find_one({'sector': sector}, {'_id': 0})

        if raw_data:
            return self._to_gics_classification_record(raw_data)

    def get_all(self) -> list[GicsClassification] | None:
        raw_data = self._collection.find({}, {'_id': 0})

        if raw_data:
            return [self._to_gics_classification_record(row) for row in raw_data]

    def clear(self) -> None:
        self._collection.delete_many({})
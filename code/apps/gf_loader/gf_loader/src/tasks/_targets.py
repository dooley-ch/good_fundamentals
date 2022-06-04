# *******************************************************************************************
#  File:  _targets.py
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
__all__ = ['CollectionPopulatedTarget']

from loguru import logger
import luigi
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection


class CollectionPopulatedTarget(luigi.Target):
    """
    This target checks if a collection contains documents
    """
    _url: str
    _database: str
    _collection: str

    def __init__(self, url: str, database: str, collection: str) -> None:
        super().__init__()

        self._url = url
        self._database = database
        self._collection = collection

    @logger.catch(reraise=True)
    def exists(self):
        client: MongoClient = MongoClient(self._url)

        db_names = client.list_database_names()
        if not self._database in db_names:
            raise ValueError(f"Database not found: {self._database}")

        database: Database = client[self._database]

        coll_names = database.list_collection_names()
        if not self._collection in coll_names:
            raise ValueError(f"Collection not found: {self._collection}")

        coll: Collection = database[self._collection]

        return coll.count_documents({}) > 0

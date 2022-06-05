# *******************************************************************************************
#  File:  _datastore_utils.py
#
#  Created: 05-06-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  05-06-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['database_exists', 'create_database', 'drop_database', 'collection_exists',
           'create_collection', 'drop_collection']

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

def database_exists(client: MongoClient | str, name: str) -> bool:
    """
    This function checks if the database exists
    """
    if isinstance(client, str):
        client = MongoClient(client)

    database_names = client.list_database_names()
    return name in database_names


def create_database(client: MongoClient | str, name: str) -> Database:
    """
    This function creates the database, if it does not exist and returns it
    """
    if isinstance(client, str):
        client = MongoClient(client)

    return client[name]


def drop_database(client: MongoClient | str, name: str) -> None:
    """
    This function drops the given database
    """
    if isinstance(client, str):
        client = MongoClient(client)

    if database_exists(client, name):
        client.drop_database(name)


def collection_exists(db: Database, name: str) -> bool:
    """
    This function checks if a collection exists in the given database
    """
    collection_names = db.list_collection_names()
    return name in collection_names


def create_collection(db: Database, name: str) -> Collection:
    """
    This function creates and returns a collection
    """
    db.create_collection(name)
    return db[name]


def drop_collection(db: Database, name: str) -> None:
    """
    This function drops a collection, if it exists
    """
    if collection_exists(db, name):
        db.drop_collection(name)

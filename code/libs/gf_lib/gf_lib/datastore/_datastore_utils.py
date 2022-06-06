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
__all__ = ['database_exists', 'create_database', 'drop_database', 'collection_exists', 'drop_collection',
           'get_master_list_validator', 'get_task_control_validator', 'create_master_list', 'create_task_control',
           'create_gics']

from collections import OrderedDict

import pymongo
from pymongo import MongoClient
from pymongo.database import Database

_gcis = {'$jsonSchema':
             {'bsonType': 'object',
              'title': 'gics',
              'required': ['id', 'name', 'industry_groups'],
              'properties': {
                  'id': {'bsonType': 'int'},
                  'name': {'bsonType': 'string'},
                  'industry_groups': {
                      'bsonType': 'array',
                      'items': {
                          'title': 'industry_group',
                          'required': ['id', 'name', 'industries'],
                          'properties': {
                              'id': {'bsonType': 'int'},
                              'name': {'bsonType': 'string'},
                              'industries': {
                                  'bsonType': 'array',
                                  'items': {
                                      'title': 'Industry',
                                      'required': ['id', 'name', 'sub_industries'],
                                      'properties': {
                                          'id': {'bsonType': 'int'},
                                          'name': {'bsonType': 'string'},
                                          'sub_industries': {
                                              'bsonType': 'array',
                                              'items': {
                                                  'title': 'item',
                                                  'required': ['id', 'name'],
                                                  'properties': {
                                                      'id': {'bsonType': 'int'},
                                                      'name': {'bsonType': 'string'}
                                                  }
                                              }
                                          }
                                      }
                                  }
                              }
                          }
                      }
                  }
              }
              }
         }

_metadata: dict[str, dict] = {
    "lock_version": {"bsonType": 'int', "required": True},
    "created_at": {"bsonType": 'date', "required": True},
    "updated_at": {"bsonType": 'date', "required": True},
}

_master_list: dict[str, dict] = {
    "ticker": {"bsonType": 'string', "required": True, "minlength": 1},
    "name": {"bsonType": 'string', "required": True, "minlength": 1},
    "cik": {"bsonType": 'string', "required": True, "minlength": 1},
    "figi": {"bsonType": 'string', "required": True, "minlength": 1},
    "sub_industry": {"bsonType": 'string', "required": True, "minlength": 1}
}

_task_control: dict[str, dict] = {
    "cik_loaded": {"bsonType": 'bool', "required": True},
    "figi_loaded": {"bsonType": 'bool', "required": True},
}


def _get_document_validator() -> dict[str, dict]:
    validator = {'bsonType': 'object', 'title': 'document_metadata', 'properties': {}}
    required = []

    for field_key in _metadata:
        field = _metadata[field_key]
        properties = {'bsonType': field['bsonType']}
        minimum = field.get('minlength')

        if type(minimum) == int:
            properties['minimum'] = minimum

        if field.get('required') is True:
            required.append(field_key)

        validator['properties'][field_key] = properties

    if len(required) > 0:
        validator['required'] = required

    return validator


def _get_validator(collection: str, schema: dict[str, dict]) -> dict[str, dict]:
    validator = {'$jsonSchema': {'bsonType': 'object', 'title': collection, 'properties': {}}}
    required = []

    for field_key in schema:
        field = schema[field_key]
        properties = {'bsonType': field['bsonType']}
        minimum = field.get('minlength')

        if type(minimum) == int:
            properties['minimum'] = minimum

        if field.get('required') is True:
            required.append(field_key)

        validator['$jsonSchema']['properties'][field_key] = properties

    metadata = _get_document_validator()
    required.append('metadata')

    validator['$jsonSchema']['required'] = required
    validator['$jsonSchema']['properties']['metadata'] = metadata

    return validator


def get_master_list_validator() -> dict[str, dict]:
    """
    This function returns the MongoDb schema validator for the master_list
    """
    return _get_validator('master_list', _master_list)


def get_task_control_validator() -> dict[str, dict]:
    """
    This function returns the MongoDb schema validator for the task_control
    """
    return _get_validator('task_control', _task_control)


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


def drop_collection(db: Database, name: str) -> None:
    """
    This function drops a collection, if it exists
    """
    if collection_exists(db, name):
        db.drop_collection(name)


def create_master_list(db: Database) -> None:
    collection_name: str = 'master_list'
    if collection_exists(db, collection_name):
        drop_collection(db, collection_name)

    validator = get_master_list_validator()

    db.create_collection(collection_name)

    query = [('collMod', collection_name), ('validator', validator)]
    db.command(OrderedDict(query))

    coll = db.get_collection(collection_name)
    coll.create_index([("ticker", pymongo.ASCENDING)], name=f"{collection_name}_unique_ticker", unique=True)
    coll.create_index([("ticker", pymongo.ASCENDING), ("name", pymongo.ASCENDING), ("cik", pymongo.ASCENDING),
                       ("figi", pymongo.ASCENDING), ("sub_industry", pymongo.ASCENDING)],
                      name=f"{collection_name}_ticker")
    coll.create_index([("cik", pymongo.ASCENDING), ("ticker", pymongo.ASCENDING), ("name", pymongo.ASCENDING),
                       ("figi", pymongo.ASCENDING), ("sub_industry", pymongo.ASCENDING)],
                      name=f"{collection_name}_cik")
    coll.create_index([("figi", pymongo.ASCENDING), ("ticker", pymongo.ASCENDING), ("name", pymongo.ASCENDING),
                       ("cik", pymongo.ASCENDING), ("sub_industry", pymongo.ASCENDING)],
                      name=f"{collection_name}_figi")
    coll.create_index([("sub_industry", pymongo.ASCENDING), ("ticker", pymongo.ASCENDING), ("name", pymongo.ASCENDING),
                       ("cik", pymongo.ASCENDING), ("figi", pymongo.ASCENDING)], name=f"{collection_name}_sub_industry")


def create_task_control(db: Database) -> None:
    collection_name: str = 'task_control'
    if collection_exists(db, collection_name):
        drop_collection(db, collection_name)

    validator = get_task_control_validator()

    db.create_collection(collection_name)

    query = [('collMod', collection_name), ('validator', validator)]
    db.command(OrderedDict(query))


def create_gics(db: Database) -> None:
    collection_name: str = 'gics'
    if collection_exists(db, collection_name):
        drop_collection(db, collection_name)

    validator = _gcis

    db.create_collection(collection_name)

    query = [('collMod', collection_name), ('validator', validator)]
    db.command(OrderedDict(query))

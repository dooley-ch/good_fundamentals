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
__all__ = ['MasterLoadedTarget', 'CikLoadedTarget', 'FigiLoadedTarget', 'EarningsFileLoadedTarget',
           'CollectionHasDataTarget']


from typing import Callable
from loguru import logger
import luigi
from pymongo import MongoClient
from pymongo.database import Database
from gf_lib.datastore import TaskTrackingDatastore, GicsSectorDatastore
from gf_lib.model import TaskTracking


class CollectionHasDataTarget(luigi.Target):
    _url: str
    _database: str

    def __init__(self, url: str, database: str):
        super().__init__()
        self._url = url
        self._database = database

    def exists(self) -> bool:
        client: MongoClient = MongoClient(self._url)
        db_names = client.list_database_names()
        if self._database not in db_names:
            raise ValueError(f"Database not found: {self._database}")

        database: Database = client[self._database]
        store = GicsSectorDatastore(database)

        return store.count() > 0


class _CheckTaskTrackingFlagTarget(luigi.Target):
    _check_flag: Callable[[TaskTracking], bool]
    _url: str
    _database: str

    def __init__(self, url: str, database: str, check_flag: Callable[[TaskTracking], bool]) -> None:
        super().__init__()

        self._url = url
        self._database = database
        self._check_flag = check_flag

    @logger.catch(reraise=True)
    def exists(self) -> bool:
        client: MongoClient = MongoClient(self._url)
        db_names = client.list_database_names()
        if self._database not in db_names:
            raise ValueError(f"Database not found: {self._database}")

        database: Database = client[self._database]

        ds = TaskTrackingDatastore(database)
        record: TaskTracking = ds.get()

        if record is None:
            raise ValueError('Task Tracking record not found')

        return self._check_flag(record)


class MasterLoadedTarget(_CheckTaskTrackingFlagTarget):
    @staticmethod
    def check_master_loaded_flag(value: TaskTracking) -> bool:
        return value.master_loaded

    def __init__(self, url: str, database: str):
        super().__init__(url, database, MasterLoadedTarget.check_master_loaded_flag)


class CikLoadedTarget(_CheckTaskTrackingFlagTarget):
    @staticmethod
    def check_cik_loaded_flag(value: TaskTracking) -> bool:
        return value.cik_loaded

    def __init__(self, url: str, database: str):
        super().__init__(url, database, CikLoadedTarget.check_cik_loaded_flag)


class FigiLoadedTarget(_CheckTaskTrackingFlagTarget):
    @staticmethod
    def check_figi_loaded_flag(value: TaskTracking) -> bool:
        return value.figi_loaded

    def __init__(self, url: str, database: str):
        super().__init__(url, database, FigiLoadedTarget.check_figi_loaded_flag)


class EarningsFileLoadedTarget(_CheckTaskTrackingFlagTarget):
    @staticmethod
    def check_earnings_file_loaded_flag(value: TaskTracking) -> bool:
        return value.earnings_file_loaded

    def __init__(self, url: str, database: str):
        super().__init__(url, database, EarningsFileLoadedTarget.check_earnings_file_loaded_flag)

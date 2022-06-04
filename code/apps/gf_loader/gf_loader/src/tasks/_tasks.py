# *******************************************************************************************
#  File:  _tasks.py
#
#  Created: 03-06-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  03-06-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['PopulateMasterListTask', 'ResetTask', 'LoadCikCodesTask', 'LoadFigiCodesTask', 'BuildMasterListTask']

import gf_lib.datastore as ds
import gf_lib.model as model
import gf_lib.services as svc
import luigi
from attrs import asdict
from gf_lib.utils import log_activity
from loguru import logger
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from ._targets import CollectionPopulatedTarget, FigiLoadTaskCompletedTarget, CikLoadTaskCompletedTarget


class ResetTask(luigi.Task):
    url = luigi.Parameter()
    database = luigi.Parameter()

    def requires(self):
        pass

    def run(self):
        client: MongoClient = MongoClient(self.url)
        database: Database = client[self.database]

        # Task Control
        coll: Collection = database['task_control']
        coll.delete_many({})
        record = model.TaskControl()
        coll.insert_one(asdict(record))

        # Master List
        coll: Collection = database['master_list']
        coll.delete_many({})

    def output(self):
        pass


class PopulateMasterListTask(luigi.Task):
    """
    This task populates the master list collection from
    the external sources
    """
    url = luigi.Parameter()
    database = luigi.Parameter()
    collection = luigi.Parameter()

    sp_600_url = luigi.Parameter()
    sp_400_url = luigi.Parameter()
    sp_500_url = luigi.Parameter()
    sp_100_url = luigi.Parameter()

    def requires(self):
        pass

    def run(self):
        client: MongoClient = MongoClient(self.url)
        database: Database = client[self.database]
        store = ds.MasterListDatastore(database)

        records: dict[str, model.Master] = dict()

        # Load S&P 600
        data: list[svc.SpEntry] = svc.get_sp600(self.sp_600_url)
        rec_count = 0
        err_count = 0
        for row in data:
            try:
                contents = asdict(row)
                contents['figi'] = '000000000000'

                record = model.Master(**contents)
                record.indexes.append('SP600')
                records[record.ticker] = record
                rec_count += 1
            except Exception as e:
                logger.error(f"Failed to parse master record for {row.ticker} - {e}")
                err_count += 1
                continue
        log_activity(f"S&P 600: records: {rec_count}, errors: {err_count}")

        # Load S&P 400
        data: list[svc.SpEntry] = svc.get_sp400(self.sp_400_url)
        rec_count = 0
        err_count = 0
        for row in data:
            try:
                contents = asdict(row)
                contents['figi'] = '000000000000'

                record = model.Master(**contents)
                record.indexes.append('SP400')
                records[record.ticker] = record
                rec_count += 1
            except Exception as e:
                logger.error(f"Failed to parse master record for {row.ticker} - {e}")
                err_count += 1
                continue
        log_activity(f"S&P 400: records: {rec_count}, errors: {err_count}")

        # Load S&P 500
        data: list[svc.SpEntry] = svc.get_sp500(self.sp_500_url)
        rec_count = 0
        err_count = 0
        for row in data:
            try:
                contents = asdict(row)
                contents['figi'] = '000000000000'

                record = model.Master(**contents)
                record.indexes.append('SP500')
                records[record.ticker] = record
                rec_count += 1
            except Exception as e:
                logger.error(f"Failed to parse master record for {row.ticker} - {e}")
                err_count += 1
                continue
        log_activity(f"S&P 500: records: {rec_count}, errors: {err_count}")

        # Update S&P 100
        data: list[str] = svc.get_sp100_tickers(self.sp_100_url)
        rec_count = 0
        err_count = 0
        for ticker in data:
            try:
                records[ticker].indexes.append('SP100')
                rec_count += 1
            except Exception as e:
                logger.error(f"Failed to update record with S&P 100 flag for {ticker} - {e}")
                err_count += 1
                continue
        log_activity(f"S&P 100: records: {rec_count}, errors: {err_count}")

        # Write recotds
        rec_count = 0
        err_count = 0
        for _, record in records.items():
            try:
                record.metadata.init_for_insert()
                store.insert(record)
                rec_count += 1
            except Exception as e:
                logger.error(f"Failed to write master record {record.ticker} - {e}")
                err_count += 1
                continue
        log_activity(f"Master records written: {rec_count}, errors: {err_count}")

    def output(self):
        return CollectionPopulatedTarget(self.url, self.database, self.collection)


class LoadFigiCodesTask(luigi.Task):
    """
    This task updates the master records with the CIK code supplied by
    the SEC
    """
    url = luigi.Parameter()
    database = luigi.Parameter()
    collection = luigi.Parameter()
    open_figi_url = luigi.Parameter()
    open_figi_key = luigi.Parameter()

    def requires(self):
        return [PopulateMasterListTask()]

    @logger.catch(reraise=True)
    def run(self):
        client: MongoClient = MongoClient(self.url)
        database: Database = client[self.database]
        store = ds.MasterListDatastore(database)
        ctrl_store = ds.TaskControlDatastore(database)

        tickers = store.get_tickers()

        rec_count = 0
        err_count = 0
        for ticker in tickers:
            try:
                code = svc.get_openfigi_code(self.open_figi_url, self.open_figi_key, ticker)
                store.update_figi(ticker, code)
                rec_count += 1
            except Exception as e:
                logger.error(f"Failed to update FIGI for ticker: {ticker} - {e}")
                err_count += 1

        if rec_count > 0:
            ctrl_store.update_figi_flag(True)

        log_activity(f"Updated Master List FIGI values: records {rec_count}, errors {err_count}")

    def output(self):
        return FigiLoadTaskCompletedTarget(self.url, self.database)


class LoadCikCodesTask(luigi.Task):
    """
    This task updates the master records with the CIK code supplied by
    the SEC
    """
    url = luigi.Parameter()
    database = luigi.Parameter()
    collection = luigi.Parameter()
    sec_url = luigi.Parameter()

    def requires(self):
        return [PopulateMasterListTask()]

    @logger.catch(reraise=True)
    def run(self):
        client: MongoClient = MongoClient(self.url)
        database: Database = client[self.database]
        store = ds.MasterListDatastore(database)
        ctrl_store = ds.TaskControlDatastore(database)

        tickers = store.get_tickers()
        map = svc.get_sec_map(self.sec_url)

        rec_count = 0
        err_count = 0
        for item in map:
            if item.ticker in tickers:
                try:
                    store.update_cik(item.ticker, item.cik_str)
                    rec_count += 1
                except Exception as e:
                    logger.error(f"Failed to update CIK for ticker: {item.ticker} - {e}")
                    err_count += 1

        if rec_count > 0:
            ctrl_store.update_cik_flag(True)

        log_activity(f"Updated Master List CIKs values: records {rec_count}, errors {err_count}")


    def output(self):
        return CikLoadTaskCompletedTarget(self.url, self.database)


class BuildMasterListTask(luigi.WrapperTask):
    def requires(self):
        return [LoadCikCodesTask(), LoadFigiCodesTask()]

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
__all__ = ['PopulateMasterTask', 'ResetTask', 'LoadCikCodesTask', 'LoadFigiCodesTask', 'PopulateDatabaseTask']

import math

import gf_lib.datastore as ds
import gf_lib.model as model
import gf_lib.services as svc
import gf_lib.utils as utils
import luigi
import orjson
from attrs import asdict
from gf_lib.utils import log_activity
from loguru import logger
import pymongo
from pymongo.database import Database

from ._targets import *


class ResetTask(luigi.Task):
    url = luigi.Parameter()
    database = luigi.Parameter()

    def requires(self):
        pass

    def run(self):
        client: pymongo.MongoClient = pymongo.MongoClient(self.url)
        db: Database = client[self.database]

        # Task Tracking
        store = ds.TaskTrackingDatastore(db)
        store.clear()
        record = model.TaskTracking()
        store.insert(record)

        # Master List
        store = ds.MasterDatastore(db)
        store.clear()

        # Company
        store = ds.CompanyDatastore(db)
        store.clear()

        # Accounts
        store = ds.IncomeDatastore(db)
        store.clear()

        store = ds.CashFlowDatastore(db)
        store.clear()

        store = ds.BalanceSheetDatastore(db)
        store.clear()

        store = ds.EarningsDatastore(db)
        store.clear()

        # Earnings (File)
        store = ds.EarningsFileDatastore(db)
        store.clear()

        # GICS
        store = ds.GicsSectorDatastore(db)
        store.clear()

        self.set_status_message(f"Database reset, successfully.")

    def output(self):
        pass


class PopulateMasterTask(luigi.Task):
    """
    This task populates the master list collection from
    the external sources
    """
    url = luigi.Parameter()
    database = luigi.Parameter()

    sp_600_url = luigi.Parameter()
    sp_400_url = luigi.Parameter()
    sp_500_url = luigi.Parameter()
    sp_100_url = luigi.Parameter()

    def requires(self):
        pass

    def run(self):
        client: pymongo.MongoClient = pymongo.MongoClient(self.url)
        database: Database = client[self.database]
        store = ds.MasterDatastore(database)

        records: dict[str, model.Master] = dict()

        # Load S&P 600
        data: list[svc.SpEntry] = svc.get_sp600(self.sp_600_url)
        rec_count = 0
        err_count = 0
        for row in data:
            try:
                contents = asdict(row)
                contents['cik'] = '0000000000'
                contents['figi'] = '000000000000'

                record = model.Master(**contents)
                record.indexes.append(model.IndexType.SP600)
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
                contents['cik'] = '0000000000'
                contents['figi'] = '000000000000'

                record = model.Master(**contents)
                record.indexes.append(model.IndexType.SP400)
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
                contents['cik'] = '0000000000'
                contents['figi'] = '000000000000'

                record = model.Master(**contents)
                record.indexes.append(model.IndexType.SP500)
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
                records[ticker].indexes.append(model.IndexType.SP100)
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
        self.set_status_message(f"Master records written: {rec_count}, errors: {err_count}")

        # Update Flag
        store = ds.TaskTrackingDatastore(database)
        store.update_master_flag(True)

    def output(self):
        return MasterLoadedTarget(self.url, self.database)


class LoadFigiCodesTask(luigi.Task):
    """
    This task updates the master records with the CIK code supplied by
    the SEC
    """
    url = luigi.Parameter()
    database = luigi.Parameter()
    open_figi_url = luigi.Parameter()
    open_figi_key = luigi.Parameter()

    def requires(self):
        return [PopulateMasterTask()]

    @logger.catch(reraise=True)
    def run(self):
        def split(data: list[str], chunk_size: int = 20) -> list[str]:
            for i in range(0, len(data), chunk_size):
                yield data[i:i + chunk_size]

        client: pymongo.MongoClient = pymongo.MongoClient(self.url)
        database: Database = client[self.database]
        store = ds.MasterDatastore(database)
        ctrl_store = ds.TaskTrackingDatastore(database)

        tickers = store.get_tickers()

        rec_count = 0
        err_count = 0
        total_count = len(tickers)
        processed_count = 0

        for batch in split(tickers):
            try:
                codes: list[svc.FigiCode] = svc.get_openfigi_codes(self.open_figi_url, self.open_figi_key, batch)

                for code in codes:
                    if code.figi is None:
                        logger.error(f"Failed to find FIGI code for: {code.ticker}")
                        err_count += 1
                        continue

                    store.update_figi(code.ticker, code.figi)
                    rec_count += 1
            except Exception as e:
                logger.error(f"Failed to update FIGI for ticker: {', '.join(batch)} - {e}")
                err_count += 1
                continue

            processed_count += len(batch)
            self.set_status_message("Processing FIGI codes...")
            self.set_progress_percentage(min(math.floor(100 * (processed_count / total_count)), 100))

        if rec_count > 0:
            ctrl_store.update_figi_flag(True)

        log_activity(f"Updated Master List FIGI values: records {rec_count}, errors {err_count}")
        self.set_status_message(f"Updated Master List FIGI values: records {rec_count}, errors {err_count}")
        self.set_progress_percentage(100)

    def output(self):
        return FigiLoadedTarget(self.url, self.database)


class LoadCikCodesTask(luigi.Task):
    """
    This task updates the master records with the CIK code supplied by
    the SEC
    """
    url = luigi.Parameter()
    database = luigi.Parameter()
    sec_url = luigi.Parameter()

    def requires(self):
        return [PopulateMasterTask()]

    @logger.catch(reraise=True)
    def run(self):
        client: pymongo.MongoClient = pymongo.MongoClient(self.url)
        database: Database = client[self.database]
        store = ds.MasterDatastore(database)
        ctrl_store = ds.TaskTrackingDatastore(database)

        tickers = store.get_tickers()
        sec_map = svc.get_sec_map(self.sec_url)

        rec_count = 0
        err_count = 0
        total_count = len(tickers)
        processed_count = 0

        for item in sec_map:
            self.set_status_message("Processing CIK codes...")

            if item.ticker in tickers:
                try:
                    store.update_cik(item.ticker, item.cik_str)
                    rec_count += 1
                except Exception as e:
                    logger.error(f"Failed to update CIK for ticker: {item.ticker} - {e}")
                    err_count += 1

                processed_count += 1
                self.set_progress_percentage(min(math.floor(100 * (processed_count / total_count)), 100))

                if processed_count == total_count:
                    break

        if rec_count > 0:
            ctrl_store.update_cik_flag(True)

        log_activity(f"Updated Master List CIKs values: records {rec_count}, errors {err_count}")
        self.set_status_message(f"Updated Master List CIKs values: records {rec_count}, errors {err_count}")
        self.set_progress_percentage(100)

    def output(self):
        return CikLoadedTarget(self.url, self.database)


class LoadGICSSectorTask(luigi.Task):
    url = luigi.Parameter()
    database = luigi.Parameter()

    def requires(self):
        pass

    def parse_sector(self, data: dict) -> model.GICSSector:
        id = data['id']
        name = data['name']

        sector = model.GICSSector(id, name)

        group_industries = data['items']
        for grp in group_industries:
            id = grp['id']
            name = grp['name']
            group = model.GICSGroupIndustry(id, name)

            industries = grp['items']
            for ind in industries:
                id = ind['id']
                name = ind['name']

                industry = model.GICSIndustry(id, name)
                sub_industries = ind['items']
                for sub in sub_industries:
                    id = sub['id']
                    name = sub['name']
                    sub_industry = model.GICSSubIndustry(id, name)
                    industry.sub_industries.append(sub_industry)

                group.industries.append(industry)

            sector.group_industries.append(group)

        return sector

    def run(self):
        client: pymongo.MongoClient = pymongo.MongoClient(self.url)
        database: Database = client[self.database]
        store = ds.GicsSectorDatastore(database)

        data_folder = utils.find_data_folder(__file__)
        data_file = data_folder.joinpath('gics.json')
        if not data_file.exists():
            raise ValueError(f"GICS data file not found ({data_file})")

        file_content = data_file.read_text()
        data = orjson.loads(file_content)

        rec_count = 0
        err_count = 0
        for entry in data:
            sector = self.parse_sector(entry)
            try:
                store.insert(sector)
                rec_count += 1
            except Exception as e:
                logger.error(f"Failed to insert GICS sector: {sector.name} - {e}")
                err_count += 1
                continue

        log_activity(f"Loaded GICS records: records {rec_count}, errors {err_count}")
        self.set_status_message(f"Loaded GICS records: records {rec_count}, errors {err_count}")

    def output(self):
        return CollectionHasDataTarget(self.url, self.database)


class PopulateDatabaseTask(luigi.WrapperTask):
    def requires(self):
        return [LoadGICSSectorTask(), LoadCikCodesTask(), LoadFigiCodesTask()]

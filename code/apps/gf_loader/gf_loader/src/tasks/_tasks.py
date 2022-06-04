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
__all__ = ['PopulateMasterListTask']

from pymongo import MongoClient
from pymongo.database import Database
import luigi
from attrs import asdict
from loguru import logger
import gf_lib.datastore as ds
import gf_lib.services as svc
import gf_lib.model as model
from gf_lib.utils import log_activity
from ._targets import CollectionPopulatedTarget


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

        # Clear the collection
        store.clear()

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

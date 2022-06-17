# *******************************************************************************************
#  File:  datastore_test.py
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

import pytest
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from gf_lib.datastore import MasterDatastore, GicsSectorDatastore, CompanyDatastore, \
    CashFlowDatastore, BalanceSheetDatastore, IncomeDatastore, EarningsDatastore, TaskTrackingDatastore, EarningsFileDatastore
from gf_lib.errors import DuplicateRecordError
import gf_lib.model as model


class TestTaskTracking:
    COLLECTION_NAME = 'task_tracking'

    @pytest.fixture
    def clear_collection(self, mongodb_connection) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        col: Collection = db[TestTaskTracking.COLLECTION_NAME]
        col.delete_many({})

    def test_insert(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = TaskTrackingDatastore(db)

        record = model.TaskTracking()
        assert store.insert(record)

    def test_update_cik(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = TaskTrackingDatastore(db)

        record = model.TaskTracking()
        assert store.insert(record)

        assert store.update_cik_flag(True)
        record = store.get()
        assert record.cik_loaded

    def test_update_figi(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = TaskTrackingDatastore(db)

        record = model.TaskTracking()
        assert store.insert(record)

        assert store.update_figi_flag(True)
        record = store.get()
        assert record.figi_loaded

    def test_update_master(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = TaskTrackingDatastore(db)

        record = model.TaskTracking()
        assert store.insert(record)

        assert store.update_master_flag(True)
        record = store.get()
        assert record.master_loaded

    def test_update_earnings(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = TaskTrackingDatastore(db)

        record = model.TaskTracking()
        assert store.insert(record)

        assert store.update_earnings_flag(True)
        record = store.get()
        assert record.earnings_file_loaded

    def test_get(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = TaskTrackingDatastore(db)

        record = model.TaskTracking()
        assert store.insert(record)

        record = store.get()
        assert record


class TestEarningsStatement:
    @pytest.fixture
    def clear_collection(self, mongodb_connection) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = EarningsDatastore(db)
        store.clear()

    def test_insert(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = EarningsDatastore(db)

        entry = model.AccountingEntry('Revenue', value_1='10000')
        record = model.EarningsStatement('IBM', model.PeriodType.Annual)
        record.items.append(entry)

        assert store.insert(record)

    def test_insert_dublicate(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = EarningsDatastore(db)

        entry = model.AccountingEntry('Revenue', value_1='10000')
        record = model.EarningsStatement('IBM', model.PeriodType.Annual)
        record.items.append(entry)
        assert store.insert(record)

        with pytest.raises(DuplicateRecordError):
            store.insert(record)

    def test_get(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = EarningsDatastore(db)

        entry = model.AccountingEntry('Revenue', value_1='10000')
        record = model.EarningsStatement('IBM', model.PeriodType.Annual)
        record.items.append(entry)

        assert store.insert(record)

        found_record: model.EarningsStatement = store.get('IBM', model.PeriodType.Annual)
        assert found_record
        assert found_record.ticker == 'IBM'
        assert len(found_record.items) == 1

    def test_get_none(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = EarningsDatastore(db)

        entry = model.AccountingEntry('Revenue', value_1='10000')
        record = model.EarningsStatement('IBM', model.PeriodType.Annual)
        record.items.append(entry)
        assert store.insert(record)

        record = store.get('IBM', model.PeriodType.Quarter)
        assert record is None


class TestIncomeStatement:
    @pytest.fixture
    def clear_collection(self, mongodb_connection) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = IncomeDatastore(db)
        store.clear()

    def test_insert(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = IncomeDatastore(db)

        entry = model.AccountingEntry('Revenue', value_1='10000')
        record = model.IncomeStatement('IBM', model.PeriodType.Annual)
        record.items.append(entry)

        assert store.insert(record)

    def test_insert_dublicate(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = IncomeDatastore(db)

        record = model.IncomeStatement('IBM', model.PeriodType.Annual)
        assert store.insert(record)

        with pytest.raises(DuplicateRecordError):
            store.insert(record)

    def test_get(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = IncomeDatastore(db)

        entry = model.AccountingEntry('Revenue', value_1='10000')
        record = model.IncomeStatement('IBM', model.PeriodType.Annual)
        record.items.append(entry)

        assert store.insert(record)

        found_record: model.IncomeStatement = store.get('IBM', model.PeriodType.Annual)
        assert found_record
        assert found_record.ticker == 'IBM'
        assert len(found_record.items) == 1

    def test_get_none(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = IncomeDatastore(db)

        record = model.IncomeStatement('IBM', model.PeriodType.Annual)
        assert store.insert(record)

        record = store.get('IBM', model.PeriodType.Quarter)
        assert record is None


class TestBalanceSheetStatement:
    @pytest.fixture
    def clear_collection(self, mongodb_connection) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = BalanceSheetDatastore(db)
        store.clear()

    def test_insert(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = BalanceSheetDatastore(db)

        entry = model.AccountingEntry('Revenue', value_1='10000')
        record = model.BalanceSheetStatement('IBM', model.PeriodType.Annual)
        record.items.append(entry)

        assert store.insert(record)

    def test_insert_dublicate(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = BalanceSheetDatastore(db)

        record = model.BalanceSheetStatement('IBM', model.PeriodType.Annual)
        assert store.insert(record)

        with pytest.raises(DuplicateRecordError):
            store.insert(record)

    def test_get(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = BalanceSheetDatastore(db)

        entry = model.AccountingEntry('Revenue', value_1='10000')
        record = model.BalanceSheetStatement('IBM', model.PeriodType.Annual)
        record.items.append(entry)

        assert store.insert(record)

        found_record: model.BalanceSheetStatement = store.get('IBM', model.PeriodType.Annual)
        assert found_record
        assert found_record.ticker == 'IBM'
        assert len(found_record.items) == 1

    def test_get_none(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = BalanceSheetDatastore(db)

        record = model.BalanceSheetStatement('IBM', model.PeriodType.Annual)
        assert store.insert(record)

        record = store.get('IBM', model.PeriodType.Quarter)
        assert record is None


class TestCashFlowStatement:
    @pytest.fixture
    def clear_collection(self, mongodb_connection) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = CashFlowDatastore(db)
        store.clear()

    def test_insert(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = CashFlowDatastore(db)

        entry = model.AccountingEntry('Revenue', value_1='10000')
        record = model.CashFlowStatement('IBM', model.PeriodType.Annual)
        record.items.append(entry)

        assert store.insert(record)

    def test_insert_dublicate(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = CashFlowDatastore(db)

        record = model.CashFlowStatement('IBM', model.PeriodType.Annual)
        assert store.insert(record)

        with pytest.raises(DuplicateRecordError):
            store.insert(record)

    def test_get(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = CashFlowDatastore(db)

        entry = model.AccountingEntry('Revenue', value_1='10000')
        record = model.CashFlowStatement('IBM', model.PeriodType.Annual)
        record.items.append(entry)

        assert store.insert(record)

        found_record: model.CashFlowStatement = store.get('IBM', model.PeriodType.Annual)
        assert found_record
        assert found_record.ticker == 'IBM'
        assert len(found_record.items) == 1

    def test_get_none(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = CashFlowDatastore(db)

        record = model.CashFlowStatement('IBM', model.PeriodType.Annual)
        assert store.insert(record)

        record = store.get('IBM', model.PeriodType.Quarter)
        assert record is None


class TestCompanyDatastore:
    @pytest.fixture
    def clear_collection(self, mongodb_connection) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = CompanyDatastore(db)
        store.clear()

    def test_insert(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = CompanyDatastore(db)

        record = model.Company('IBM', 'IBM Corporation', 'Test Description', '0123456789', '012345678912', 'NYSE',
                               'USD', 'USA', 'Test-Sub-Industry', 'Main Street', model.Months.December, '2022-03-31')

        assert store.insert(record)

    def test_insert_duplicate(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = CompanyDatastore(db)

        record = model.Company('IBM', 'IBM Corporation', 'Test Description', '0123456789', '012345678912', 'NYSE',
                               'USD', 'USA', 'Test-Sub-Industry', 'Main Street', model.Months.December, '2022-03-31')

        assert store.insert(record)

        with pytest.raises(DuplicateRecordError):
            store.insert(record)

    def test_get(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = CompanyDatastore(db)

        record = model.Company('IBM', 'IBM Corporation', 'Test Description', '0123456789', '012345678912', 'NYSE',
                               'USD', 'USA', 'Test-Sub-Industry', 'Main Street', model.Months.December, '2022-03-31')

        assert store.insert(record)

        result = store.get('IBM')

        assert record.name == result.name
        assert record.description == result.description

    def test_get_none(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = CompanyDatastore(db)

        record = model.Company('IBM', 'IBM Corporation', 'Test Description', '0123456789', '012345678912', 'NYSE',
                               'USD', 'USA', 'Test-Sub-Industry', 'Main Street', model.Months.December, '2022-03-31')

        assert store.insert(record)

        result = store.get('AAPL')

        assert result is None


class TestGicsSectorDatastore:
    @pytest.fixture
    def clear_collection(self, mongodb_connection) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = GicsSectorDatastore(db)
        store.clear()

    def test_insert(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = GicsSectorDatastore(db)

        sub_ind = model.GICSSubIndustry(10_100_100, 'Sub Industry 1')

        ind = model.GICSIndustry(100_100, 'Industry 1')
        ind.sub_industries.append(sub_ind)

        grp = model.GICSGroupIndustry(1_100, 'Group Industry 1')
        grp.industries.append(ind)

        sec = model.GICSSector(12, 'Sector')
        sec.group_industries.append(grp)

        assert store.insert(sec)

    def test_insert_duplicate(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = GicsSectorDatastore(db)

        sub_ind = model.GICSSubIndustry(10_100_100, 'Sub Industry 1')

        ind = model.GICSIndustry(100_100, 'Industry 1')
        ind.sub_industries.append(sub_ind)

        grp = model.GICSGroupIndustry(1_100, 'Group Industry 1')
        grp.industries.append(ind)

        sec = model.GICSSector(12, 'Sector')
        sec.group_industries.append(grp)

        assert store.insert(sec)
        with pytest.raises(DuplicateRecordError):
            store.insert(sec)

    def test_get(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = GicsSectorDatastore(db)

        sub_ind = model.GICSSubIndustry(10_100_100, 'Sub Industry 1')

        ind = model.GICSIndustry(100_100, 'Industry 1')
        ind.sub_industries.append(sub_ind)

        grp = model.GICSGroupIndustry(1_100, 'Group Industry 1')
        grp.industries.append(ind)

        sec = model.GICSSector(12, 'Materials')
        sec.group_industries.append(grp)

        assert store.insert(sec)

        record = store.get('Materials')
        assert record.name == record.name

    def test_get_all(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = GicsSectorDatastore(db)

        sub_ind = model.GICSSubIndustry(10_100_100, 'Sub Industry 1')
        ind = model.GICSIndustry(100_100, 'Industry 1')
        ind.sub_industries.append(sub_ind)
        grp = model.GICSGroupIndustry(1_100, 'Group Industry 1')
        grp.industries.append(ind)
        sec = model.GICSSector(12, 'Materials')
        sec.group_industries.append(grp)

        assert store.insert(sec)

        sub_ind = model.GICSSubIndustry(10_100_100, 'Sub Industry 1')
        ind = model.GICSIndustry(100_100, 'Industry 1')
        ind.sub_industries.append(sub_ind)
        grp = model.GICSGroupIndustry(1_100, 'Group Industry 1')
        grp.industries.append(ind)
        sec = model.GICSSector(12, 'Transportation')
        sec.group_industries.append(grp)

        assert store.insert(sec)

        records = store.get_all()
        assert len(records) == 2


class TestMasterListDatastore:
    @pytest.fixture
    def clear_collection(self, mongodb_connection) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterDatastore(db)
        store.clear()

    def test_insert(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterDatastore(db)
        record = model.Master(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='012345678912',
                              sub_industry='Industry')
        record.indexes.append(model.IndexType.SP600)
        record.indexes.append(model.IndexType.SP100)

        assert store.insert(record)

    def test_insert_duplicate(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterDatastore(db)

        record = model.Master(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='012345678912',
                              sub_industry='Industry')
        record.indexes.append(model.IndexType.SP600)
        record.indexes.append(model.IndexType.SP100)

        assert store.insert(record)
        with pytest.raises(DuplicateRecordError):
            store.insert(record)

    def test_get(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterDatastore(db)

        record = model.Master(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='012345678912',
                              sub_industry='Industry')
        record.indexes.append(model.IndexType.SP600)
        record.indexes.append(model.IndexType.SP100)
        assert store.insert(record)

        record = model.Master(ticker='AAPL', name='Apple Inc.', cik='0123456780', figi='012345678910',
                              sub_industry='Industry')
        record.indexes.append(model.IndexType.SP600)
        record.indexes.append(model.IndexType.SP100)
        assert store.insert(record)

        result = store.get('AAPL')

        assert record.ticker == result.ticker
        assert record.name == result.name
        assert record.cik == result.cik
        assert record.figi == result.figi
        assert record.sub_industry == result.sub_industry

    def test_get_none(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterDatastore(db)

        record = model.Master(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='012345678912',
                              sub_industry='Industry')
        record.indexes.append(model.IndexType.SP600)
        record.indexes.append(model.IndexType.SP100)
        assert store.insert(record)

        result = store.get('AAPL')

        assert result is None

    def test_get_tickers(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterDatastore(db)

        record = model.Master(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='012345678912',
                              sub_industry='Industry')
        record.indexes.append(model.IndexType.SP600)
        record.indexes.append(model.IndexType.SP100)
        assert store.insert(record)

        record = model.Master(ticker='AAPL', name='Apple Inc.', cik='0123456780', figi='012345678910',
                              sub_industry='Industry')
        record.indexes.append(model.IndexType.SP600)
        record.indexes.append(model.IndexType.SP100)
        assert store.insert(record)

        record = model.Master(ticker='DOW', name='Dow Chenicals Inc.', cik='0123456700', figi='012345678900',
                              sub_industry='Industry')
        record.indexes.append(model.IndexType.SP600)
        record.indexes.append(model.IndexType.SP100)
        assert store.insert(record)

        record = model.Master(ticker='DD', name='DuPont de Nemours Inc.', cik='0123456000', figi='012345678000',
                              sub_industry='Industry')
        record.indexes.append(model.IndexType.SP600)
        record.indexes.append(model.IndexType.SP100)
        assert store.insert(record)

        data = store.get_tickers()
        assert len(data) == 4

    def test_update_figi(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterDatastore(db)

        record = model.Master(ticker='DD', name='DuPont de Nemours Inc.', cik='0123456789', figi='012345678912',
                              sub_industry='Industry')
        assert store.insert(record)

        record = store.get('DD')
        assert record.figi == '012345678912'

        store.update_figi('DD', 'BBG000BLNNH6')
        record = store.get('DD')

        assert record.figi == 'BBG000BLNNH6'
        assert record.metadata.lock_version == 2

    def test_update_cik(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterDatastore(db)

        record = model.Master(ticker='DD', name='DuPont de Nemours Inc.', cik='0123456789', figi='012345678912',
                              sub_industry='Industry')
        assert store.insert(record)

        record = store.get('DD')
        assert record.cik == '0123456789'

        store.update_cik('DD', '9876543210')
        record = store.get('DD')

        assert record.cik == '9876543210'
        assert record.metadata.lock_version == 2


class TestEarnings:
    @pytest.fixture
    def clear_collection(self, mongodb_connection) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = EarningsFileDatastore(db)
        store.clear()

    def test_insert(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = EarningsFileDatastore(db)

        record = model.Earnings('IBM', name='IBM Corporation', estimate='3.45')

        assert store.insert(record)

    def test_insert_duplicate(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = EarningsFileDatastore(db)

        record = model.Earnings('IBM', name='IBM Corporation', estimate='3.45')

        assert store.insert(record)
        with pytest.raises(DuplicateRecordError):
            store.insert(record)

    def test_get(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = EarningsFileDatastore(db)

        record = model.Earnings('IBM', name='IBM Corporation', estimate='3.45')
        assert store.insert(record)

        record = model.Earnings(ticker='AAPL', name='Apple Inc.', estimate='3.45')
        assert store.insert(record)

        result = store.get('AAPL')

        assert record.ticker == result.ticker
        assert record.name == result.name

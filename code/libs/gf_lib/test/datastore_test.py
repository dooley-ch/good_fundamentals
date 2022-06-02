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
from pymongo.database import Database
from pymongo.collection import Collection
from gf_lib.datastore import MasterListDatastore, GicsClassificationDatastore, CompanyDatastore, \
    AccountingStatemetDatastore
from gf_lib.model import Master, GicsClassification, Company, PeriodType, AccountingStatement
from gf_lib.errors import DuplicateRecordError


class TestEarningsStatement:
    COLLECTION_NAME = 'earnings_statements'

    @pytest.fixture
    def clear_collection(self, mongodb_connection) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        col: Collection = db[TestEarningsStatement.COLLECTION_NAME]
        col.delete_many({})

    def test_insert(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = AccountingStatemetDatastore(db, TestEarningsStatement.COLLECTION_NAME)

        record = AccountingStatement('IBM', PeriodType.Annual)
        assert store.insert(record)

    def test_insert_dublicate(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = AccountingStatemetDatastore(db, TestEarningsStatement.COLLECTION_NAME)

        record = AccountingStatement('IBM', PeriodType.Annual)
        assert store.insert(record)

        with pytest.raises(DuplicateRecordError):
            store.insert(record)

    def test_get(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = AccountingStatemetDatastore(db, TestEarningsStatement.COLLECTION_NAME)

        record = AccountingStatement('IBM', PeriodType.Annual)
        assert store.insert(record)

        record = store.get('IBM', PeriodType.Annual)
        assert record

    def test_get_none(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = AccountingStatemetDatastore(db, TestEarningsStatement.COLLECTION_NAME)

        record = AccountingStatement('IBM', PeriodType.Annual)
        assert store.insert(record)

        record = store.get('IBM', PeriodType.Quarter)
        assert record is None


class TestCashFlow:
    COLLECTION_NAME = 'cashflow_statements'

    @pytest.fixture
    def clear_collection(self, mongodb_connection) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        col: Collection = db[TestCashFlow.COLLECTION_NAME]
        col.delete_many({})

    def test_insert(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = AccountingStatemetDatastore(db, TestCashFlow.COLLECTION_NAME)

        record = AccountingStatement('IBM', PeriodType.Annual)
        assert store.insert(record)

    def test_insert_dublicate(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = AccountingStatemetDatastore(db, TestCashFlow.COLLECTION_NAME)

        record = AccountingStatement('IBM', PeriodType.Annual)
        assert store.insert(record)

        with pytest.raises(DuplicateRecordError):
            store.insert(record)

    def test_get(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = AccountingStatemetDatastore(db, TestCashFlow.COLLECTION_NAME)

        record = AccountingStatement('IBM', PeriodType.Annual)
        assert store.insert(record)

        record = store.get('IBM', PeriodType.Annual)
        assert record

    def test_get_none(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = AccountingStatemetDatastore(db, TestCashFlow.COLLECTION_NAME)

        record = AccountingStatement('IBM', PeriodType.Annual)
        assert store.insert(record)

        record = store.get('IBM', PeriodType.Quarter)
        assert record is None


class TestBalanceSheet:
    COLLECTION_NAME = 'balance_sheets'

    @pytest.fixture
    def clear_collection(self, mongodb_connection) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        col: Collection = db[TestBalanceSheet.COLLECTION_NAME]
        col.delete_many({})

    def test_insert(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = AccountingStatemetDatastore(db, TestBalanceSheet.COLLECTION_NAME)

        record = AccountingStatement('IBM', PeriodType.Annual)
        assert store.insert(record)

    def test_insert_dublicate(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = AccountingStatemetDatastore(db, TestBalanceSheet.COLLECTION_NAME)

        record = AccountingStatement('IBM', PeriodType.Annual)
        assert store.insert(record)

        with pytest.raises(DuplicateRecordError):
            store.insert(record)

    def test_get(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = AccountingStatemetDatastore(db, TestBalanceSheet.COLLECTION_NAME)

        record = AccountingStatement('IBM', PeriodType.Annual)
        assert store.insert(record)

        record = store.get('IBM', PeriodType.Annual)
        assert record

    def test_get_none(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = AccountingStatemetDatastore(db, TestBalanceSheet.COLLECTION_NAME)

        record = AccountingStatement('IBM', PeriodType.Annual)
        assert store.insert(record)

        record = store.get('IBM', PeriodType.Quarter)
        assert record is None


class TestIncomeStatement:
    COLLECTION_NAME = 'income_statements'

    @pytest.fixture
    def clear_collection(self, mongodb_connection) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        col: Collection = db[TestIncomeStatement.COLLECTION_NAME]
        col.delete_many({})

    def test_insert(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = AccountingStatemetDatastore(db, TestIncomeStatement.COLLECTION_NAME)

        record = AccountingStatement('IBM', PeriodType.Annual)
        assert store.insert(record)

    def test_insert_dublicate(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = AccountingStatemetDatastore(db, TestIncomeStatement.COLLECTION_NAME)

        record = AccountingStatement('IBM', PeriodType.Annual)
        assert store.insert(record)

        with pytest.raises(DuplicateRecordError):
            store.insert(record)

    def test_get(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = AccountingStatemetDatastore(db, TestIncomeStatement.COLLECTION_NAME)

        record = AccountingStatement('IBM', PeriodType.Annual)
        assert store.insert(record)

        record = store.get('IBM', PeriodType.Annual)
        assert record

    def test_get_none(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = AccountingStatemetDatastore(db, TestIncomeStatement.COLLECTION_NAME)

        record = AccountingStatement('IBM', PeriodType.Annual)
        assert store.insert(record)

        record = store.get('IBM', PeriodType.Quarter)
        assert record is None


class TestCompanyDatastore:
    @pytest.fixture
    def clear_collection(self, mongodb_connection) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        col: Collection = db['companies']
        col.delete_many({})

    def test_insert(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = CompanyDatastore(db)

        record = Company('IBM', 'International Business Machines Corp.', 'Company description', '0123456789',
                         '012345678912', 'NYSE', 'USD', 'USA', 'Technology', 'Information Technology Services',
                         'Main St. City, State', 'March', '2022-03-31', '2022-03-31', '2022-03-31')

        assert store.insert(record)

    def test_insert_duplicate(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = CompanyDatastore(db)

        record = Company('IBM', 'International Business Machines Corp.', 'Company description', '0123456789',
                         '012345678912', 'NYSE', 'USD', 'USA', 'Technology', 'Information Technology Services',
                         'Main St. City, State', 'March', '2022-03-31', '2022-03-31', '2022-03-31')

        assert store.insert(record)

        with pytest.raises(DuplicateRecordError):
            store.insert(record)

    def test_get(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = CompanyDatastore(db)

        record = Company('IBM', 'International Business Machines Corp.', 'Company description', '0123456789',
                         '012345678912', 'NYSE', 'USD', 'USA', 'Technology', 'Information Technology Services',
                         'Main St. City, State', 'March', '2022-03-31', '2022-03-31', '2022-03-31')

        assert store.insert(record)

        result = store.get('IBM')

        assert record.name == result.name
        assert record.description == result.description

    def test_get_none(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = CompanyDatastore(db)

        record = Company('IBM', 'International Business Machines Corp.', 'Company description', '0123456789',
                         '012345678912', 'NYSE', 'USD', 'USA', 'Technology', 'Information Technology Services',
                         'Main St. City, State', 'March', '2022-03-31', '2022-03-31', '2022-03-31')

        assert store.insert(record)

        result = store.get('AAPL')

        assert result is None


class TestGicsClassificationDatastore:
    @pytest.fixture
    def clear_collection(self, mongodb_connection) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        col: Collection = db['gics_classifications']
        col.delete_many({})

    def test_insert(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = GicsClassificationDatastore(db)

        record = GicsClassification('Materials')
        record.industry.append('Chemicals')
        record.industry.append('Construction Materials')
        record.industry.append('Containers & Packaging')
        record.industry.append('Metals & Mining')
        record.industry.append('Paper & Forest Products')

        assert store.insert(record)

    def test_insert_duplicate(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = GicsClassificationDatastore(db)

        record = GicsClassification('Materials')
        record.industry.append('Chemicals')
        record.industry.append('Construction Materials')
        record.industry.append('Containers & Packaging')
        record.industry.append('Metals & Mining')
        record.industry.append('Paper & Forest Products')

        assert store.insert(record)
        with pytest.raises(DuplicateRecordError):
            store.insert(record)

    def test_get(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = GicsClassificationDatastore(db)

        record = GicsClassification('Materials')
        record.industry.append('Chemicals')
        record.industry.append('Construction Materials')
        record.industry.append('Containers & Packaging')
        record.industry.append('Metals & Mining')
        record.industry.append('Paper & Forest Products')
        assert store.insert(record)

        record = store.get('Materials')
        assert record.sector == record.sector

    def test_get_all(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = GicsClassificationDatastore(db)

        record = GicsClassification('Materials')
        record.industry.append('Chemicals')
        record.industry.append('Construction Materials')
        record.industry.append('Containers & Packaging')
        record.industry.append('Metals & Mining')
        record.industry.append('Paper & Forest Products')
        assert store.insert(record)

        record = GicsClassification('Transportation')
        record.industry.append('Air Freight & Logistics')
        record.industry.append('Airlines')
        record.industry.append('Marine')
        record.industry.append('Road & Rail')
        record.industry.append('Transportation Infrastructure')
        assert store.insert(record)

        record = store.get_all()
        assert len(record) == 2


class TestMasterListDatastore:
    @pytest.fixture
    def clear_collection(self, mongodb_connection) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        col: Collection = db['master_list']
        col.delete_many({})

    def test_insert(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterListDatastore(db)
        record = Master(ticker='IBM', name='International Business Machines Corp.', cik='0123456789',
                        figi='012345678912', sector='Technology', sub_industry='Information Technology Services')

        record.indexes.append('SP500')
        record.indexes.append('SP100')

        assert store.insert(record)

    def test_insert_duplicate(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterListDatastore(db)

        record = Master(ticker='IBM', name='International Business Machines Corp.', cik='0123456789',
                        figi='012345678912', sector='Technology', sub_industry='Information Technology Services')

        assert store.insert(record)
        with pytest.raises(DuplicateRecordError):
            store.insert(record)

    def test_get(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterListDatastore(db)

        record = Master(ticker='IBM', name='International Business Machines Corp.', cik='0123456789',
                        figi='012345678912', sector='Technology', sub_industry='Information Technology Services')
        assert store.insert(record)

        record = Master(ticker='AAPL', name='Apple Inc.', cik='0123456789',
                        figi='012345678912', sector='Technology', sub_industry='Information Technology Services')
        record.indexes.append('SP500')
        record.indexes.append('SP100')

        assert store.insert(record)

        result = store.get('AAPL')

        assert record.ticker == result.ticker
        assert record.name == result.name
        assert record.cik == result.cik
        assert record.figi == result.figi
        assert record.sector == result.sector
        assert record.sub_industry == result.sub_industry

    def test_get_none(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterListDatastore(db)

        record = Master(ticker='IBM', name='International Business Machines Corp.', cik='0123456789',
                        figi='012345678912', sector='Technology', sub_industry='Information Technology Services')
        assert store.insert(record)

        result = store.get('AAPL')

        assert result is None

    def test_get_by_sector(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterListDatastore(db)

        record = Master(ticker='IBM', name='International Business Machines Corp.', cik='0123456789',
                        figi='012345678912', sector='Technology', sub_industry='Information Technology Services')
        assert store.insert(record)

        record = Master(ticker='AAPL', name='Apple Inc.', cik='0123456789',
                        figi='012345678912', sector='Technology', sub_industry='Consumer Electronics')

        assert store.insert(record)

        record = Master(ticker='DOW', name='Dow Inc.', cik='0123456789',
                        figi='012345678912', sector='Basic Materials', sub_industry='Chemicals')
        assert store.insert(record)

        records = store.find_by_sector('Technology')
        assert len(records) == 2

    def test_get_by_sector_one_row(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterListDatastore(db)

        record = Master(ticker='IBM', name='International Business Machines Corp.', cik='0123456789',
                        figi='012345678912', sector='Technology', sub_industry='Information Technology Services')
        assert store.insert(record)

        record = Master(ticker='AAPL', name='Apple Inc.', cik='0123456789',
                        figi='012345678912', sector='Technology', sub_industry='Consumer Electronics')

        assert store.insert(record)

        record = Master(ticker='DOW', name='Dow Inc.', cik='0123456789',
                        figi='012345678912', sector='Basic Materials', sub_industry='Chemicals')
        assert store.insert(record)

        records = store.find_by_sector('Basic Materials')
        assert len(records) == 1

    def test_get_by_sector_no_row(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterListDatastore(db)

        record = Master(ticker='IBM', name='International Business Machines Corp.', cik='0123456789',
                        figi='012345678912', sector='Technology', sub_industry='Information Technology Services')
        assert store.insert(record)

        record = Master(ticker='AAPL', name='Apple Inc.', cik='0123456789',
                        figi='012345678912', sector='Technology', sub_industry='Consumer Electronics')

        assert store.insert(record)

        record = Master(ticker='DOW', name='Dow Inc.', cik='0123456789',
                        figi='012345678912', sector='Basic Materials', sub_industry='Chemicals')
        assert store.insert(record)

        records = store.find_by_sector('Finance')
        assert len(records) == 0

    def test_get_by_sector_and_sub_industry(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterListDatastore(db)

        record = Master(ticker='IBM', name='International Business Machines Corp.', cik='0123456789',
                        figi='012345678912', sector='Technology', sub_industry='Information Technology Services')
        assert store.insert(record)

        record = Master(ticker='AAPL', name='Apple Inc.', cik='0123456789',
                        figi='012345678912', sector='Technology', sub_industry='Consumer Electronics')

        assert store.insert(record)

        record = Master(ticker='DOW', name='Dow Inc.', cik='0123456789',
                        figi='012345678912', sector='Basic Materials', sub_industry='Chemicals')
        assert store.insert(record)

        record = Master(ticker='DD', name='DuPont de Nemours Inc.', cik='0123456789',
                        figi='012345678912', sector='Basic Materials', sub_industry='Specialty Chemicals')
        assert store.insert(record)

        records = store.find_by_industry('Basic Materials', 'Specialty Chemicals')
        assert len(records) == 1

    def test_get_by_sector_and_industry_no_row(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterListDatastore(db)

        record = Master(ticker='IBM', name='International Business Machines Corp.', cik='0123456789',
                        figi='012345678912', sector='Technology', sub_industry='Information Technology Services')
        assert store.insert(record)

        record = Master(ticker='AAPL', name='Apple Inc.', cik='0123456789',
                        figi='012345678912', sector='Technology', sub_industry='Consumer Electronics')

        assert store.insert(record)

        record = Master(ticker='DOW', name='Dow Inc.', cik='0123456789',
                        figi='012345678912', sector='Basic Materials', sub_industry='Chemicals')
        assert store.insert(record)

        record = Master(ticker='DD', name='DuPont de Nemours Inc.', cik='0123456789',
                        figi='012345678912', sector='Basic Materials', sub_industry='Specialty Chemicals')
        assert store.insert(record)

        records = store.find_by_industry('Technology', 'Software')
        assert len(records) == 0

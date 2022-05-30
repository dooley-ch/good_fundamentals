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
from gf_lib.datastore import MasterListDatastore, GicsClassificationDatastore
from gf_lib.model import Master, GicsClassification
from gf_lib.errors import DuplicateRecordError


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
        record = Master('IBM', 'International Business Machines Corp.', '0123456789', '012345678912', 'Technology',
                        'Information Technology Services')
        assert store.insert(record)

    def test_insert_duplicate(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterListDatastore(db)

        record = Master('IBM', 'International Business Machines Corp.', '0123456789', '012345678912', 'Technology',
                        'Information Technology Services')

        assert store.insert(record)
        with pytest.raises(DuplicateRecordError):
            store.insert(record)

    def test_get(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterListDatastore(db)

        record = Master('IBM', 'International Business Machines Corp.', '0123456789', '012345678912', 'Technology',
                        'Information Technology Services')
        assert store.insert(record)

        record = Master('AAPL', 'Apple Inc.', '0123456789', '012345678912', 'Technology', 'Consumer Electronics')
        assert store.insert(record)

        result = store.get('AAPL')

        assert record.ticker == result.ticker
        assert record.name == result.name
        assert record.cik == result.cik
        assert record.figi == result.figi
        assert record.sector == result.sector
        assert record.industry == result.industry

    def test_get_none(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterListDatastore(db)

        record = Master('IBM', 'International Business Machines Corp.', '0123456789', '012345678912', 'Technology',
                        'Information Technology Services')
        assert store.insert(record)

        result = store.get('AAPL')

        assert result is None

    def test_get_by_sector(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterListDatastore(db)

        record = Master('IBM', 'International Business Machines Corp.', '0123456789', '012345678912', 'Technology',
                        'Information Technology Services')
        assert store.insert(record)

        record = Master('AAPL', 'Apple Inc.', '0123456789', '012345678912', 'Technology', 'Consumer Electronics')
        assert store.insert(record)

        record = Master('Dow', 'Dow Inc.', '0123456789', '012345678912', 'Basic Materials', 'Chemicals')
        assert store.insert(record)

        records = store.find_by_sector('Technology')
        assert len(records) == 2

    def test_get_by_sector_one_row(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterListDatastore(db)

        record = Master('IBM', 'International Business Machines Corp.', '0123456789', '012345678912', 'Technology',
                        'Information Technology Services')
        assert store.insert(record)

        record = Master('AAPL', 'Apple Inc.', '0123456789', '012345678912', 'Technology', 'Consumer Electronics')
        assert store.insert(record)

        record = Master('Dow', 'Dow Inc.', '0123456789', '012345678912', 'Basic Materials', 'Chemicals')
        assert store.insert(record)

        records = store.find_by_sector('Basic Materials')
        assert len(records) == 1

    def test_get_by_sector_no_row(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterListDatastore(db)

        record = Master('IBM', 'International Business Machines Corp.', '0123456789', '012345678912', 'Technology',
                        'Information Technology Services')
        assert store.insert(record)

        record = Master('AAPL', 'Apple Inc.', '0123456789', '012345678912', 'Technology', 'Consumer Electronics')
        assert store.insert(record)

        record = Master('Dow', 'Dow Inc.', '0123456789', '012345678912', 'Basic Materials', 'Chemicals')
        assert store.insert(record)

        records = store.find_by_sector('Finance')
        assert len(records) == 0

    def test_get_by_sector_and_industry(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterListDatastore(db)

        record = Master('IBM', 'International Business Machines Corp.', '0123456789', '012345678912', 'Technology',
                        'Information Technology Services')
        assert store.insert(record)

        record = Master('AAPL', 'Apple Inc.', '0123456789', '012345678912', 'Technology', 'Consumer Electronics')
        assert store.insert(record)

        record = Master('Dow', 'Dow Inc.', '0123456789', '012345678912', 'Basic Materials', 'Specialty Chemicals')
        assert store.insert(record)

        record = Master('DD', 'DuPont de Nemours Inc.', '0123456789', '012345678912', 'Basic Materials', 'Specialty Chemicals')
        assert store.insert(record)

        records = store.find_by_industry('Basic Materials', 'Specialty Chemicals')
        assert len(records) == 2

    def test_get_by_sector_and_industry_one_row(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterListDatastore(db)

        record = Master('IBM', 'International Business Machines Corp.', '0123456789', '012345678912', 'Technology',
                        'Information Technology Services')
        assert store.insert(record)

        record = Master('AAPL', 'Apple Inc.', '0123456789', '012345678912', 'Technology', 'Consumer Electronics')
        assert store.insert(record)

        record = Master('Dow', 'Dow Inc.', '0123456789', '012345678912', 'Basic Materials', 'Specialty Chemicals')
        assert store.insert(record)

        record = Master('DD', 'DuPont de Nemours Inc.', '0123456789', '012345678912', 'Basic Materials', 'Specialty Chemicals')
        assert store.insert(record)

        records = store.find_by_industry('Technology', 'Consumer Electronics')
        assert len(records) == 1

    def test_get_by_sector_and_industry_no_row(self, clear_collection, mongodb_connection: MongoClient) -> None:
        db: Database = mongodb_connection['good_fundamentals_test']
        store = MasterListDatastore(db)

        record = Master('IBM', 'International Business Machines Corp.', '0123456789', '012345678912', 'Technology',
                        'Information Technology Services')
        assert store.insert(record)

        record = Master('AAPL', 'Apple Inc.', '0123456789', '012345678912', 'Technology', 'Consumer Electronics')
        assert store.insert(record)

        record = Master('Dow', 'Dow Inc.', '0123456789', '012345678912', 'Basic Materials', 'Specialty Chemicals')
        assert store.insert(record)

        record = Master('DD', 'DuPont de Nemours Inc.', '0123456789', '012345678912', 'Basic Materials', 'Specialty Chemicals')
        assert store.insert(record)

        records = store.find_by_industry('Technology', 'Software')
        assert len(records) == 0

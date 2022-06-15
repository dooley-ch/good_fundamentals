# *******************************************************************************************
#  File:  model_database_test.py
#
#  Created: 29-05-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  29-05-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

import time
import pytest
import gf_lib.model as model


class TestAccounting:
    def test_creation(self) -> None:
        acc_entry = model.AccountingEntry('Revenue')
        assert acc_entry.tag == 'Revenue'

        data = model.IncomeStatement('IBM')
        assert data.tick == 'IBM'

        data = model.CashFlowStatement('IBM')
        assert data.tick == 'IBM'

        data = model.BalanceSheetStatement('IBM')
        assert data.tick == 'IBM'

        data = model.EarningsStatement('IBM')
        assert data.tick == 'IBM'

    def test_assignment(self) -> None:
        acc_entry = model.AccountingEntry('Revenue')
        assert acc_entry.tag == 'Revenue'

        data = model.IncomeStatement('IBM')
        data.items.append(acc_entry)
        assert data.tick == 'IBM'
        assert len(data.items) == 1

        data = model.CashFlowStatement('IBM')
        data.items.append(acc_entry)
        assert data.tick == 'IBM'
        assert len(data.items) == 1

        data = model.BalanceSheetStatement('IBM')
        data.items.append(acc_entry)
        assert data.tick == 'IBM'
        assert len(data.items) == 1

        data = model.EarningsStatement('IBM')
        data.items.append(acc_entry)
        assert data.tick == 'IBM'
        assert len(data.items) == 1


class TestGicsSector:
    def test_creation(self) -> None:
        data = model.GICSSubIndustry()
        assert data

        data = model.GICSGroupIndustry()
        assert data

        data = model.GICSSector()
        assert data

    def test_assignment(self) -> None:
        sub_ind = model.GICSSubIndustry(10_100_100, 'Sub Industry 1')
        assert sub_ind.id == 10_100_100
        assert sub_ind.name == 'Sub Industry 1'

        ind  = model.GICSIndustry(100_100, 'Industry 1')
        ind.sub_industries.append(sub_ind)
        assert ind.id == 100_100
        assert ind.name == 'Industry 1'
        assert len(ind.sub_industries) == 1

        grp = model.GICSGroupIndustry(1_100, 'Group Industry 1')
        grp.industries.append(ind)
        assert grp.id == 1_100
        assert grp.name == 'Group Industry 1'
        assert len(grp.industries) == 1

        sec = model.GICSSector(12, 'Sector')
        sec.group_industries.append(grp)
        assert sec.id == 12
        assert sec.name == 'Sector'
        assert len(sec.group_industries) == 1


class TestTaskTracking:
    def test_creation(self) -> None:
        data = model.TaskTracking()
        assert data

    def test_assignment(self) -> None:
        data = model.TaskTracking()
        assert data

        data.cik_loaded = True
        assert data.cik_loaded == True


class TestEarnings:
    def test_creation(self) -> None:
        data = model.Earnings('IBM')
        assert data

    def test_assignment(self) -> None:
        data = model.Earnings('IBM')
        assert data

        data.name = 'IBM Inc.'
        assert data.name == 'IBM Inc.'


class TestDocumentMetadata:
    def test_creation(self) -> None:
        data = model.DocumentMetadata()
        assert data

    def test_insert_init(self) -> None:
        data = model.DocumentMetadata()
        created_at = data.created_at

        time.sleep(2)
        data.init_for_insert()
        assert created_at < data.created_at

    def test_update_prep(self) -> None:
        data = model.DocumentMetadata()
        updated_at = data.updated_at
        lock_version = data.lock_version

        time.sleep(2)
        data.prep_for_update()
        assert updated_at < data.updated_at
        assert lock_version < data.lock_version


class TestMaster:
    def test_ticker_wrong_type(self) -> None:
        with pytest.raises(AttributeError) as e:
            model.Master(ticker=12, name='IBM Corporation', cik='0123456789', figi='012345678912',
                         sub_industry='Industry')

        msg: str = e.value.args[0]
        assert msg.startswith("'int' object has no attribute")

    def test_ticker_wrong_length(self) -> None:
        with pytest.raises(ValueError) as e:
            model.Master(ticker='XXXXXX', name='IBM Corporation', cik='0123456789', figi='012345678912',
                         sub_industry='Industry')

        msg: str = e.value.args[0]
        assert msg.startswith("'ticker' must match regex")

    def test_ticker_empty(self) -> None:
        with pytest.raises(ValueError) as e:
            model.Master(ticker='', name='IBM Corporation', cik='0123456789', figi='012345678912',
                         sub_industry='Industry')

        msg: str = e.value.args[0]
        assert msg.startswith("'ticker' must match regex")

    def test_ticker_convert_to_upper_case(self) -> None:
        record = model.Master(ticker='xxxxx', name='IBM Corporation', cik='0123456789', figi='012345678912',
                         sub_industry='Industry')
        assert record.ticker == 'XXXXX'

    def test_ticker_with_valid_value(self) -> None:
        record = model.Master(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='012345678912',
                              sub_industry='Industry')
        assert record.ticker == 'IBM'

    def test_cik_wrong_length(self) -> None:
        record = model.Master(ticker='IBM', name='IBM Corporation', cik='01234567', figi='012345678912',
                              sub_industry='Industry')
        assert record.cik == '0001234567'

    def test_cik_invalid_chars(self) -> None:
        with pytest.raises(ValueError) as e:
            model.Master(ticker='IBM', name='IBM Corporation', cik='01234567AB', figi='012345678912',
                         sub_industry='Industry')

        msg: str = e.value.args[0]
        assert msg.startswith("'cik' must match regex")

    def test_cik_with_valid_value(self) -> None:
        record = model.Master(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='012345678912',
                     sub_industry='Industry')
        assert record.cik == '0123456789'

    def test_figi_wrong_length(self) -> None:
        record = model.Master(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='0123456789',
                     sub_industry='Industry')
        assert record.figi == '000123456789'

    def test_figi_invalid_chars(self) -> None:
        with pytest.raises(ValueError) as e:
            model.Master(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='0123456789ab',
                         sub_industry='Industry')

        msg: str = e.value.args[0]
        assert msg.startswith("'figi' must match regex")

    def test_figi_with_valid_value(self) -> None:
        record = model.Master(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='012345678912',
                     sub_industry='Industry')
        assert record.figi == '012345678912'

    def test_equal(self) -> None:
        record_1 = model.Master(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='012345678912',
                              sub_industry='Industry')
        record_2 = model.Master(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='012345678943',
                              sub_industry='Industry')
        assert record_1 == record_2

    def test_not_equal(self) -> None:
        record_1 = model.Master(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='012345678912',
                              sub_industry='Industry')
        record_2 = model.Master(ticker='AAPL', name='IBM Corporation', cik='0123456789', figi='012345678912',
                              sub_industry='Industry')
        assert record_1 != record_2


class TestCompany:
    def test_ticker_wrong_type(self) -> None:
        with pytest.raises(AttributeError) as e:
            model.Company(1, 'IBM Corporation', 'Test Description', '0123456789', '012345678912', 'NYSE', 'USD', 'USA',
                          'Test-Sub-Industry', 'Main Street', model.Months.December, '2022-03-31')

        msg: str = e.value.args[0]

        assert msg.startswith("'int' object has no attribute")

    def test_ticker_wrong_length(self) -> None:
        with pytest.raises(ValueError) as e:
            model.Company('XXXXXX', 'IBM Corporation', 'Test Description', '0123456789', '012345678912', 'NYSE', 'USD', 'USA',
                          'Test-Sub-Industry', 'Main Street', model.Months.December, '2022-03-31')

        msg: str = e.value.args[0]
        assert msg.startswith("'ticker' must match regex")

    def test_ticker_empty(self) -> None:
        with pytest.raises(ValueError) as e:
            model.Company('', 'IBM Corporation', 'Test Description', '0123456789', '012345678912', 'NYSE', 'USD', 'USA',
                          'Test-Sub-Industry', 'Main Street', model.Months.December, '2022-03-31')

        msg: str = e.value.args[0]
        assert msg.startswith("'ticker' must match regex")

    def test_ticker_convert_to_upper_case(self) -> None:
        record = model.Company('XXXXX', 'IBM Corporation', 'Test Description', '0123456789', '012345678912', 'NYSE', 'USD', 'USA',
                          'Test-Sub-Industry', 'Main Street', model.Months.December, '2022-03-31')
        assert record.ticker == 'XXXXX'

    def test_ticker_with_valid_value(self) -> None:
        record = model.Company('IBM', 'IBM Corporation', 'Test Description', '0123456789', '012345678912', 'NYSE', 'USD', 'USA',
                          'Test-Sub-Industry', 'Main Street', model.Months.December, '2022-03-31')
        assert record.ticker == 'IBM'

    def test_cik_wrong_length(self) -> None:
        with pytest.raises(ValueError) as e:
            model.Company('IBM', 'IBM Corporation', 'Test Description', '01234567', '012345678912', 'NYSE', 'USD', 'USA',
                          'Test-Sub-Industry', 'Main Street', model.Months.December, '2022-03-31')

        msg: str = e.value.args[0]
        assert msg.startswith("'cik' must match regex")

    def test_cik_invalid_chars(self) -> None:
        with pytest.raises(ValueError) as e:
            model.Company('IBM', 'IBM Corporation', 'Test Description', '01234567AB', '012345678912', 'NYSE', 'USD', 'USA',
                          'Test-Sub-Industry', 'Main Street', model.Months.December, '2022-03-31')

        msg: str = e.value.args[0]
        assert msg.startswith("'cik' must match regex")

    def test_cik_with_valid_value(self) -> None:
        record = model.Company('IBM', 'IBM Corporation', 'Test Description', '0123456789', '012345678912', 'NYSE', 'USD', 'USA',
                          'Test-Sub-Industry', 'Main Street', model.Months.December, '2022-03-31')
        assert record.cik == '0123456789'

    def test_figi_wrong_length(self) -> None:
        with pytest.raises(ValueError) as e:
            model.Company('IBM', 'IBM Corporation', 'Test Description', '0123456789', '0123456789', 'NYSE', 'USD', 'USA',
                          'Test-Sub-Industry', 'Main Street', model.Months.December, '2022-03-31')

        msg: str = e.value.args[0]
        assert msg.startswith("'figi' must match regex")

    def test_figi_invalid_chars(self) -> None:
        with pytest.raises(ValueError) as e:
            model.Company('IBM', 'IBM Corporation', 'Test Description', '0123456789', '0123456789AB', 'NYSE', 'USD', 'USA',
                          'Test-Sub-Industry', 'Main Street', model.Months.December, '2022-03-31')
        msg: str = e.value.args[0]
        assert msg.startswith("'figi' must match regex")

    def test_figi_with_valid_value(self) -> None:
        record = model.Company('IBM', 'IBM Corporation', 'Test Description', '0123456789', '012345678912', 'NYSE', 'USD', 'USA',
                          'Test-Sub-Industry', 'Main Street', model.Months.December, '2022-03-31')
        assert record.figi == '012345678912'

    def test_equal(self) -> None:
        record_1 = model.Company('IBM', 'IBM Corporation', 'Test Description', '0123456789', '012345678912', 'NYSE', 'USD', 'USA',
                          'Test-Sub-Industry', 'Main Street', model.Months.December, '2022-03-31')
        record_2 = model.Company('IBM', 'IBM Corporation', 'Test Description', '0123456789', '012345678912', 'NYSE', 'USD', 'USA',
                          'Test-Sub-Industry', 'Main Street', model.Months.December, '2022-03-31')

        assert record_1 == record_2

    def test_not_equal(self) -> None:
        record_1 = model.Company('IBM', 'IBM Corporation', 'Test Description', '0123456789', '012345678912', 'NYSE', 'USD', 'USA',
                          'Test-Sub-Industry', 'Main Street', model.Months.December, '2022-03-31')
        record_2 = model.Company('AAPL', 'IBM Corporation', 'Test Description', '0123456789', '012345678912', 'NYSE', 'USD', 'USA',
                          'Test-Sub-Industry', 'Main Street', model.Months.December, '2022-03-31')

        assert record_1 != record_2

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

import attrs
import pytest
import gf_lib.model as model


class TestMaster:
    def test_ticker_wrong_type(self) -> None:
        with pytest.raises(AttributeError) as e:
            model.Master(ticker=12, name='IBM Corporation', cik='0123456789', figi='012345678912',
                         sector='Sector', sub_industry='Industry')

        msg: str = e.value.args[0]
        assert msg.startswith("'int' object has no attribute")

    def test_ticker_wrong_length(self) -> None:
        with pytest.raises(ValueError) as e:
            model.Master(ticker='XXXXXX', name='IBM Corporation', cik='0123456789', figi='012345678912',
                         sector='Sector', sub_industry='Industry')

        msg: str = e.value.args[0]
        assert msg.startswith("'ticker' must match regex")

    def test_ticker_empty(self) -> None:
        with pytest.raises(ValueError) as e:
            model.Master(ticker='', name='IBM Corporation', cik='0123456789', figi='012345678912',
                         sector='Sector', sub_industry='Industry')

        msg: str = e.value.args[0]
        assert msg.startswith("'ticker' must match regex")

    def test_ticker_convert_to_upper_case(self) -> None:
        record = model.Master(ticker='xxxxx', name='IBM Corporation', cik='0123456789', figi='012345678912',
                         sector='Sector', sub_industry='Industry')
        assert record.ticker == 'XXXXX'

    def test_ticker_with_valid_value(self) -> None:
        record = model.Master(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='012345678912',
                              sector='Sector', sub_industry='Industry')
        assert record.ticker == 'IBM'

    def test_cik_wrong_length(self) -> None:
        record = model.Master(ticker='IBM', name='IBM Corporation', cik='01234567', figi='012345678912',
                              sector='Sector', sub_industry='Industry')
        assert record.cik == '0001234567'

    def test_cik_invalid_chars(self) -> None:
        with pytest.raises(ValueError) as e:
            model.Master(ticker='IBM', name='IBM Corporation', cik='01234567AB', figi='012345678912',
                         sector='Sector', sub_industry='Industry')

        msg: str = e.value.args[0]
        assert msg.startswith("'cik' must match regex")

    def test_cik_with_valid_value(self) -> None:
        record = model.Master(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='012345678912',
                     sector='Sector', sub_industry='Industry')
        assert record.cik == '0123456789'

    def test_figi_wrong_length(self) -> None:
        record = model.Master(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='0123456789',
                     sector='Sector', sub_industry='Industry')
        assert record.figi == '000123456789'

    def test_figi_invalid_chars(self) -> None:
        with pytest.raises(ValueError) as e:
            model.Master(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='0123456789ab',
                         sector='Sector', sub_industry='Industry')

        msg: str = e.value.args[0]
        assert msg.startswith("'figi' must match regex")

    def test_figi_with_valid_value(self) -> None:
        record = model.Master(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='012345678912',
                     sector='Sector', sub_industry='Industry')
        assert record.figi == '012345678912'

    def test_equal(self) -> None:
        record_1 = model.Master(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='012345678912',
                              sector='Sector', sub_industry='Industry')
        record_2 = model.Master(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='012345678943',
                              sector='Sector', sub_industry='Industry')
        assert record_1 == record_2

    def test_not_equal(self) -> None:
        record_1 = model.Master(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='012345678912',
                              sector='Sector', sub_industry='Industry')
        record_2 = model.Master(ticker='AAPL', name='IBM Corporation', cik='0123456789', figi='012345678912',
                              sector='Sector', sub_industry='Industry')
        assert record_1 != record_2


class TestCompany:
    def test_ticker_wrong_type(self) -> None:
        with pytest.raises(AttributeError) as e:
            model.Company(1, 'IBM Corporation', 'Test', '0123456789', '012345678912', 'NYSE', 'USD', 'USA',
                          'TestSector',
                          'TestIndustry', 'Main Street', model.Months.December, '2022-03-31', '2022-06-10',
                          '2022-06-10')

        msg: str = e.value.args[0]

        assert msg.startswith("'int' object has no attribute")

    def test_ticker_wrong_length(self) -> None:
        with pytest.raises(ValueError) as e:
            model.Company('XXXXXX', 'IBM Corporation', 'Test', '0123456789', '012345678912', 'NYSE', 'USD', 'USA',
                          'TestSector', 'TestIndustry', 'Main Street', model.Months.December, '2022-03-31',
                          '2022-06-10',
                          '2022-06-10')

        msg: str = e.value.args[0]
        assert msg.startswith("'ticker' must match regex")

    def test_ticker_empty(self) -> None:
        with pytest.raises(ValueError) as e:
            model.Company('', 'IBM Corporation', 'Test', '0123456789', '012345678912', 'NYSE', 'USD', 'USA',
                          'TestSector', 'TestIndustry', 'Main Street', model.Months.December, '2022-03-31',
                          '2022-06-10',
                          '2022-06-10')

        msg: str = e.value.args[0]
        assert msg.startswith("'ticker' must match regex")

    def test_ticker_convert_to_upper_case(self) -> None:
        record = model.Company('XXXXX', 'IBM Corporation', 'Test', '0123456789', '012345678912', 'NYSE', 'USD', 'USA',
                               'TestSector', 'TestIndustry', 'Main Street', model.Months.December, '2022-03-31',
                               '2022-06-10',
                               '2022-06-10')
        assert record.ticker == 'XXXXX'

    def test_ticker_with_valid_value(self) -> None:
        record = model.Company('IBM', 'IBM Corporation', 'Test', '0123456789', '012345678912', 'NYSE', 'USD', 'USA',
                               'TestSector', 'TestIndustry', 'Main Street', model.Months.December, '2022-03-31',
                               '2022-06-10',
                               '2022-06-10')
        assert record.ticker == 'IBM'

    def test_cik_wrong_length(self) -> None:
        with pytest.raises(ValueError) as e:
            model.Company('IBM', 'IBM Corporation', 'Test', '01234567', '012345678912', 'NYSE', 'USD', 'USA',
                          'TestSector', 'TestIndustry', 'Main Street', model.Months.December, '2022-03-31',
                          '2022-06-10',
                          '2022-06-10')

        msg: str = e.value.args[0]
        assert msg.startswith("'cik' must match regex")

    def test_cik_invalid_chars(self) -> None:
        with pytest.raises(ValueError) as e:
            model.Company('IBM', 'IBM Corporation', 'Test', '01234567AB', '012345678912', 'NYSE', 'USD', 'USA',
                          'TestSector', 'TestIndustry', 'Main Street', model.Months.December, '2022-03-31',
                          '2022-06-10',
                          '2022-06-10')

        msg: str = e.value.args[0]
        assert msg.startswith("'cik' must match regex")

    def test_cik_with_valid_value(self) -> None:
        record = model.Company('IBM', 'IBM Corporation', 'Test', '0123456789', '012345678912', 'NYSE', 'USD', 'USA',
                               'TestSector', 'TestIndustry', 'Main Street', model.Months.December, '2022-03-31',
                               '2022-06-10',
                               '2022-06-10')
        assert record.cik == '0123456789'

    def test_figi_wrong_length(self) -> None:
        with pytest.raises(ValueError) as e:
            model.Company('IBM', 'IBM Corporation', 'Test', '0123456789', '0123456789', 'NYSE', 'USD', 'USA',
                          'TestSector', 'TestIndustry', 'Main Street', model.Months.December, '2022-03-31',
                          '2022-06-10', '2022-06-10')

        msg: str = e.value.args[0]
        assert msg.startswith("'figi' must match regex")

    def test_figi_invalid_chars(self) -> None:
        with pytest.raises(ValueError) as e:
            model.Company('IBM', 'IBM Corporation', 'Test', '0123456789', '0123456789AB', 'NYSE', 'USD', 'USA',
                          'TestSector', 'TestIndustry', 'Main Street', model.Months.December, '2022-03-31',
                          '2022-06-10', '2022-06-10')
        msg: str = e.value.args[0]
        assert msg.startswith("'figi' must match regex")

    def test_figi_with_valid_value(self) -> None:
        record = model.Company('IBM', 'IBM Corporation', 'Test', '0123456789', '012345678912', 'NYSE', 'USD', 'USA',
                               'TestSector', 'TestIndustry', 'Main Street', model.Months.December, '2022-03-31',
                               '2022-06-10',
                               '2022-06-10')
        assert record.figi == '012345678912'

    def test_equal(self) -> None:
        record_1 = model.Company('IBM', 'IBM Corporation', 'Test', '0123456789', '012345678912', 'NYSE', 'USD', 'USA',
                                 'TestSector', 'TestIndustry', 'Main Street', model.Months.December, '2022-03-31',
                                 '2022-06-10',
                                 '2022-06-10')
        record_2 = model.Company('IBM', 'IBM Corporation', 'Test', '0123456789', '012345678912', 'NYSE', 'USD', 'USA',
                                 'TestSector', 'TestIndustry', 'Main Street', model.Months.December, '2022-03-31',
                                 '2022-06-10',
                                 '2022-06-10')

        assert record_1 == record_2

    def test_not_equal(self) -> None:
        record_1 = model.Company('IBM', 'IBM Corporation', 'Test', '0123456789', '012345678912', 'NYSE', 'USD', 'USA',
                                 'TestSector', 'TestIndustry', 'Main Street', model.Months.December, '2022-03-31',
                                 '2022-06-10',
                                 '2022-06-10')
        record_2 = model.Company('IBM', 'IBM Corporation', 'Test', '0123456789', '012345678912', 'NYSE', 'USD', 'USA',
                                 'TestSector', 'TestIndustry', 'Main Street', model.Months.December, '2022-03-31',
                                 '2022-06-10',
                                 '2022-06-10')

        assert record_1 == record_2


class TestAccountingItem:
    def test_tag_wrong_type(self) -> None:
        with pytest.raises(TypeError) as e:
            model.AccountingItem(23)

        msg: str = e.value.args[0]
        assert msg.startswith("'tag' must be <class 'str'>")

    def test_tag_wrong_length(self) -> None:
        with pytest.raises(ValueError) as e:
            model.AccountingItem('Aa')

        msg: str = e.value.args[0]
        assert msg.startswith("'tag' must match regex")

    def test_tag_with_valid_value(self) -> None:
        record = model.AccountingItem('CashAndNearCashItems')
        assert record.tag == 'CashAndNearCashItems'

    # noinspection PyDataclass
    def test_are_equal(self) -> None:
        record_1 = model.AccountingItem('CashAndNearCashItems')
        record_1 = attrs.evolve(record_1, period_1=23)

        record_2 = model.AccountingItem('CashAndNearCashItems')

        assert record_1 == record_2

    def test_are_not_equal(self) -> None:
        record_1 = model.AccountingItem('Creditors')
        record_2 = model.AccountingItem('CashAndNearCashItems')

        assert record_1 != record_2


class TestAccountingStatement:
    def test_ticker_wrong_type(self) -> None:
        with pytest.raises(TypeError) as e:
            model.AccountingStatement(23, model.PeriodType.Annual)

        msg: str = e.value.args[0]
        assert msg.startswith("'ticker' must be <class 'str'>")

    def test_ticker_wrong_length(self) -> None:
        with pytest.raises(ValueError) as e:
            model.AccountingStatement('XXXXXX', model.PeriodType.Annual)

        msg: str = e.value.args[0]
        assert msg.startswith("'ticker' must match regex")

    def test_ticker_with_valid_value(self) -> None:
        record = model.AccountingStatement('IBM', model.PeriodType.Annual)
        assert record.ticker == 'IBM'

    def test_are_equal(self) -> None:
        record_1 = model.AccountingStatement('IBM', model.PeriodType.Annual)
        record_2 = model.AccountingStatement('IBM', model.PeriodType.Annual)

        assert record_1 == record_2

    def test_are_not_equal(self) -> None:
        record_1 = model.AccountingStatement('IBM', model.PeriodType.Annual)
        record_2 = model.AccountingStatement('AAPL', model.PeriodType.Annual)

        assert record_1 != record_2

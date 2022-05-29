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
import pendulum
import pytest
import gf_lib.model as model


class TestMasterList:
    def test_ticker_wrong_type(self) -> None:
        with pytest.raises(TypeError) as ex:
            model.MasterList(ticker=1, name='IBM Corporation', cik='0123456789', figi='012345678912',
                             sector='Test Sector', industry='Test Industry')
        assert ex.value.args[0] == "'ticker' must be <class 'str'> (got 1 that is a <class 'int'>)."

    def test_ticker_wrong_length(self) -> None:
        with pytest.raises(ValueError) as ex:
            model.MasterList(ticker='XXXXXX', name='IBM Corporation', cik='0123456789', figi='012345678912',
                             sector='Test Sector', industry='Test Industry')
        assert ex.value.args[0] == "'ticker' must match regex '^[A-Z0-9]{1,5}$' ('XXXXXX' doesn't)"

    def test_ticker_convert(self) -> None:
        record = model.MasterList(ticker='xxxxx', name='IBM Corporation', cik='0123456789', figi='012345678912',
                                  sector='Test Sector', industry='Test Industry')
        assert record.ticker == 'XXXXX'

    def test_ticker(self) -> None:
        record = model.MasterList(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='012345678912',
                                  sector='Test Sector', industry='Test Industry')
        assert record.ticker == 'IBM'

    def test_cik_wrong_type(self) -> None:
        with pytest.raises(TypeError) as ex:
            model.MasterList(ticker='XXXXX', name='IBM Corporation', cik=345, figi='012345678912',
                             sector='Test Sector', industry='Test Industry')
        assert ex.value.args[0] == "'cik' must be <class 'str'> (got 345 that is a <class 'int'>)."

    def test_cik_wrong_length(self) -> None:
        with pytest.raises(ValueError) as ex:
            model.MasterList(ticker='XXXXX', name='IBM Corporation', cik='0123456', figi='012345678912',
                             sector='Test Sector', industry='Test Industry')
        assert ex.value.args[0] == "'cik' must match regex '^[0-9]{10,10}$' ('0123456' doesn't)"

    def test_cik(self) -> None:
        record = model.MasterList(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='012345678912',
                                  sector='Test Sector', industry='Test Industry')
        assert record.cik == '0123456789'

    def test_figi_wrong_type(self) -> None:
        with pytest.raises(TypeError) as ex:
            model.MasterList(ticker='XXXXX', name='IBM Corporation', cik='0123456789', figi=123,
                             sector='Test Sector', industry='Test Industry')
        assert ex.value.args[0] == "'figi' must be <class 'str'> (got 123 that is a <class 'int'>)."

    def test_figi_wrong_length(self) -> None:
        with pytest.raises(ValueError) as ex:
            model.MasterList(ticker='XXXXX', name='IBM Corporation', cik='0123456789', figi='2333',
                             sector='Test Sector', industry='Test Industry')
        assert ex.value.args[0] == "'figi' must match regex '^[0-9]{12,12}$' ('2333' doesn't)"

    def test_figi(self) -> None:
        record = model.MasterList(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='012345678912',
                                  sector='Test Sector', industry='Test Industry')
        assert record.figi == '012345678912'

    def test_not_equal(self) -> None:
        record_1 = model.MasterList(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='012345678912',
                                    sector='Test Sector', industry='Test Industry')
        record_2 = model.MasterList(ticker='APPL', name='IBM Corporation', cik='0123456789', figi='012345678912',
                                    sector='Test Sector', industry='Test Industry')
        assert record_1 != record_2

    def test_equal(self) -> None:
        record_1 = model.MasterList(ticker='IBM', name='IBM Corporation', cik='0123456789', figi='012345678912',
                                    sector='Test Sector', industry='Test Industry')
        record_2 = model.MasterList(ticker='IBM', name='IBM Corporation', cik='9876543210', figi='012345678912',
                                    sector='Test Sector', industry='Test Industry')
        assert record_1 == record_2


class TestCompany:
    def test_ticker_wrong_type(self) -> None:
        with pytest.raises(TypeError) as ex:
            model.Company(ticker=1, name='IBM Corporation', description='Test', cik='0123456789', figi='012345678912',
                          exchange='NYSE', currency='USD', country='USA', sector='Test Sector',
                          industry='Test Industry',
                          address='Main Street', fiscal_year_end='December', last_quarter='2022-03-31',
                          dividend_date='2022-06-10', ex_dividend_date='2022-06-10')

        assert ex.value.args[0] == "'ticker' must be <class 'str'> (got 1 that is a <class 'int'>)."

    def test_ticker_wrong_length(self) -> None:
        with pytest.raises(ValueError) as ex:
            model.Company(ticker='XXXXXX', name='IBM Corporation', description='Test', cik='0123456789',
                          figi='012345678912',
                          exchange='NYSE', currency='USD', country='USA', sector='Test Sector',
                          industry='Test Industry',
                          address='Main Street', fiscal_year_end='December', last_quarter='2022-03-31',
                          dividend_date='2022-06-10', ex_dividend_date='2022-06-10')
        assert ex.value.args[0] == "'ticker' must match regex '^[A-Z0-9]{1,5}$' ('XXXXXX' doesn't)"

    def test_ticker_convert(self) -> None:
        record = model.Company(ticker='xxxxx', name='IBM Corporation', description='Test', cik='0123456789',
                               figi='012345678912',
                               exchange='NYSE', currency='USD', country='USA', sector='Test Sector',
                               industry='Test Industry',
                               address='Main Street', fiscal_year_end='December', last_quarter='2022-03-31',
                               dividend_date='2022-06-10', ex_dividend_date='2022-06-10')
        assert record.ticker == 'XXXXX'

    def test_cik_wrong_type(self) -> None:
        with pytest.raises(TypeError) as ex:
            model.Company(ticker='xxxxx', name='IBM Corporation', description='Test', cik=345, figi='012345678912',
                          exchange='NYSE', currency='USD', country='USA', sector='Test Sector',
                          industry='Test Industry',
                          address='Main Street', fiscal_year_end='December', last_quarter='2022-03-31',
                          dividend_date='2022-06-10', ex_dividend_date='2022-06-10')
        assert ex.value.args[0] == "'cik' must be <class 'str'> (got 345 that is a <class 'int'>)."

    def test_cik_wrong_length(self) -> None:
        with pytest.raises(ValueError) as ex:
            model.Company(ticker='xxxxx', name='IBM Corporation', description='Test', cik='0123456',
                          figi='012345678912',
                          exchange='NYSE', currency='USD', country='USA', sector='Test Sector',
                          industry='Test Industry',
                          address='Main Street', fiscal_year_end='December', last_quarter='2022-03-31',
                          dividend_date='2022-06-10', ex_dividend_date='2022-06-10')

        assert ex.value.args[0] == "'cik' must match regex '^[0-9]{10,10}$' ('0123456' doesn't)"

    def test_cik(self) -> None:
        record = model.Company(ticker='xxxxx', name='IBM Corporation', description='Test', cik='0123456789',
                               figi='012345678912',
                               exchange='NYSE', currency='USD', country='USA', sector='Test Sector',
                               industry='Test Industry',
                               address='Main Street', fiscal_year_end='December', last_quarter='2022-03-31',
                               dividend_date='2022-06-10', ex_dividend_date='2022-06-10')

        assert record.cik == '0123456789'

    def test_figi_wrong_type(self) -> None:
        with pytest.raises(TypeError) as ex:
            model.Company(ticker='xxxxx', name='IBM Corporation', description='Test', cik='0123456789',
                          figi=123, exchange='NYSE', currency='USD', country='USA', sector='Test Sector',
                          industry='Test Industry', address='Main Street', fiscal_year_end='December',
                          last_quarter='2022-03-31', dividend_date='2022-06-10', ex_dividend_date='2022-06-10')
        assert ex.value.args[0] == "'figi' must be <class 'str'> (got 123 that is a <class 'int'>)."

    def test_figi_wrong_length(self) -> None:
        with pytest.raises(ValueError) as ex:
            model.Company(ticker='xxxxx', name='IBM Corporation', description='Test', cik='0123456789',
                          figi='2333', exchange='NYSE', currency='USD', country='USA', sector='Test Sector',
                          industry='Test Industry', address='Main Street', fiscal_year_end='December',
                          last_quarter='2022-03-31', dividend_date='2022-06-10', ex_dividend_date='2022-06-10')
        assert ex.value.args[0] == "'figi' must match regex '^[0-9]{12,12}$' ('2333' doesn't)"

    def test_figi(self) -> None:
        record = model.Company(ticker='xxxxx', name='IBM Corporation', description='Test', cik='0123456789',
                               figi='012345678912', exchange='NYSE', currency='USD', country='USA',
                               sector='Test Sector',
                               industry='Test Industry', address='Main Street', fiscal_year_end='December',
                               last_quarter='2022-03-31', dividend_date='2022-06-10', ex_dividend_date='2022-06-10')
        assert record.figi == '012345678912'

    def test_not_equal(self) -> None:
        record_1 = model.Company(ticker='xxxxx', name='IBM Corporation', description='Test', cik='0123456789',
                                 figi='129876543210', exchange='NYSE', currency='USD', country='USA',
                                 sector='Test Sector',
                                 industry='Test Industry', address='Main Street', fiscal_year_end='December',
                                 last_quarter='2022-03-31', dividend_date='2022-06-10', ex_dividend_date='2022-06-10')
        record_2 = model.Company(ticker='xxxxx', name='IBM Corporation', description='Test', cik='0123456789',
                                 figi='012345678912', exchange='NYSE', currency='USD', country='USA',
                                 sector='Test Sector',
                                 industry='Test Industry', address='Main Street', fiscal_year_end='December',
                                 last_quarter='2022-03-31', dividend_date='2022-06-10', ex_dividend_date='2022-06-10')

        assert record_1 != record_2

    def test_equal(self) -> None:
        record_1 = model.Company(ticker='xxxxx', name='IBM Corporation', description='Test', cik='0123456789',
                                 figi='012345678912', exchange='NYSE', currency='USD', country='USA',
                                 sector='Test Sector',
                                 industry='Test Industry', address='Main Street', fiscal_year_end='December',
                                 last_quarter='2022-03-31', dividend_date='2022-06-10', ex_dividend_date='2022-06-10')
        record_2 = model.Company(ticker='xxxxx', name='IBM Corporation', description='Test', cik='0123456789',
                                 figi='012345678912', exchange='NYSE', currency='USD', country='USA',
                                 sector='Test Sector',
                                 industry='Test Industry', address='Main Street', fiscal_year_end='December',
                                 last_quarter='2022-03-31', dividend_date='2022-06-10', ex_dividend_date='2022-06-10')

        assert record_1 == record_2


class TestPeriodEnds:
    # noinspection PyDataclass
    def test_are_not_equal(self):
        dt_1 = pendulum.date(2022, 5, 24)
        dt_2 = pendulum.date(2022, 5, 25)

        record_1 = model.PeriodEnds()
        record_1 = attrs.evolve(record_1, period_1=dt_1, period_2=dt_1, period_3=dt_1, period_4=dt_1, period_5=dt_1)

        record_2 = model.PeriodEnds()
        record_2 = attrs.evolve(record_2, period_1=dt_2, period_2=dt_1, period_3=dt_1, period_4=dt_1, period_5=dt_1)

        assert record_1 != record_2

    # noinspection PyDataclass
    def test_are_equal(self):
        dt = pendulum.date(2022, 5, 24)

        record_1 = model.PeriodEnds()
        record_1 = attrs.evolve(record_1, period_1=dt, period_2=dt, period_3=dt, period_4=dt, period_5=dt)

        record_2 = model.PeriodEnds()
        record_2 = attrs.evolve(record_2, period_1=dt, period_2=dt, period_3=dt, period_4=dt, period_5=dt)

        assert record_1 == record_2


class TestAccountingItem:
    def test_tag_wrong_type(self) -> None:
        with pytest.raises(TypeError) as ex:
            model.AccountingItem(tag=23)
        assert ex.value.args[0] == "'tag' must be <class 'str'> (got 23 that is a <class 'int'>)."

    def test_tag_wrong_length(self) -> None:
        with pytest.raises(ValueError) as ex:
            model.AccountingItem(tag='Aa')
        assert ex.value.args[0] == "'tag' must match regex '^[A-Za-z0-9]{4,60}$' ('Aa' doesn't)"

    def test_tag(self) -> None:
        record = model.AccountingItem(tag='CashAndNearCashItems')
        assert record.tag == 'CashAndNearCashItems'

    # noinspection PyDataclass
    def test_are_equal(self) -> None:
        record_1 = model.AccountingItem(tag='CashAndNearCashItems')
        record_1 = attrs.evolve(record_1, period_1=23)

        record_2 = model.AccountingItem(tag='CashAndNearCashItems')

        assert record_1 == record_2

    def test_are_not_equal(self) -> None:
        record_1 = model.AccountingItem(tag='Creditors')
        record_2 = model.AccountingItem(tag='CashAndNearCashItems')

        assert record_1 != record_2


class TestAccountingStatement:
    def test_ticker_wrong_type(self) -> None:
        with pytest.raises(TypeError) as ex:
            model.AccountingStatement(ticker=23)
        assert ex.value.args[0] == "'ticker' must be <class 'str'> (got 23 that is a <class 'int'>)."

    def test_ticker_wrong_length(self) -> None:
        with pytest.raises(ValueError) as ex:
            model.AccountingStatement(ticker='XXXXXX')
        assert ex.value.args[0] == "'ticker' must match regex '^[A-Z0-9]{1,5}$' ('XXXXXX' doesn't)"

    def test_ticker(self) -> None:
        record = model.AccountingStatement(ticker='IBM')
        assert record.ticker == 'IBM'

    def test_are_equal(self) -> None:
        record_1 = model.AccountingStatement(ticker='IBM')
        record_2 = model.AccountingStatement(ticker='IBM')

        assert record_1 == record_2

    def test_are_not_equal(self) -> None:
        record_1 = model.AccountingStatement(ticker='IBM')
        record_2 = model.AccountingStatement(ticker='AAPL')

        assert record_1 != record_2

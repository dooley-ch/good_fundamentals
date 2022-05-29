# *******************************************************************************************
#  File:  _database.py
#
#  Created: 28-05-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  28-05-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['MasterList', 'Company', 'PeriodEnds', 'AccountingItem', 'AccountingStatement']

from datetime import datetime, date
import pendulum
import attrs
import attrs.validators as validators


def _ticker_to_upper_case(value: str) -> str:
    """
    This function converts the given value to an upper case value
    """
    if isinstance(value, str):
        return value.upper()

    return value


def _date_str_to_date(value: str) -> date:
    return pendulum.parse(value, strict=False)


@attrs.frozen(kw_only=True)
class MasterList:
    ticker: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('^[A-Z0-9]{1,5}$')],
                              converter=_ticker_to_upper_case)
    name: str = attrs.field(eq=False, validator=[validators.instance_of(str),
                                                 validators.matches_re('^[A-Za-z0-9 _]{4,120}$')])
    cik: str = attrs.field(eq=False, validator=[validators.instance_of(str), validators.matches_re('^[0-9]{10,10}$')])
    figi: str = attrs.field(eq=False, validator=[validators.instance_of(str), validators.matches_re('^[0-9]{12,12}$')])
    sector: str = attrs.field(eq=False, validator=[validators.instance_of(str),
                                                   validators.matches_re('^[A-Za-z0-9 _]{4,100}$')])
    industry: str = attrs.field(eq=False, validator=[validators.instance_of(str),
                                                     validators.matches_re('^[A-Za-z0-9 _]{4,100}$')])
    lock_version: int = attrs.field(default=1, eq=False, validator=[validators.instance_of(int), validators.gt(0)])
    created_at: datetime = attrs.field(eq=False, factory=datetime.now, validator=[validators.instance_of(datetime)])
    updated_at: datetime = attrs.field(eq=False, factory=datetime.now, validator=[validators.instance_of(datetime)])


@attrs.frozen(kw_only=True)
class Company:
    ticker: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('^[A-Z0-9]{1,5}$')],
                              converter=_ticker_to_upper_case)
    name: str = attrs.field(eq=False, validator=[validators.instance_of(str),
                                                 validators.matches_re('^[A-Za-z0-9 _]{4,120}$')])
    description: str = attrs.field(eq=False, validator=[validators.instance_of(str),
                                                        validators.matches_re('^[A-Za-z0-9 _]{4,5000}$')])
    cik: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('^[0-9]{10,10}$')])
    figi: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('^[0-9]{12,12}$')])
    exchange: str = attrs.field(eq=False, validator=[validators.instance_of(str),
                                                     validators.matches_re('^[A-Za-z]{1,60}$')])
    currency: str = attrs.field(eq=False, validator=[validators.instance_of(str),
                                                     validators.matches_re('^[A-Z]{3,3}$')])
    country: str = attrs.field(eq=False, validator=[validators.instance_of(str),
                                                    validators.matches_re('^[A-Z]{3,3}$')])
    sector: str = attrs.field(eq=False, validator=[validators.instance_of(str),
                                                   validators.matches_re('^[A-Za-z0-9 _]{4,100}$')])
    industry: str = attrs.field(eq=False, validator=[validators.instance_of(str),
                                                     validators.matches_re('^[A-Za-z0-9 _]{4,100}$')])
    address: str = attrs.field(eq=False, validator=[validators.instance_of(str),
                                                    validators.matches_re('^[A-Za-z0-9 _]{4,120}$')])
    fiscal_year_end: str = attrs.field(eq=False, validator=[validators.instance_of(str),
                                                            validators.matches_re('^[A-Za-z0-9 _]{4,100}$')])
    last_quarter: datetime = attrs.field(eq=False, factory=datetime.now, validator=[validators.instance_of(datetime)],
                                         converter=_date_str_to_date)
    dividend_date: datetime = attrs.field(eq=False, factory=datetime.now, validator=[validators.instance_of(datetime)],
                                          converter=_date_str_to_date)
    ex_dividend_date: datetime = attrs.field(eq=False, factory=datetime.now,
                                             validator=[validators.instance_of(datetime)], converter=_date_str_to_date)
    lock_version: int = attrs.field(default=1, eq=False, validator=[validators.instance_of(int), validators.gt(0)])
    created_at: datetime = attrs.field(eq=False, factory=datetime.now, validator=[validators.instance_of(datetime)])
    updated_at: datetime = attrs.field(eq=False, factory=datetime.now, validator=[validators.instance_of(datetime)])


@attrs.frozen(kw_only=True)
class PeriodEnds:
    period_1: date = attrs.field(factory=datetime.now, validator=[validators.instance_of(date)])
    period_2: date = attrs.field(factory=datetime.now, validator=[validators.instance_of(date)])
    period_3: date = attrs.field(factory=datetime.now, validator=[validators.instance_of(date)])
    period_4: date = attrs.field(factory=datetime.now, validator=[validators.instance_of(date)])
    period_5: date = attrs.field(factory=datetime.now, validator=[validators.instance_of(date)])


@attrs.frozen(kw_only=True)
class AccountingItem:
    tag: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('^[A-Za-z0-9]{4,60}$')])
    period_1: int = attrs.field(default=0, eq=False, validator=[validators.instance_of(int)])
    period_2: int = attrs.field(default=0, eq=False, validator=[validators.instance_of(int)])
    period_3: int = attrs.field(default=0, eq=False, validator=[validators.instance_of(int)])
    period_4: int = attrs.field(default=0, eq=False, validator=[validators.instance_of(int)])
    period_5: int = attrs.field(default=0, eq=False, validator=[validators.instance_of(int)])


@attrs.frozen(kw_only=True)
class AccountingStatement:
    ticker: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('^[A-Z0-9]{1,5}$')],
                              converter=_ticker_to_upper_case)
    periods: PeriodEnds = attrs.field(eq=False, factory=PeriodEnds)
    items: list[AccountingItem] = attrs.field(eq=False, factory=list)
    lock_version: int = attrs.field(default=1, eq=False, validator=[validators.instance_of(int), validators.gt(0)])
    created_at: datetime = attrs.field(eq=False, factory=datetime.now, validator=[validators.instance_of(datetime)])
    updated_at: datetime = attrs.field(eq=False, factory=datetime.now, validator=[validators.instance_of(datetime)])

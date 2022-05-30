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
__all__ = ['PeriodType', 'Months', 'DocumentMetaData', 'Master', 'Company', 'PeriodEnds', 'AccountingItem',
           'AccountingStatement', 'IncomeStatement', 'CashFlow', 'BalanceSheet', 'EarningsStatement',
           'GicsClassification']

from typing import NewType
from enum import Enum
from datetime import datetime, date
import pendulum
import attrs
import attrs.validators as validators


def string_to_date(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        return value
    return pendulum.parse(value, strict=False)

class PeriodType(str, Enum):
    """
    Differentiates annual from quarterly financial statements
    """
    Annual = 'Annual'
    Quarter = 'Quarter'


class Months(str, Enum):
    """
    Defines the months of the year
    """
    January = 'January'
    February = 'February'
    March = 'March'
    April = 'April'
    May = 'May'
    June = 'June'
    July = 'July'
    August = 'August'
    September = 'September'
    October = 'October'
    November = 'November'
    December = 'December'


@attrs.define
class DocumentMetaData:
    """
    Holds metadata about a document stored in the database
    """
    lock_version: int = attrs.field(default=1, validator=[validators.instance_of(int), validators.gt(0)])
    created_at: datetime = attrs.field(factory=datetime.now, validator=[validators.instance_of(datetime)])
    updated_at: datetime = attrs.field(factory=datetime.now, validator=[validators.instance_of(datetime)])

    def prep_for_update(self) -> None:
        self.lock_version += 1
        self.updated_at = datetime.now()

    def init_for_insert(self) -> None:
        self.lock_version = 1
        self.created_at = datetime.now()
        self.updated_at = self.created_at


@attrs.frozen
class Master:
    ticker: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('^[A-Z]{1,5}$')],
                              converter=lambda value: value.upper())
    name: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('[A-Za-z .]{5,120}$')])
    cik: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('^[0-9]{10,10}$')])
    figi: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('^[0-9]{12,12}$')])
    sector: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('[A-Za-z ]{5,80}$')])
    industry: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('[A-Za-z ]{5,80}$')])
    metadata: DocumentMetaData = attrs.field(factory=DocumentMetaData,
                                             validator=[validators.instance_of(DocumentMetaData)])


@attrs.define
class GicsClassification:
    sector: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('[A-Za-z]{5,80}$')])
    industries: list[str] = attrs.Factory(list)


@attrs.define
class Company:
    ticker: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('^[A-Z]{1,5}$')],
                              converter=lambda value: value.upper())
    name: str = attrs.field(eq=False,
                            validator=[validators.instance_of(str), validators.matches_re('[A-Za-z .]{5,120}$')])
    description: str = attrs.field(eq=False, validator=[validators.instance_of(str)])
    cik: str = attrs.field(eq=False, validator=[validators.instance_of(str), validators.matches_re('^[0-9]{10,10}$')])
    figi: str = attrs.field(eq=False, validator=[validators.instance_of(str), validators.matches_re('^[0-9]{12,12}$')])
    exchange: str = attrs.field(eq=False, validator=[validators.instance_of(str)])
    currency: str = attrs.field(eq=False,
                                validator=[validators.instance_of(str), validators.matches_re('^[A-Z]{3,3}$')])
    country: str = attrs.field(eq=False,
                               validator=[validators.instance_of(str), validators.matches_re('[A-Za-z ]{1,80}$')])
    sector: str = attrs.field(eq=False,
                              validator=[validators.instance_of(str), validators.matches_re('[A-Za-z]{5,80}$')])
    industry: str = attrs.field(eq=False,
                                validator=[validators.instance_of(str), validators.matches_re('[A-Za-z]{5,80}$')])
    address: str = attrs.field(eq=False, validator=[validators.instance_of(str)])
    fiscal_year_end: str = attrs.field(eq=False, validator=[validators.instance_of(str), validators.in_(Months)])
    last_quarter: datetime = attrs.field(eq=False, factory=datetime.now, validator=[validators.instance_of(datetime)],
                                         converter=lambda value: pendulum.parse(value, strict=False))
    dividend_date: datetime = attrs.field(eq=False, factory=datetime.now, validator=[validators.instance_of(datetime)],
                                          converter=lambda value: pendulum.parse(value, strict=False))
    ex_dividend_date: datetime = attrs.field(eq=False, factory=datetime.now,
                                             validator=[validators.instance_of(datetime)],
                                             converter=lambda value: pendulum.parse(value, strict=False))
    metadata: DocumentMetaData = attrs.field(eq=False, factory=DocumentMetaData,
                                             validator=[validators.instance_of(DocumentMetaData)])


@attrs.define
class PeriodEnds:
    """
    Holds the accounting dates for the data in the financial statement
    """
    period_1: date = attrs.field(factory=datetime.now, validator=[validators.instance_of(date)])
    period_2: date = attrs.field(factory=datetime.now, validator=[validators.instance_of(date)])
    period_3: date = attrs.field(factory=datetime.now, validator=[validators.instance_of(date)])
    period_4: date = attrs.field(factory=datetime.now, validator=[validators.instance_of(date)])
    period_5: date = attrs.field(factory=datetime.now, validator=[validators.instance_of(date)])


@attrs.define
class AccountingItem:
    """
    Holds the details of a single entry in a financial statement
    """
    tag: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('[A-Za-z]{4,100}$')])
    period_1: int = attrs.field(default=0, eq=False, validator=[validators.instance_of(int)])
    period_2: int = attrs.field(default=0, eq=False, validator=[validators.instance_of(int)])
    period_3: int = attrs.field(default=0, eq=False, validator=[validators.instance_of(int)])
    period_4: int = attrs.field(default=0, eq=False, validator=[validators.instance_of(int)])
    period_5: int = attrs.field(default=0, eq=False, validator=[validators.instance_of(int)])


@attrs.define
class AccountingStatement:
    """
    Holds the details of an accounting statement
    """
    ticker: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('^[A-Z]{1,5}$')])
    period_type: PeriodType = attrs.field(validator=[validators.instance_of(PeriodType)])
    period_ends: PeriodEnds = attrs.field(eq=False, factory=PeriodEnds)
    items: list[AccountingItem] = attrs.field(eq=False, factory=list)
    metadata: DocumentMetaData = attrs.field(eq=False, factory=DocumentMetaData)


IncomeStatement = NewType('IncomeStatement', AccountingStatement)
CashFlow = NewType('CashFlow', AccountingStatement)
BalanceSheet = NewType('BalanceSheet', AccountingStatement)
EarningsStatement = NewType('EarningsStatement', AccountingStatement)

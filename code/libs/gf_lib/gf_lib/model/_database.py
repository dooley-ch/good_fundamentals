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

from __future__ import annotations

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['PeriodType', 'IndexType', 'Months', 'DocumentMetadata', 'Master', 'Company', 'AccountingEntry',
           'IncomeStatement', 'CashFlowStatement', 'BalanceSheetStatement', 'EarningsStatement',
           'GICSSubIndustry', 'GICSIndustry', 'GICSGroupIndustry', 'GICSSector', 'TaskTracking', 'Earnings']

from enum import Enum
from datetime import datetime, date
import pendulum
import attrs
import attrs.validators as validators


def parse_alphavantage_date(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        return value
    return pendulum.parse(value, strict=False)


class Months(str, Enum):
    January = 'january'
    February = 'february'
    March = 'march'
    April = 'april'
    May = 'may'
    June = 'june'
    July = 'july'
    August = 'august'
    September = 'september'
    October = 'october'
    November = 'november'
    December = 'december'

    @classmethod
    def parse(cls, value: str | Months) -> Months:
        if isinstance(value, Months):
            return value

        return Months(value.lower())


class IndexType(str, Enum):
    SP100 = 'sp100'
    SP600 = 'sp600'
    SP400 = 'sp400'
    SP500 = 'sp500'

    @classmethod
    def parse(cls, value: str | IndexType) -> IndexType:
        if isinstance(value, IndexType):
            return value

        return IndexType(value.lower())


class PeriodType(str, Enum):
    Annual = 'annual'
    Quarter = 'quarter'

    @classmethod
    def parse(cls, value: str | PeriodType) -> PeriodType:
        if isinstance(value, PeriodType):
            return value

        return PeriodType(value)


@attrs.define(kw_only=True)
class DocumentMetadata:
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

    @classmethod
    def parse(cls, value: dict | DocumentMetadata) -> DocumentMetadata:
        """
        This function converts the metadata dict to an instance of the class
        """
        if isinstance(value, DocumentMetadata):
            return value

        return DocumentMetadata(**value)


@attrs.frozen
class AccountingEntry:
    tag: str
    value_1: str = attrs.field(default='', validator=[attrs.validators.instance_of(str)])
    value_2: str = attrs.field(default='', validator=[attrs.validators.instance_of(str)])
    value_3: str = attrs.field(default='', validator=[attrs.validators.instance_of(str)])
    value_4: str = attrs.field(default='', validator=[attrs.validators.instance_of(str)])
    value_5: str = attrs.field(default='', validator=[attrs.validators.instance_of(str)])


@attrs.frozen
class Master:
    ticker: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('^[A-Z.-]{1,5}$')],
                              converter=lambda value: value.upper())
    name: str = attrs.field(eq=False, validator=[validators.instance_of(str)])
    cik: str = attrs.field(eq=False, validator=[validators.instance_of(str), validators.matches_re('^[0-9]{10,10}$')],
                           converter=lambda value: value.zfill(10))
    figi: str = attrs.field(eq=False,
                            validator=[validators.instance_of(str), validators.matches_re('^[0-9A-Z]{12,12}$')],
                            converter=lambda value: value.zfill(12))
    sub_industry: str = attrs.field(eq=False, validator=[validators.instance_of(str)])
    indexes: list[IndexType] = attrs.field(eq=False, factory=list)
    metadata: DocumentMetadata = attrs.field(eq=False, factory=DocumentMetadata,
                                             validator=[validators.instance_of(DocumentMetadata)],
                                             converter=DocumentMetadata.parse)


@attrs.frozen
class IncomeStatement:
    ticker: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('^[A-Z.-]{1,5}$')],
                              converter=lambda value: value.upper())
    period_type: PeriodType = attrs.field(default=PeriodType.Annual, converter=PeriodType.parse)
    items: list[AccountingEntry] = attrs.field(factory=list)
    metadata: DocumentMetadata = attrs.field(eq=False, factory=DocumentMetadata,
                                             validator=[validators.instance_of(DocumentMetadata)],
                                             converter=DocumentMetadata.parse)


@attrs.frozen
class CashFlowStatement:
    ticker: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('^[A-Z.-]{1,5}$')],
                              converter=lambda value: value.upper())
    period_type: PeriodType = attrs.field(default=PeriodType.Annual, converter=PeriodType.parse)
    items: list[AccountingEntry] = attrs.field(factory=list)
    metadata: DocumentMetadata = attrs.field(eq=False, factory=DocumentMetadata,
                                             validator=[validators.instance_of(DocumentMetadata)],
                                             converter=DocumentMetadata.parse)


@attrs.frozen
class BalanceSheetStatement:
    ticker: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('^[A-Z.-]{1,5}$')],
                              converter=lambda value: value.upper())
    period_type: PeriodType = attrs.field(default=PeriodType.Annual, converter=PeriodType.parse)
    items: list[AccountingEntry] = attrs.field(factory=list)
    metadata: DocumentMetadata = attrs.field(eq=False, factory=DocumentMetadata,
                                             validator=[validators.instance_of(DocumentMetadata)],
                                             converter=DocumentMetadata.parse)


@attrs.frozen
class EarningsStatement:
    ticker: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('^[A-Z.-]{1,5}$')],
                              converter=lambda value: value.upper())
    period_type: PeriodType = attrs.field(default=PeriodType.Annual, converter=PeriodType.parse)
    items: list[AccountingEntry] = attrs.field(factory=list)
    metadata: DocumentMetadata = attrs.field(eq=False, factory=DocumentMetadata,
                                             validator=[validators.instance_of(DocumentMetadata)],
                                             converter=DocumentMetadata.parse)


@attrs.define
class TaskTracking:
    master_loaded: bool = attrs.field(default=False)
    cik_loaded: bool = attrs.field(default=False)
    figi_loaded: bool = attrs.field(default=False)
    earnings_file_loaded: bool = attrs.field(default=False)
    metadata: DocumentMetadata = attrs.field(eq=False, factory=DocumentMetadata,
                                             validator=[validators.instance_of(DocumentMetadata)],
                                             converter=DocumentMetadata.parse)


@attrs.frozen
class GICSSubIndustry:
    id: int = attrs.field(default=10_000_001, validator=[attrs.validators.instance_of(int), attrs.validators.gt(10_000_000),
                                                attrs.validators.lt(61_000_000)], converter=int)
    name: str = attrs.field(default='Unknown', validator=[attrs.validators.instance_of(str)])


@attrs.frozen
class GICSIndustry:
    id: int = attrs.field(default=100_001, validator=[attrs.validators.instance_of(int), attrs.validators.gt(100_000),
                                                attrs.validators.lt(610_000)], converter=int)
    name: str = attrs.field(default='Unknown', validator=[attrs.validators.instance_of(str)])
    sub_industries: list[GICSSubIndustry] = attrs.Factory(list)


@attrs.frozen
class GICSGroupIndustry:
    id: int = attrs.field(default=1_001, validator=[attrs.validators.instance_of(int), attrs.validators.gt(1_000),
                                                attrs.validators.lt(6_100)], converter=int)
    name: str = attrs.field(default='Unknown', validator=[attrs.validators.instance_of(str)])
    industries: list[GICSIndustry] = attrs.Factory(list)


@attrs.frozen
class GICSSector:
    id: int = attrs.field(default=11, validator=[attrs.validators.instance_of(int), attrs.validators.gt(9),
                                                attrs.validators.lt(61)], converter=int)
    name: str = attrs.field(default='Unknown', validator=[attrs.validators.instance_of(str)])
    group_industries: list[GICSGroupIndustry] = attrs.Factory(list)
    metadata: DocumentMetadata = attrs.field(eq=False, factory=DocumentMetadata,
                                             validator=[validators.instance_of(DocumentMetadata)],
                                             converter=DocumentMetadata.parse)


@attrs.define
class Earnings:
    ticker: str = attrs.field(eq=True, validator=[validators.instance_of(str), validators.matches_re('^[A-Z.-]{1,5}$')],
                              converter=lambda value: value.upper())
    name: str = attrs.field(default='', eq=False, validator=[attrs.validators.instance_of(str)])
    report_date: date = attrs.field(eq=False, factory=datetime.now)
    fiscal_year: date = attrs.field(eq=False, factory=datetime.now)
    estimate: str = attrs.field(default='', eq=False)
    currency: str = attrs.field(default='USD')
    metadata: DocumentMetadata = attrs.field(eq=False, factory=DocumentMetadata,
                                             validator=[validators.instance_of(DocumentMetadata)],
                                             converter=DocumentMetadata.parse)


@attrs.define
class Company:
    ticker: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('^[A-Z]{1,5}$')],
                              converter=lambda value: value.upper())
    name: str = attrs.field(eq=False, validator=[validators.instance_of(str)])
    description: str = attrs.field(eq=False, validator=[validators.instance_of(str)])
    cik: str = attrs.field(eq=False, validator=[validators.instance_of(str), validators.matches_re('^[0-9]{10,10}$')])
    figi: str = attrs.field(eq=False, validator=[validators.instance_of(str), validators.matches_re('^[0-9]{12,12}$')])
    exchange: str = attrs.field(eq=False, validator=[validators.instance_of(str)])
    currency: str = attrs.field(eq=False,
                                validator=[validators.instance_of(str), validators.matches_re('^[A-Z]{3,3}$')])
    country: str = attrs.field(eq=False, validator=[validators.instance_of(str)])
    sub_industry: str = attrs.field(eq=False, validator=[validators.instance_of(str)])
    address: str = attrs.field(eq=False, validator=[validators.instance_of(str)])
    fiscal_year_end: str = attrs.field(eq=False, validator=[validators.instance_of(str), validators.in_(Months)],
                                       converter=Months.parse)
    last_quarter: datetime = attrs.field(eq=False, factory=datetime.now, validator=[validators.instance_of(datetime)],
                                         converter=parse_alphavantage_date)
    metadata: DocumentMetadata = attrs.field(eq=False, factory=DocumentMetadata,
                                             validator=[validators.instance_of(DocumentMetadata)],
                                             converter=DocumentMetadata.parse)

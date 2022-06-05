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
           'AccountingStatement', 'GicsClassification', 'TaskControl']

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


def to_period_type(value: str | PeriodType) -> PeriodType:
    if isinstance(value, PeriodType):
        return value

    return PeriodType(value)


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


def to_months(value: str | Months) -> Months:
    if isinstance(value, Months):
        return value

    return Months(value)


@attrs.frozen
class TaskControl:
    cik_loaded: bool = attrs.field(default=False, validator=[validators.instance_of(bool)])
    figi_loaded: bool = attrs.field(default=False, validator=[validators.instance_of(bool)])


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


def to_document_metadata(value: dict | DocumentMetaData) -> DocumentMetaData:
    """
    This function converts the metadata dict to an instance of the class
    """
    if isinstance(value, DocumentMetaData):
        return value

    return DocumentMetaData(**value)


@attrs.frozen
class TaskControl:
    cik_loaded: bool = attrs.field(default=False, validator=[validators.instance_of(bool)])
    figi_loaded: bool = attrs.field(default=False, validator=[validators.instance_of(bool)])
    metadata: DocumentMetaData = attrs.field(eq=False, factory=DocumentMetaData,
                                             validator=[validators.instance_of(DocumentMetaData)],
                                             converter=to_document_metadata)


@attrs.frozen(kw_only=True)
class Master:
    """
    This is the record for an entry in the master list of financial instruments used by the application
    """
    ticker: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('^[A-Z.-]{1,5}$')],
                              converter=lambda value: value.upper())
    name: str = attrs.field(eq=False, validator=[validators.instance_of(str)])
    cik: str = attrs.field(eq=False, validator=[validators.instance_of(str), validators.matches_re('^[0-9]{10,10}$')],
                           converter=lambda value: value.zfill(10))
    figi: str = attrs.field(eq=False,
                            validator=[validators.instance_of(str), validators.matches_re('^[0-9A-Z]{12,12}$')],
                            converter=lambda value: value.zfill(12))
    sub_industry: str = attrs.field(eq=False, validator=[validators.instance_of(str)])
    indexes: list[str] = attrs.Factory(list)
    metadata: DocumentMetaData = attrs.field(eq=False, factory=DocumentMetaData,
                                             validator=[validators.instance_of(DocumentMetaData)],
                                             converter=to_document_metadata)


@attrs.define
class GicsClassification:
    sector: str = attrs.field(validator=[validators.instance_of(str), validators.matches_re('[A-Za-z .]{5,80}$')])
    industry: list[str] = attrs.Factory(list)
    metadata: DocumentMetaData = attrs.field(factory=DocumentMetaData,
                                             validator=[validators.instance_of(DocumentMetaData)],
                                             converter=to_document_metadata)


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
                              validator=[validators.instance_of(str), validators.matches_re('[A-Za-z .]{5,80}$')])
    industry: str = attrs.field(eq=False,
                                validator=[validators.instance_of(str), validators.matches_re('[A-Za-z .]{5,80}$')])
    address: str = attrs.field(eq=False, validator=[validators.instance_of(str)])
    fiscal_year_end: str = attrs.field(eq=False, validator=[validators.instance_of(str), validators.in_(Months)],
                                       converter=to_months)
    last_quarter: datetime = attrs.field(eq=False, factory=datetime.now, validator=[validators.instance_of(datetime)],
                                         converter=string_to_date)
    dividend_date: datetime = attrs.field(eq=False, factory=datetime.now, validator=[validators.instance_of(datetime)],
                                          converter=string_to_date)
    ex_dividend_date: datetime = attrs.field(eq=False, factory=datetime.now,
                                             validator=[validators.instance_of(datetime)],
                                             converter=string_to_date)
    metadata: DocumentMetaData = attrs.field(eq=False, factory=DocumentMetaData,
                                             validator=[validators.instance_of(DocumentMetaData)],
                                             converter=to_document_metadata)


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
    period_type: PeriodType = attrs.field(validator=[validators.instance_of(PeriodType)], converter=to_period_type)
    period_ends: PeriodEnds = attrs.field(eq=False, factory=PeriodEnds)
    items: list[AccountingItem] = attrs.field(eq=False, factory=list)
    metadata: DocumentMetaData = attrs.field(eq=False, factory=DocumentMetaData)

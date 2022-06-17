# *******************************************************************************************
#  File:  _statement.py
#
#  Created: 31-05-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  31-05-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['CashFlowDatastore', 'BalanceSheetDatastore', 'IncomeDatastore', 'EarningsDatastore']

from typing import TypeVar
from attrs import asdict
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertManyResult
from pymongo.errors import DuplicateKeyError
from gf_lib.model import PeriodType, CashFlowStatement, BalanceSheetStatement, IncomeStatement, EarningsStatement
from gf_lib.errors import DuplicateRecordError


T = TypeVar("T")

class _StatemetDatastore:
    _collection: Collection
    _statement_class: T

    def __init__(self, database: Database, collection: str, statement_class: T) -> None:
        self._collection = database[collection]
        self._statement_class = statement_class

    def insert(self, value: T) -> bool:
        try:
            data = asdict(value)
            results: InsertManyResult = self._collection.insert_one(data)
        except DuplicateKeyError:
            raise DuplicateRecordError(value.ticker)
        else:
            return results.acknowledged

    def get(self, ticker: str, period: PeriodType) -> T | None:
        raw_data = self._collection.find_one({'ticker': ticker, 'period_type': period.value}, {'_id': 0})

        if raw_data:
            return self._statement_class(**raw_data)

    def clear(self) -> None:
        self._collection.delete_many({})


class CashFlowDatastore(_StatemetDatastore):
    def __init__(self, database: Database):
        super().__init__(database, 'cash_flow_statement', CashFlowStatement)


class BalanceSheetDatastore(_StatemetDatastore):
    def __init__(self, database: Database):
        super().__init__(database, 'balance_sheet_statement', BalanceSheetStatement)


class IncomeDatastore(_StatemetDatastore):
    def __init__(self, database: Database):
        super().__init__(database, 'income_statement', IncomeStatement)


class EarningsDatastore(_StatemetDatastore):
    def __init__(self, database: Database):
        super().__init__(database, 'earnings_statement', EarningsStatement)

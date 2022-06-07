# *******************************************************************************************
#  File:  _alphavantage.py
#
#  Created: 07-06-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  07-06-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['parse_financial_statements']

import attrs
import orjson


@attrs.define
class FinancialItem:
    tag: str
    column_1: str | None = attrs.field(default=None)
    column_2: str | None = attrs.field(default=None)
    column_3: str | None = attrs.field(default=None)
    column_4: str | None = attrs.field(default=None)
    column_5: str | None = attrs.field(default=None)


@attrs.frozen
class FinancialStatements:
    ticker: str
    items: dict[str, FinancialItem] = attrs.Factory(dict)


def parse_financial_statements(value: str, annual_tag: str = 'annualReports', quarter_tag: str = 'quarterlyReports'):
    data = orjson.loads(value)

    ticker = data['symbol']
    annual_statements = FinancialStatements(ticker)
    quarter_statements = FinancialStatements(ticker)

    annuals = data[annual_tag]
    quarters = data[quarter_tag]

    for index, statement in enumerate(annuals):
        if index > 4:
            break

        for key, value in statement.items():
            if key not in annual_statements.items:
                annual_statements.items[key] = FinancialItem(key)

            match index:
                case 0: annual_statements.items[key].column_1 = value
                case 1: annual_statements.items[key].column_2 = value
                case 2: annual_statements.items[key].column_3 = value
                case 3: annual_statements.items[key].column_4 = value
                case 4: annual_statements.items[key].column_5 = value

    for index, statement in enumerate(quarters):
        if index > 2:
            break

        for key, value in statement.items():
            if key not in quarter_statements.items:
                quarter_statements.items[key] = FinancialItem(key)

            match index:
                case 0: quarter_statements.items[key].column_1 = value
                case 1: quarter_statements.items[key].column_2 = value
                case 2: quarter_statements.items[key].column_3 = value

    return annual_statements, quarter_statements

# *******************************************************************************************
#  File:  _alphavantage.py
#
#  Created: 12-06-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  12-06-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['FinancialItemAlphavantage', 'FinancialStatementsAlphavantage', 'CompanyAlphavantage', 'AlphavantageData',
           'EarningsAlphavantage']

import attrs


@attrs.define
class FinancialItemAlphavantage:
    tag: str
    column_1: str | None = attrs.field(default=None)
    column_2: str | None = attrs.field(default=None)
    column_3: str | None = attrs.field(default=None)
    column_4: str | None = attrs.field(default=None)
    column_5: str | None = attrs.field(default=None)


@attrs.frozen
class FinancialStatementsAlphavantage:
    ticker: str
    items: dict[str, FinancialItemAlphavantage] = attrs.Factory(dict)


@attrs.define
class CompanyAlphavantage:
    ticker: str
    name: str
    description: str
    exchange: str
    currency: str
    country: str
    address: str
    fiscal_year_end: str
    last_quarter: str


@attrs.frozen
class EarningsAlphavantage:
    ticker: str
    name: str
    report_date: str
    fiscal_year: str
    estimate: str
    currency: str


@attrs.frozen
class AlphavantageData:
    company: CompanyAlphavantage
    income_annual: FinancialStatementsAlphavantage
    income_quarter: FinancialStatementsAlphavantage
    balance_sheet_annual: FinancialStatementsAlphavantage
    balance_sheet_quarter: FinancialStatementsAlphavantage
    cashflow_annual: FinancialStatementsAlphavantage
    cashflow_quarter: FinancialStatementsAlphavantage
    earnings_annual: FinancialStatementsAlphavantage
    earnings_quarter: FinancialStatementsAlphavantage

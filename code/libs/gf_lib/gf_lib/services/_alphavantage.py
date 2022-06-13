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
__all__ = ['get_company_data', 'parse_financial_statements', 'parse_company',
           'parse_earnings_file', 'get_earnings_estimates']

from io import StringIO
import csv
import requests
import orjson
import gf_lib.model as model
from gf_lib.errors import RequestFailedError, ApiFailedError


def parse_company(value: str) -> model.CompanyAlphavantage:
    data = orjson.loads(value)

    try:
        ticker = data['Symbol']
    except KeyError:
        raise ApiFailedError('API calls exceeded')

    name = data['Name']
    description = data['Description']
    exchange = data['Exchange']
    currency = data['Currency']
    country = data['Country']
    address = data['Address']
    fiscal_year_end = data['FiscalYearEnd']
    last_quarter = data['LatestQuarter']

    company = model.CompanyAlphavantage(ticker, name, description, exchange, currency, country, address,
                                        fiscal_year_end, last_quarter)

    return company


def parse_financial_statements(value: str,
        annual_tag: str = 'annualReports', quarter_tag: str = 'quarterlyReports') -> (model.FinancialItemAlphavantage,
                                                                                      model.FinancialItemAlphavantage):
    data = orjson.loads(value)

    try:
        ticker = data['symbol']
    except KeyError:
        raise ApiFailedError('API calls exceeded')

    annual_statements = model.FinancialStatementsAlphavantage(ticker)
    quarter_statements = model.FinancialStatementsAlphavantage(ticker)

    annuals = data[annual_tag]
    quarters = data[quarter_tag]

    for index, statement in enumerate(annuals):
        if index > 4:
            break

        for key, value in statement.items():
            if key not in annual_statements.items:
                annual_statements.items[key] = model.FinancialItemAlphavantage(key)

            match index:
                case 0:
                    annual_statements.items[key].column_1 = value
                case 1:
                    annual_statements.items[key].column_2 = value
                case 2:
                    annual_statements.items[key].column_3 = value
                case 3:
                    annual_statements.items[key].column_4 = value
                case 4:
                    annual_statements.items[key].column_5 = value

    for index, statement in enumerate(quarters):
        if index > 2:
            break

        for key, value in statement.items():
            if key not in quarter_statements.items:
                quarter_statements.items[key] = model.FinancialItemAlphavantage(key)

            match index:
                case 0:
                    quarter_statements.items[key].column_1 = value
                case 1:
                    quarter_statements.items[key].column_2 = value
                case 2:
                    quarter_statements.items[key].column_3 = value

    return annual_statements, quarter_statements


def _get_alphavantage_data(function: str, ticker: str, key: str) -> str:
    url = f"https://www.alphavantage.co/query?function={function}&symbol={ticker}&apikey={key}"

    response = requests.get(url)

    if response.status_code != 200:
        raise RequestFailedError(url, response.status_code)

    return response.text


def get_company_data(ticker: str, key: str) -> model.AlphavantageData:
    data = _get_alphavantage_data('OVERVIEW', ticker, key)
    cpy = parse_company(data)

    data = _get_alphavantage_data('INCOME_STATEMENT', ticker, key)
    inc_stmts_a, inc_stmts_q = parse_financial_statements(data)

    data = _get_alphavantage_data('BALANCE_SHEET', ticker, key)
    bs_stmts_a, bs_stmts_b = parse_financial_statements(data)

    data = _get_alphavantage_data('CASH_FLOW', ticker, key)
    cf_stmts_a, cf_stmts_q = parse_financial_statements(data)

    data = _get_alphavantage_data('EARNINGS', ticker, key)
    earnings_a, earnings_b = parse_financial_statements(data, annual_tag='annualEarnings',
                                                        quarter_tag='quarterlyEarnings')

    return model.AlphavantageData(cpy, inc_stmts_a, inc_stmts_q, bs_stmts_a, bs_stmts_b, cf_stmts_a,
                                  cf_stmts_q, earnings_a, earnings_b)


def parse_earnings_file(data: str) -> list[model.EarningsAlphavantage]:
    source = StringIO(data)
    reader = csv.reader(source, delimiter=',')
    next(reader)

    earnings: list[model.EarningsAlphavantage] = list()

    for row in reader:
        earnings.append(model.EarningsAlphavantage(row[0], row[1], row[2], row[3], row[4], row[5]))

    if not earnings:
        ApiFailedError('API calls exceeded')

    return earnings


def get_earnings_estimates(key: str) -> list[model.EarningsAlphavantage]:
    url = f"https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&apikey={key}"
    response = requests.get(url)

    if response.status_code != 200:
        raise RequestFailedError(url, response.status_code)

    return parse_earnings_file(response.text)

# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2017. 11. 16.
"""
import os

from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from sqlalchemy.exc import SQLAlchemyError
import traceback
from sqlalchemy import types

database = 'highvol'
aws_endpoint = 'findb.cay7taoqqrm6.ap-northeast-2.rds.amazonaws.com'
aws_user = 'highvol'
aws_password = 'FE538'
aws_engine = create_engine(
    'mysql+mysqlconnector://{}:{}@{}/{}'.format(aws_user, aws_password, aws_endpoint, database),
    encoding='utf-8', pool_recycle=1, pool_size=2 * (os.cpu_count() or 1))


def get_connection():
    """
    Get connection of db.

    :return Connection:
    """
    return aws_engine.connect()


def get_stock_master():
    """
    Get stock masters from MySQL and return them.

    :return stock_masters: (DataFrame)
        index       code        | (string) 6 digit number string code of stock.
        columns     name        | (string) The name of company.
    """
    schema_name = 'highvol_stock_master'
    select_sql = "SELECT * FROM {}".format(schema_name)
    stock_masters = pd.DataFrame()
    connection = get_connection()

    try:
        # get all stock codes from the db.
        stock_masters = pd.read_sql(select_sql, connection)
        stock_masters.set_index('code', inplace=True)

    except SQLAlchemyError or EnvironmentError:
        traceback.print_exc()

    finally:
        connection.close()

    return stock_masters


def get_stock_price(codes):
    """
    Get all stock prices from MySQL and return them.

    :param codes: (list of string)
        6 digit number string code of stock. If code is None, select all stock codes.

    :return stock_prices: (DataFrame)
        index       date                    | (datetime)
                    code                    | (string) 6 digit number string code of stock.
        columns     market_capitalization   | (int) The market capitalization of the date.
                    listed_stocks_number    | (int) The number of stocks of the company.
                    adj_close               | (float) market_capitalization / listed_stocks_number
    """
    # If codes is not a list, raise TypeError.
    if type(codes) is not list and type(codes) is not np.ndarray:
        raise TypeError("codes should be a list or numpy.ndarray.")

    # If codes has no element, raise ValueError.
    if len(codes) == 0:
        raise ValueError("codes has at least one element.")

    schema_name = 'highvol_stock_price'
    select_sql = "SELECT `date`, `code`, `market_capitalization`, `listed_stocks_number` FROM {}".format(schema_name)
    stock_prices = pd.DataFrame()
    connection = get_connection()

    # WHERE clause
    if len(codes) is 1:
        select_sql += " WHERE `code` = '{}'".format(codes[0])
    else:
        select_sql += " WHERE `code` in {}".format("('" + "', '".join(str(code) for code in codes) + "')")

    try:
        # get all stock codes from the db.
        stock_prices = pd.read_sql(select_sql, connection, parse_dates=['date'])
        stock_prices['adj_close'] = stock_prices['market_capitalization'] / stock_prices['listed_stocks_number']
        stock_prices.set_index(['date', 'code'], inplace=True)

    except SQLAlchemyError or EnvironmentError:
        traceback.print_exc()

    finally:
        connection.close()

    return stock_prices


def get_highest_volatility(window, stock_masters=None):
    """
    Get the highest volatility by standard deviation of window days.

    :param window: (int) The size of a rolling window.
    :param stock_masters: (DataFrame)
        index       code        | (string) 6 digit number string code of stock.
        columns     name        | (string) The name of company.

    :return: highest_volatilities: (DataFrame)
        index       code                        | (string) 6 digit number string code of stock.
        columns     highest_volatility_{window} | (float) The highest volatility by standard deviation of window days.
    """
    # If window is not bigger than 2, raise ValueError.
    if window <= 2:
        raise ValueError("window should be bigger than 2, but {}.".format(window))

    if stock_masters is None:
        stock_masters = get_stock_master()

    volatility_column_name = 'highest_volatility_{}'.format(window)
    schema_name = 'highvol_' + volatility_column_name
    select_sql = "SELECT * FROM {}".format(schema_name)
    highest_volatilities = pd.DataFrame(columns=[volatility_column_name])
    connection = get_connection()

    try:
        # If the table does not exist, create the table.
        connection.execute("""
            CREATE TABLE IF NOT EXISTS `{}` (
                code VARCHAR(16) NOT NULL PRIMARY KEY,
                {} DOUBLE NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """.format(schema_name, volatility_column_name))

        # get all stock codes from the db.
        highest_volatilities = pd.read_sql(select_sql, connection)
        highest_volatilities.set_index('code', inplace=True)

        if highest_volatilities.empty:
            highest_volatilities.index.name = 'code'
            for code, name in stock_masters.iterrows():
                stock_prices = get_stock_price([code])
                first_price = stock_prices.iloc[0]['adj_close']
                stock_prices['profit_rate'] = stock_prices['adj_close'] / first_price

                # If window is bigger than the length of stock_price, the window is meaningless.
                assert window < len(stock_prices)

                highest_volatility = max(stock_prices['profit_rate'].rolling(window=window).std().dropna())
                highest_volatilities.loc[code] = [highest_volatility]

            highest_volatilities.to_sql(schema_name, connection, if_exists='append', dtype={'code': types.VARCHAR(16)})

    except SQLAlchemyError or EnvironmentError:
        traceback.print_exc()

    finally:
        connection.close()

    return highest_volatilities


def get_market_capitalization_sum(selected_stock_masters):
    """
    Get market capitalization of selected stocks and total stocks,
    and the portion of market capitalization of selected stocks.

    :param selected_stock_masters: (DataFrame) the stock master of selected companies.
        index       code        | (string) 6 digit number string code of stock.
        columns     name        | (string) The name of company.

    :return market_capitalization_sum: (DataFrame)
        index       date            | (datetime)
        columns     selected_sum    | (int) The market capitalization of selected companies.
                    total_sum       | (int) The market capitalization of all companies.
                    portion         | (float) selected_sum / total_sum
    """
    schema_name = 'highvol_market_capitalization'
    select_sql = "SELECT `date`, `market_capitalization` AS `total_sum` FROM {}".format(schema_name)
    market_capitalization_sum = pd.DataFrame()
    connection = get_connection()

    try:
        # Get the market capitalization of all companies.
        total_sum = pd.read_sql(select_sql, connection, parse_dates=['date'])
        total_sum = total_sum.set_index('date')

        # Get the market capitalization of selected companies.
        selected_codes = selected_stock_masters.index.values
        selected_stock_prices = get_stock_price(selected_codes)
        selected_sum = pd.DataFrame(selected_stock_prices.groupby(level=0)['market_capitalization'].sum())
        selected_sum.columns = ['selected_sum']

        # If the length of two sum is not equal, there could be some error. So raise ValueError.
        if len(total_sum) != len(selected_sum):
            raise ValueError("total_sum and selected_sum should have same number of element, " +
                             "but total_sum has {} and selected_sum has {}.".format(len(total_sum), len(selected_sum)))

        market_capitalization_sum = pd.concat([selected_sum, total_sum], axis=1, join='inner')
        market_capitalization_sum['portion'] = \
            market_capitalization_sum['selected_sum'] / market_capitalization_sum['total_sum']

    except SQLAlchemyError or EnvironmentError:
        traceback.print_exc()

    finally:
        connection.close()

    return market_capitalization_sum


if __name__ == '__main__':
    # Save highest volatility data for preparing future.
    print('{} is started...'.format('get_highest_volatility'))
    stock_masters = get_stock_master()
    for window in range(5, 100):
        highest_volatilities = get_highest_volatility(window=window, stock_masters=stock_masters)
        print(highest_volatilities.head())
    print('{} is done!!'.format('get_highest_volatility'))

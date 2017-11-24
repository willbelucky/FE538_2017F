# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2017. 11. 23.
"""
import os

from sqlalchemy import create_engine

database = 'highvol'
aws_endpoint = 'findb.cay7taoqqrm6.ap-northeast-2.rds.amazonaws.com'
aws_user = 'highvol'
aws_password = 'FE538'
aws_engine = create_engine(
    'mysql+mysqlconnector://{}:{}@{}/{}'.format(aws_user, aws_password, aws_endpoint, database),
    encoding='utf-8', pool_recycle=1, pool_size=4 * (os.cpu_count() or 1))


def get_connection():
    """
    Get connection of db.

    :return Connection:
    """
    return aws_engine.connect()

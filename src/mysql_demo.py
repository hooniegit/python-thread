# multiprocessing
# https://docs.python.org/ko/3.7/library/multiprocessing.html

from multiprocessing import Pool
from logmaker import logmaker
from configparser import ConfigParser
from datetime import datetime

from mysql import connector
import MySQLdb


parser = ConfigParser()
config_dir = '/Users/kimdohoon/git/hooniegit/python-thread-pool/config/config.ini'
parser.read(config_dir)

MYSQL_HOST = parser.get('MYSQL', 'MYSQL_HOST')
MYSQL_PWD = parser.get('MYSQL', 'MYSQL_PWD')
MYSQL_PORT = parser.get('MYSQL', 'MYSQL_PORT')
MYSQL_USER = parser.get('MYSQL', 'MYSQL_USER')
MYSQL_DB = parser.get('MYSQL', 'MYSQL_DB')


def mysql_connector():
    conn = connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PWD,
        database=MYSQL_DB
    )

    return conn

log_dir = '/Users/kimdohoon/git/hooniegit/python-thread-pool/ipynb/log'
logger = logmaker.LogMakerTxt(log_dir)


def function(value):

    conn = mysql_connector()
    cursor = conn.cursor()
    QUERY = f"""
    insert into test(data)
    values ('{value}')
    """
    cursor.execute(QUERY)
    conn.commit()

# check connecton status
# SHOW VARIABLES LIKE '%max_connection%';

# MAX_CONNECTION 수를 늘릴 필요성이 있다!

def thread_function(value_list):
    with Pool(150) as p:
        p.map(function, value_list)

value_list = [
    "Hello, World!",
    "Nice to meet you",
    "Have a good time",
    "My name is Hooniegit",
    "Land over time"
]

thread_function(value_list)
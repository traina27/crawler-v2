import configparser
import mysql.connector
from mysql.connector import Error

CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')

HOST = CONFIG['mysqlDB']['host']
DATABASE = CONFIG['mysqlDB']['db']
USER = CONFIG['mysqlDB']['user']
PASSWORD = CONFIG['mysqlDB']['pass']

def connect():
    try:
        CONNECTION = mysql.connector.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        print('Connected to MySQL server version ', CONNECTION.get_server_info())
        return CONNECTION

    except Error as e:
        print('Error while connecting to MySQL ', e)
        return False


def checkExit(cursor, table):
    try:
        cursor.execute("")
    except:
        return true

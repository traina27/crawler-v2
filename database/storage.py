import configparser
import mysql.connector
import database.handles.table as table
import database.handles.create as create
from mysql.connector import Error
import coloredlogs, logging

coloredlogs.install()

CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')

HOST = CONFIG['mysqlDB']['host']
DATABASE = CONFIG['mysqlDB']['db']
USER = CONFIG['mysqlDB']['user']
PASSWORD = CONFIG['mysqlDB']['pass']
# Name Table
TB_SITES = CONFIG['mysqlDB']['tb_sites']
TB_CATEGORY = CONFIG['mysqlDB']['tb_categories']
TB_EBOOKS = CONFIG['mysqlDB']['tb_ebooks']
TB_INFO_EBOOKS = CONFIG['mysqlDB']['tb_info_ebooks']
TB_CHAPTER = CONFIG['mysqlDB']['tb_chapters']
TB_CONTENTS = CONFIG['mysqlDB']['tb_contents']

def connect():
    try:
        CONNECTION = mysql.connector.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        logging.info('Connected to MySQL server version {0}'.format(CONNECTION.get_server_info()))

        # Check exists Table
        dbCursor = CONNECTION.cursor()

        _tb_sites = table.checkExists(dbCursor, TB_SITES)
        if _tb_sites == False:
            create.table(dbCursor, TB_SITES)

        _tb_category = table.checkExists(dbCursor, TB_CATEGORY)
        if _tb_category == False:
            create.table(dbCursor, TB_CATEGORY)

        _tb_ebooks = table.checkExists(dbCursor, TB_EBOOKS)
        if _tb_ebooks == False:
            create.table(dbCursor, TB_EBOOKS)

        _tb_ebooks = table.checkExists(dbCursor, TB_INFO_EBOOKS)
        if _tb_ebooks == False:
            create.table(dbCursor, TB_INFO_EBOOKS)

        _tb_chapters = table.checkExists(dbCursor, TB_CHAPTER)
        if _tb_chapters == False:
            create.table(dbCursor, TB_CHAPTER)

        _tb_contents = table.checkExists(dbCursor, TB_CONTENTS)
        if _tb_contents == False:
            create.table(dbCursor, TB_CONTENTS)


        return CONNECTION

    except Error as e:
        logging.error('Error while connecting to MySQL {0}'.format(e))
        return False


def checkExit(cursor, table):
    try:
        cursor.execute("")
    except:
        return true

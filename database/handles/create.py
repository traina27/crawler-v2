import database.storage as storage
from mysql.connector import Error
import coloredlogs, logging

coloredlogs.install()

def insertCategory(name, url, site_id):
    try:
        db = storage.connect()
        dbCur = db.cursor()

        insertQuery = """INSERT INTO categories (name, url, site_id) VALUES ('{0}', '{1}', {2}) """.format(name, url, site_id)

        dbCur.execute(insertQuery)
        db.commit()

        dbCur.close()
    except Error as e:
        logging.error('Error: Insert categories {}'.format(e))


def insertEbook(category_id, url):
    try:
        db = storage.connect()
        dbCur = db.cursor()

        insertQuery = """INSERT INTO ebooks (category_id, url) VALUES ('{0}', '{1}') """.format(category_id, url)

        dbCur.execute(insertQuery)
        db.commit()

        dbCur.close()
    except Error as e:
        logging.error('Error: Insert ebook {}'.format(e))

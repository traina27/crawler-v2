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

def insertChapter(name, url, ebook_id):
    try:
        db = storage.connect()
        dbCur = db.cursor()

        insertQuery = """INSERT INTO chapters (name, url, ebook_id) VALUES ('{0}', '{1}', {2}) """.format(name, url, ebook_id)

        dbCur.execute(insertQuery)
        db.commit()

        dbCur.close()
    except Error as e:
        logging.error('Error: Insert chapter {}'.format(e))

def insertInfoBook(ebook_id, url, name, description, author):
    try:
        db = storage.connect()
        dbCur = db.cursor()

        insertQuery = """INSERT INTO info_ebooks (ebook_id, url, name, description, author) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}') """.format(ebook_id, url, name, description, author)

        dbCur.execute(insertQuery)
        db.commit()

        dbCur.close()
    except Error as e:
        logging.error('Error: Insert info book {}'.format(e))

def insertContent(chapter_id, content):
    try:
        db = storage.connect()
        dbCur = db.cursor()

        insertQuery = """INSERT INTO contents (chapter_id, contents) VALUES ({0}, '{1}') """.format(chapter_id, content)

        dbCur.execute(insertQuery)
        db.commit()

        dbCur.close()
    except Error as e:
        logging.error('Error: Insert content {}'.format(e))

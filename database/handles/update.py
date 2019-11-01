import database.storage as storage
from mysql.connector import Error
import coloredlogs, logging

coloredlogs.install()

def updateInfoEbook(key, value, id):
    try:
        db = storage.connect()
        dbCur = db.cursor()

        updateQuery = """UPDATE info_ebooks SET {0}='{1}' WHERE id={2}""".format(key, value, id)

        dbCur.execute(updateQuery)
        db.commit()

        dbCur.close()
    except Error as e:
        logging.error('Error: Update Info Ebook {}'.format(e))


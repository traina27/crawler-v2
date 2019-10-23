import coloredlogs, logging
import database.storage as storage

coloredlogs.install()

def all(tableName):
    try:
        db = storage.connect()
        dbCur = db.cursor()
        dbCur.execute("SELECT * FROM {0}".format(tableName))
        result = dbCur.fetchall()
        dbCur.close()
        return result
    except Exception as e:
        logging.error('Error: Select all {0}'.format(e))

def _one(field,value, key, tableName):
    try:
        db = storage.connect()
        dbCur = db.cursor()
        querySql = """SELECT {0} FROM {2} WHERE {1}='{3}' """.format(field, key, tableName, value)
        dbCur.execute(querySql)
        result = dbCur.fetchone()
        dbCur.close()
        return False if result is None else result[0]
    except Exception as e:
        logging.error('Error: select one {}', e)

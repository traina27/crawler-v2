import coloredlogs, logging

coloredlogs.install()

def all(dbCur, tableName):
    try:
        dbCur.execute("SELECT * FROM {0}".format(tableName)
        result = dbCur.fetchall()
        return result
    except Exception as e:
        logging.error('Error: Select all {0}'.format(e))

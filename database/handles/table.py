import coloredlogs, logging

coloredlogs.install()

def checkExists(dbCur, tableName):
    try:
        dbCur.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_name = '{0}'
                """.format(tableName.replace('\'', '\'\'')))
        if dbCur.fetchone()[0] == 1:
            return True
        return False
    except Exception as e:
        logging.error('Error: Check Exists tableName {0}'.format(e))
        return False

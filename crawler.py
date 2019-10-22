import database.storage as storage
import coloredlogs, logging
import src.spider as spider

coloredlogs.install()

class crawler:
    CONNECT = storage.connect()
    if CONNECT == False:
        logging.error('Enable to connect mysql host')
        exit()

    spider.BrickSetSpider()

import database.storage as storage
import coloredlogs, logging
# import src.categories as categories
# import src.ebooks as ebooks
import src.info_ebooks as info_ebooks

coloredlogs.install()

class crawler:
    CONNECT = storage.connect(True)
    if CONNECT == False:
        logging.error('Enable to connect mysql host')
        exit()

    CONNECT.cursor().close()
#     categories.spider()
#     ebooks.spider()
    info_ebooks.spider()

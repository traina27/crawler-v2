import coloredlogs, logging

coloredlogs.install()

__TABLE = {
    'sites': """CREATE TABLE {0} (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255),
       url VARCHAR(255),
       created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
       updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )""",
    'categories': """CREATE TABLE {0} (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255),
       url VARCHAR(255),
       site_id INT,
       created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
       updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )""",
    'ebooks': """CREATE TABLE {0} (
       id INT AUTO_INCREMENT PRIMARY KEY,
       category_id INT,
       url VARCHAR(255),
       created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
       updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )""",
    'info_ebooks': """CREATE TABLE {0} (
       id INT AUTO_INCREMENT PRIMARY KEY,
       ebook_id INT,
       name VARCHAR(255),
       description LONGTEXT,
       author VARCHAR(255),
       url_read_online VARCHAR(255),
       url_dw_epub VARCHAR(255),
       url_dw_mobi VARCHAR(255),
       url_dw_pdf VARCHAR(255),
       created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
       updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )""",
    'chapters': """CREATE TABLE {0} (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255),
       ebook_id INT,
       order_chapter INT,
       created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
       updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )""",
    'contents': """CREATE TABLE {0} (
       id INT AUTO_INCREMENT PRIMARY KEY,
       chapter_id INT,
       contents LONGTEXT,
       created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
       updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )"""
}

def table(dbCur, tableName):
    try:
        dbCur.execute(__TABLE[tableName].format(tableName))
    except Exception as e:
        logging.error('Error: create table Sites {0}'.format(e))

def mysql_connector():
    from configparser import ConfigParser
    from mysql import connector
    import MySQLdb

    parser = ConfigParser()
    config_dir = 'hooniegit/python-thread-pool/config/config.ini'
    parser.read(config_dir)

    MYSQL_HOST = parser.get('MYSQL', 'MYSQL_HOST')
    MYSQL_PWD = parser.get('MYSQL', 'MYSQL_PWD')
    MYSQL_PORT = parser.get('MYSQL', 'MYSQL_PORT')
    MYSQL_USER = parser.get('MYSQL', 'MYSQL_USER')
    MYSQL_DB = parser.get('MYSQL', 'MYSQL_DB')

    conn = connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PWD,
        database=MYSQL_DB
    )
    return conn

if __name__ == '__main__':
    conn = mysql_connector()
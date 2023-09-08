import sys
sys.path.append("/home/hooniegit/git/personal/python-thread-pool/lib")

from mysql_lib import *
from spotify_lib import *
from datetime import datetime, timedelta
from threading import Thread
from mysql.connector.pooling import MySQLConnectionPool


#
def make_movieList(conn, start_date, end_date):
    cursor = conn.cursor()

    QUERY = f"SELECT * from movie where date_gte>'{start_date}' and date_gte<'{end_date}' "
    cursor.execute(QUERY)
    movie_list = cursor.fetchall()
    return movie_list

#
if __name__ == "__main__":
    conn = mysql_connector()

    movie_dump = []
    for i in range(19):
        movie_list = make_movieList(conn, f'{i*5+1960}-01-01', f'{(i+1)*5+1960}-01-01')
        movie_dump.append(movie_list)

    f

    # token = make_accessToken()






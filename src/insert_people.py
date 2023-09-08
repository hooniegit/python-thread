import sys
sys.path.append("/Users/kimdohoon/git/hooniegit/python-thread-pool/lib")

from mysql_lib import *
from tmdb_lib import *

from datetime import datetime, timedelta
from multiprocessing import Pool
from logmaker import logmaker

def make_list(KEY, date, dump):
    conn = mysql_connector()
    people_list = make_peopleList(KEY, conn, date)
    
    # 전달된 dump 리스트에 데이터를 추가
    dump.extend(people_list)
    
    print("Job Finished for", date)
    conn.close()

def threadjob(KEY, date_list, dump):
    with Pool(150) as pool:
        pool.starmap(make_list, [(KEY, date, dump) for date in date_list])
    
    print("All jobs finished")
    print(dump)


if __name__ == '__main__':

    KEY = get_keys()
    dump = []

    date_list = []
    start_date_str = "1987-05-15"
    date_list.append(start_date_str)
    date = datetime.strptime(start_date_str, "%Y-%m-%d")

    for count in range(1, 2):
        date = date + timedelta(days=7)
        date_str = date.strftime("%Y-%m-%d")
        date_list.append(date_str)

    log_dir = "/Users/kimdohoon/git/hooniegit/python-thread-pool/src/logs"
    logger = logmaker.LogMakerTxt(log_dir=log_dir)

    logger.LogFunction(threadjob(KEY, date_list, dump))
    

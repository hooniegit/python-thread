# start_date ~ end_date 기간의 date list 생성
def make_dateList(start_date, end_date, period):
    from datetime import datetime, timedelta

    date_list = []
    date_list.append(start_date)
    now_date = datetime.strptime(start_date, "%Y-%m-%d")

    while True:
        now_date += timedelta(days=period)
        now_date_str = now_date.strftime("%Y-%m-%d")
        date_list.append(now_date_str)

        if now_date_str == end_date:
            break
    
    return date_list


# 해당 date에 대한 people list 생성
def make_people_list(date):
    from configparser import ConfigParser
    from mysql import connector

    # config.ini 읽기
    parser = ConfigParser()
    parser.read("config/config.ini")

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
    cursor = conn.cursor()

    QUERY = f"""SELECT people_id from people
                WHERE date_gte = '{date}'"""
    cursor.execute(QUERY)
    rows = cursor.fetchall()
    conn.close()

    people_list = []
    for row in rows:
        people_id = row[0]
        people_list.append(people_id)

    return people_list


# 해당 date에 대한 
def load_json(tmdb_key, date, people_list):
    import requests, json, time

    for people_id in people_list:
        base_url = f"https://api.themoviedb.org/3/person/{people_id}"
        headers = {
            "Authorization": f"Bearer {tmdb_key}",
            "accept": "application/json"
        }
        response = requests.get(base_url, headers=headers)

        if response.status_code == 200:
            json_data = response.json()
            try:
                dir = f"/home/hooniegit/datas/people/TMDB_peopleDetails_{people_id}_{date}.json"
                with open (dir, "w", encoding="utf-8") as file:
                    json.dump(json_data, file, indent=4, ensure_ascii=False)
            except Exception as e:
                print(e)
        else:
            print(f"ERROR : {date}, {people_id}")
            dir = f"/home/hooniegit/ERROR/people/{date}"
            with open (dir, "w", encoding="utf-8") as file:
                pass
        time.sleep(1)



def thread_single():
    print(f"START THREAD : {} >>>>>>>>>>")


    print(f"FINISH THREAD : {} <<<<<<<<<<")

def thread_all(KEY, date_list):
    from threading import Thread

    threads = []
    for date in date_list:
        thread = Thread(target=thread_job, args=(KEY, date))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()


# need to do until 64
if __name__ == "__main__":

    # start_date_str = "2000-01-"
    # start_date_str = "2005-01-"
    # start_date_str = "2010-01-"
    # start_date_str = "2015-01-"
    # start_date_str = "2020-01-"
    start_date_str = sys.argv[1]
    date_list_base = make_dateList(start_date_str, 273, 14)

    cnt = sys.argv[2]
    KEY = get_keys(cnt)

    for date in date_list_base:
        date_list = make_dateList(date, 7, 39)

        thread_all(KEY, date_list)

import mysql.connector, configparser, requests
from datetime import datetime, timedelta

# get_keys()
def get_keys():
    from configparser import ConfigParser

    parser = ConfigParser()
    parser.read('hooniegit/python-thread-pool/config/config.ini')
    KEY = parser.get("TMDB", "API_KEY")

    return KEY
    
# make_peopleList(key, conn, 'YYYY-mm-dd')
def make_peopleList(key, conn, date_gte):
    cursor = conn.cursor()

    QUERY = f"""SELECT movie_id from movie
                WHERE date_gte = '{date_gte}'"""
    cursor.execute(QUERY)
    rows = cursor.fetchall()

    unique_ids = set()
    people_list = []
    
    for row in rows:
        movie_id = row[0]
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {key}"
        }
        response = requests.get(url, headers=headers).json()

        try : cast = response["cast"]
        except : cast = []
        try : crew = response["crew"]
        except : crew = []
        people = crew + cast

        for item in people:
            id_value = item.get("id")
            if id_value not in unique_ids:
                people_list.append(item)
                unique_ids.add(id_value)
        
    return people_list

# insert_people(conn, people_list, 'YYYY-mm-dd)
def insert_people(conn, people_list, date_gte):
    cursor = conn.cursor

    for person in people_list:
        id = person["id"]
        original_name = person["original_name"]

        QUERY = "INSERT IGNORE INTO people(people_id, people_nm, date_gte) VALUES (%s, %s, %s)"
        values = (id, original_name, date_gte)
        cursor.execute(QUERY, values)
        conn.commit()
        conn.close

        print(f"DONE : {date_gte}")
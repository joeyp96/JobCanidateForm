import requests
import sqlite3
import json

def database():
    try:
        db_connection = sqlite3.connect('meteorite_db.db')
        cursor = db_connection.cursor()
        query_create_met_data="""CREATE TABLE IF NOT EXISTS meteorite_data(
                                 name TEXT,
                                 id INTEGER,
                                 nametype TEXT,
                                 recclass TEXT,
                                 mass TEXT,
                                 fall TEXT,
                                 year TEXT,
                                 reclat TEXT,
                                 reclong TEXT,
                                 geolocation TEXT,
                                 states TEXT,
                                 countries TEXT);"""
        cursor.execute(query_create_met_data)
        results = cursor.fetchall()

        query_delete=""""DELETE FROM meteorite_data"""
        cursor.execute(query_delete)
    except sqlite3.Error as db_error:
        print(f'A database error: {db_error}')
    finally:
        if db_connection:
            db_connection.close()

def call_api():
    url = "https://data.nasa.gov/resource/gh4g-9sfh.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(data)
        print(type(data))
        print(data[2])
        print(data[2]['mass'])
        return data


if __name__ == '__main__':
  meteorite_list=call_api()
  database()

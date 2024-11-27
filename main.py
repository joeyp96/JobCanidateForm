import requests

from requests.auth import HTTPBasicAuth
import sqlite3
import json


def database():
    # try:
    #     db_connection = sqlite3.connect('candidate.db')
    #     cursor = db_connection.cursor()
    #     query_create_can_data = """CREATE TABLE IF NOT EXISTS can_data(
    #                              name TEXT,
    #                              email TEXT,
    #                              DOB TEXT,
    #                              phone TEXT,
    #                              field TEXT,
    #                              graduate TEXT,
    #                              years TEXT,
    #                              website TEXT,
    #                              ;"""
    #     cursor.execute(query_create_can_data)
    #     results = cursor.fetchall()
    #
    #     query_delete = """"DELETE FROM can_data"""
    #     cursor.execute(query_delete)
    # except sqlite3.Error as db_error:
    #     print(f'A database error: {db_error}')
    # finally:
    #     if db_connection:
    #         db_connection.close()

    with open('secret.txt', 'r') as file:
        api_key = file.read().strip()
    candidate_list = call_api(api_key)
    return candidate_list

def call_api(api_key):
    url = 'https://joeyp96.wufoo.com/forms/employee-complaint-form/entries/json'
    response = requests.get(url, auth=HTTPBasicAuth(api_key, 'pass'))
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        print(data)
        print(type(data))
        print(data[2])
        print(data[2]['mass'])
        return data


if __name__ == '__main__':
    data = database()


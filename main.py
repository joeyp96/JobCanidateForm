import sqlite3
import requests
from requests.auth import HTTPBasicAuth


def call_api():
    url = 'https://joeyp96.wufoo.com/api/v3/forms/employee-complaint-form/entries.json'

    with open('secret.txt', 'r') as file:
        api_key = file.read().strip()

    response = requests.get(url, auth=HTTPBasicAuth(api_key, 'pass'))

    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        print("API Connection Successful")
        data = response.json()
        return data.get('Entries', [])  # Return the list of entries
    elif response.status_code == 404:
        print("Error 404")
    else:
        print(f"Error: Received status code {response.status_code}")
    return []


def create_database():
    # connecting to database
    conn = sqlite3.connect("candidates.db")
    cursor = conn.cursor()

    # creating table with Wufoo fields
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            date_of_birth TEXT,
            phone_number TEXT,
            desired_field_of_work TEXT,
            years_of_experience INTEGER,
            website TEXT,
            college_graduate TEXT
        )
    ''')
    conn.commit()
    return conn

    # populating table with the data submitted on the forms
def filter_and_insert_data(entries, conn):
    cursor = conn.cursor()

    for entry in entries:
        # mapping the fields from the terminal to the required format
        candidate_data = (
            entry.get('Field1'),  # candidate name
            entry.get('Field24'),  # email
            entry.get('Field7'),  # dob
            entry.get('Field5'),  # phone
            entry.get('Field2'),  # field of work
            int(entry.get('Field23', 0)), # years of experience
            entry.get('Field31'),  # website
            entry.get('Field3')  # college graduate (y/n)
        )

        # inserting filtered data into the database
        cursor.execute('''
            INSERT INTO candidates (
                name, email, date_of_birth, phone_number,
                desired_field_of_work, years_of_experience,
                website, college_graduate
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', candidate_data)

    conn.commit()


if __name__ == '__main__':
    # fetch data from API
    entries = call_api()

    if entries:
        # create the database and table by calling function
        conn = create_database()

        # filter and insert data by calling function
        filter_and_insert_data(entries, conn)


        conn.close()

        # print statement to verify if db was created successfully
        print("Data successfully inserted into the database.")
    else:
        print("No data to insert.")

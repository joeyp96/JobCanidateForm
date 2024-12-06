import sqlite3
import requests
from requests.auth import HTTPBasicAuth
import PySimpleGUI as sg

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
    cursor.execute("DELETE FROM candidates")
    return conn
    # populating table with the data submitted on the forms

def guiLayout():
    # Creates the layout of the GUI, which creates text boxes to display user data and input our filters, as well as
    # buttons to run our filters or exit the program.
    layout = [
            [sg.Text('Job Candidate Filter')],
            [sg.Multiline(size=(480, 20), key='Candidate Box', disabled=True, horizontal_scroll = True,)],
            [sg.Button('Apply Filter', size=(20, 2)), sg.Button('EXIT', size=(20, 2))],
            [sg.Text('Minimum Years of Experience Required: > '),
         sg.Input(key='min_years_of_experience', size=6)],
        [sg.Text('College Graduate? > '),
         sg.Combo(['Yes', 'No', 'Both'], default_value='Both', key='grad_key'),
         ],
    ]
    # Create the Window
    window = sg.Window('Job Sorter', layout, size=(1280, 720))
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'EXIT':
            break
        if event == 'Apply Filter':
            window['Candidate Box'].update('')
            window['Candidate Box'].print(f"{'name':<40}{'email':<40}{'dob':<40}{'#':<40}{'Field of Work':<40}{'Experience':<40}{'Website':<40}{'College':<40}")
            #Used to clear the output then print a header across the top including candidate attributes.
            can_list = []
            try:
                can_list = fetch_data(int(values["min_years_of_experience"]), values["grad_key"])
            except:
                can_list = fetch_data(0, values["grad_key"])
            for row in can_list:
                id = int(row[0])
                name = row[1]
                email = row[2]
                birth = row[3]
                phone_number = row[4]
                field_of_work = row[5]
                experience = int(row[6])
                website = row[7]
                college = row[8]
                window['Candidate Box'].print(f"{name:<40}{email:<40}{birth:<40}{phone_number:<40}{field_of_work:<40}{experience:<40}{website:<40}{college:<40}")
                # Taking the candidate list that was populated by fetch_data and prints out each attribute with spacing.

def fetch_data(experience_filter, college_filter):
    conn = sqlite3.connect("candidates.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates")
    data = cursor.fetchall()
    formatted_data = []
    for row in data:
        # Grabs data from sqlite database and formats it into a tuple to be stored into a list.
        id = int(row[0])
        name = row[1]
        email = row[2]
        birth = row[3]
        phone_number = row[4]
        field_of_work = row[5]
        experience = int(row[6])
        website = row[7]
        college = row[8]
        if college_filter == 'Both':
            # To allow the college graduate filter to work in both removing the option to filter in this statement.
            if experience >= experience_filter:
                candidate = (id, name, email, birth, phone_number, field_of_work, experience, website, college)
                formatted_data.append(candidate)
        else:
            if experience >= experience_filter and college == college_filter:
                # If college experience filter is set to any option besides 'Both', this statement will choose the filter.
                candidate = (id, name, email, birth, phone_number, field_of_work, experience, website, college)
                formatted_data.append(candidate)
    conn.close()
    return formatted_data


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
            int(entry.get('Field23', 0)),  # years of experience
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
    guiLayout()
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

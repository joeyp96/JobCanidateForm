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
        print(data)  # Print the received JSON data for verification
        return data
    elif response.status_code == 404:
        print("Error 404")
    else:
        print(f"Error: Received status code {response.status_code}")


if __name__ == '__main__':
    call_api()

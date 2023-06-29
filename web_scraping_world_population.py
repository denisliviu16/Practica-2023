import time
import os
import shutil
from bs4 import BeautifulSoup
import requests

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

url = 'https://countrymeters.info/en/World'

while True:

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table')

    rows = table.find_all('tr')

    clear_console()

    for row in rows:
        columns = row.find_all('td')
        if len(columns) >= 2:
            column1 = columns[0].text.strip()
            column2 = columns[1].text.strip()
            print(f"{column1}: {column2}")

    time.sleep(1)

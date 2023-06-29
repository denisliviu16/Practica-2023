import requests
import openpyxl
import pandas as pd
from openpyxl import Workbook
from bs4 import BeautifulSoup
import re

url = 'https://www.visualcapitalist.com/cp/mapped-ukrainian-refugee-destinations/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
}
response = requests.get(url, headers=headers)
content = response.text

soup = BeautifulSoup(content, 'lxml')
tables = soup.find_all('table')
table = tables[0]

rows = table.find_all('tr')

data = []
for row in rows:
    cells = row.find_all('td')
    row_values = [re.sub(r'[^A-Za-z 0-9]', '', cell.text.strip()) for cell in cells]
    data.append(row_values)

df = pd.DataFrame(data, columns=['Country', 'Number'])

df.to_excel('ukrainian_refugee_destinations.xlsx', index=False, engine='openpyxl')

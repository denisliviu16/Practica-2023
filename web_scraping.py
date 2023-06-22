import requests
import openpyxl
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/List_of_European_countries_by_life_expectancy#Life_expectancy_by_country_(World_Bank_Group,_2021)'
response = requests.get(url)
content = response.text

soup = BeautifulSoup(content, 'lxml')
table = soup.find('table', {'class': 'wikitable'})

wb = openpyxl.load_workbook('data.xlsx')
sheet = wb.active

sheet.append(["Country", "Life Expectancy"])

rows = table.find_all('td')


row_data = []

cell_count = 0

for row in rows:
    for cell in row:
        cell_value = cell.text.strip()
        if cell_value != '':
            row_data.append(cell_value)
            cell_count += 1
        
        if cell_count == 13:
            sheet.append(row_data[:2])
            row_data = []
            cell_count = 0
        
        
wb.save('data.xlsx')
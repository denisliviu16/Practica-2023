import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

url = "https://countrymeters.info/en/World"
response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, "html.parser")

selector_div = soup.find("div", id="selector")
values = [option.get("value") for option in selector_div.find_all("option")]

workbook = Workbook()
sheet = workbook.active

for index, value in enumerate(values, start=1):
    if value is not None:
        modified_value = value[4:]
        sheet.cell(row=index, column=1, value=modified_value)
        
workbook.save("countries.xlsx")
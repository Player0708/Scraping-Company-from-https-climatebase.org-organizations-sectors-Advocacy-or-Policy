import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup

# Set up headless Firefox driver
firefox_options = Options()
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()), options=firefox_options)

url = "https://climatebase.org/organizations?sectors=Advocacy+or+Policy"
driver.get(url)
time.sleep(10)
page_source = driver.page_source

# Print or process the page source as needed
# print(page_source)

soup = BeautifulSoup(page_source, 'html.parser')

# Extract the text content of the <span> elements

companies = soup.find_all("a", class_="sc-gvPdwL jXPveZ list_card comp")

# Open CSV file in write mode
with open("companies_data.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write header row
    writer.writerow(["Company", "Location", "Size", "Description"])
    
    for company in companies:
        company_name_elem = company.find("div", class_="list_card__title")
        company_name = company_name_elem.text.strip() if company_name_elem else "Not Available"
        
        location_elem = company.find("div", class_="sc-kbdlSk bDYuio list_card__metadata-item")
        location = location_elem.find("span").text.strip() if location_elem else "Not Available"
        
        size_elem = company.find_all("div", class_="sc-kbdlSk bDYuio list_card__metadata-item")[1]
        size = size_elem.find("span").text.strip() if size_elem else "Not Available"
        
        description_elem = company.find("div", class_="list_card__description")
        description = description_elem.p.text.strip() if description_elem else "Not Available"
        
        # Write data to CSV file
        writer.writerow([company_name, location, size, description])

driver.quit()

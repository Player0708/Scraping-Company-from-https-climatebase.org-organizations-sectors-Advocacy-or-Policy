import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service

# Set up headless Firefox driver
firefox_options = Options()
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()), options=firefox_options)

url = "https://climatebase.org/organizations?sectors=Advocacy+or+Policy"
driver.get(url)
time.sleep(3)

# Function to scroll slowly down the page
# def scroll_slowly():
#     total_height = int(driver.execute_script("return document.body.scrollHeight"))
#     for i in range(0, total_height, 2):
#         driver.execute_script("window.scrollTo(0, {});".format(i))
#         time.sleep(0.1)

# Create lists to store data
company_names = []
sizes = []
locations = []
company_urls = []
descriptions = []

# Find all elements with the specified class name

for i in range(1, 651):
    print(i)
    try:
        xpath = '(//*[@class="sc-iaJaUu dnxWqB list_card__tag"])[' + str(i) + ']'
        # xpath = '(//*[@class="sc-iaJaUu dnxWqB list_card__tag"])[13]'
        button = driver.find_element(By.XPATH, xpath)
        time.sleep(3)
        button.click()
        time.sleep(5)
        
        # Scraping data
        try:
          company_name = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/h1').text
        except:
           company_name=""
           
        # time.sleep(2)
        try:
            size = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/span').text
        except:
            size = ""
        # time.sleep(2)
        try:
          location = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div[3]/div/span').text
        except:
            location=""
        # time.sleep(2)
        try:
          company_url = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[5]/a').get_attribute('href')
        except:
            company_url=""
        # time.sleep(2)
        try:
          description = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div').text
        except:
            description=""
        # time.sleep(2)
        
        # Appending data to lists
        company_names.append(company_name)
        sizes.append(size)
        locations.append(location)
        company_urls.append(company_url)
        descriptions.append(description)
        driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[1]/div[3]/div[1]/div[1]/span/div').click()
        # print(company_names)
        # print(sizes)
        # print(locations)
        # print(company_urls)
        # print(descriptions)

        driver.get(url)
        # scroll_slowly()
        time.sleep(5)
        

    except:
        print("Bad luck")


# Write data to CSV file
with open('climatebase_organizations.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Company Name', 'Size', 'Location', 'Company URL', 'Description']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    
    for i in range(len(company_names)):
        writer.writerow({'Company Name': company_names[i], 'Size': sizes[i], 'Location': locations[i], 'Company URL': company_urls[i], 'Description': descriptions[i]})


# Quit the driver
# driver.quit()

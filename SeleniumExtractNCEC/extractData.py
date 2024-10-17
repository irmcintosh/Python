!apt-get update
!apt-get install -y wget unzip
!wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
!dpkg -i google-chrome-stable_current_amd64.deb || apt-get -f install -y
!pip install selenium
!pip install webdriver-manager
!apt-get install -y xvfb
!pip install pyvirtualdisplay
!pip install beautifulsoup4
!pip install pandas

# Import necessary modules
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
import pandas as pd
import time
from google.colab import drive


display = Display(visible=0, size=(1024, 768))
display.start()

# Set up the Selenium Chrome driver with Chrome binary path
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.binary_location = "/usr/bin/google-chrome"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the target URL
url = "https://outages.ncelectriccooperatives.com/outages/maps"
driver.get(url)

# Wait for the page to load
time.sleep(10)  # Adjust as needed depending on your internet speed

# Extract everything from the div with class "jsCountyDetailsWrapperByAlpha"
try:
    # Wait until the div is present in the DOM
    county_details_wrapper = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'jsCountyDetailsWrapperByAlpha'))
    )

    # Get the HTML content of the div
    county_details_html = county_details_wrapper.get_attribute('innerHTML')

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(county_details_html, 'html.parser')

    # Prepare lists to hold data
    counties = []
    members_affected = []
    utilities = []

    # Extract information from the HTML content
    outage_reports = soup.find_all('dl', class_='outage_report')

    for report in outage_reports:
        # Extract county name
        county_name = report.find('dt').text.strip()

        # Extract number of members affected
        affected_info = report.find('p').text.strip().split('member')[0]

        # Extract the utility information (if available)
        utility_info_list = report.find_all('li')
        utility_info = ", ".join([utility.text.strip().split(':')[0] for utility in utility_info_list])

        # Append data to lists
        counties.append(county_name)
        members_affected.append(affected_info)
        utilities.append(utility_info)

    # Create a DataFrame from the extracted data
    data = {
        'County': counties,
        'Members Affected': members_affected,
        'Utility':utilities,
        'CountyJoin': [c.split('(')[0] for c in counties]
    }
    df = pd.DataFrame(data)

except Exception as e:
    print("An error occurred:", e)

# Clean up
driver.quit()
display.stop()

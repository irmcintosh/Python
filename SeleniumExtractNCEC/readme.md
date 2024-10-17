# NC Electric Outage Scraper

This Python script is designed to scrape power outage information from the North Carolina Electric Cooperatives website using Selenium and BeautifulSoup. The extracted data is stored in a Pandas DataFrame for further analysis.

## Features

- **Headless Chrome Automation**: The script uses Selenium with a headless Chrome browser to navigate the website.
- **HTML Parsing**: BeautifulSoup is employed to parse the page's content.
- **Data Extraction**: The script scrapes county names, number of members affected by outages, and utility provider information.
- **Colab Support**: The script is designed to run on Google Colab with specific configurations for Chrome in a headless mode.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Output](#output)
- [Contributing](#contributing)
- [License](#license)

## Requirements

This script requires the following Python libraries to be installed:

- `selenium`: Used for browser automation and interacting with web pages.
- `webdriver_manager`: Manages and installs the appropriate ChromeDriver.
- `pyvirtualdisplay`: Allows running a virtual display in environments like Colab where no graphical display is available.
- `BeautifulSoup4`: Used for parsing the HTML content.
- `pandas`: For storing and manipulating scraped data.
- `google.colab`: Optional, but useful for mounting Google Drive when running in Google Colab.

You can install the necessary dependencies using pip:

```bash
pip install selenium webdriver-manager pyvirtualdisplay beautifulsoup4 pandas google-colab

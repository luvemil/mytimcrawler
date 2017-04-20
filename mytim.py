import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json

# LOAD ENV VARIABLES
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")

login_link = 'https://auth.tim.it/dcareg/public/login'

# Load and setup Selenium using PhantomJS
driver = webdriver.PhantomJS()
driver.set_window_size(1024,760)
driver.get(login_link)

# Login into MyTIM

username = driver.find_element_by_id("usernameLogin")
password = driver.find_element_by_id("passwordLogin")

username.send_keys(USERNAME)
password.send_keys(PASSWORD)

driver.find_element_by_id("entra").click()

# Setup requests Session to get data from the API

session = requests.Session()

cookies = driver.get_cookies()

for cookie in cookies:
    session.cookies.set(cookie['name'],cookie['value'])

# Define the correct params

with open("request_data.json","r") as f:
  data = json.load(f)

url = "https://www.119selfservice.tim.it/area-clienti-119/rest/dettaglioTraffico/json"

response = session.post(url, data=data)

with open('output.json','w') as f:
  f.write(response.content)

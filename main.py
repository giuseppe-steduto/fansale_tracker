import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import title_contains
from datetime import datetime
import os
from dotenv import load_dotenv


def send_notification(str, chat_id):
    """ Send a Telegram message to a specified user """
    api_token = os.getenv("API_TOKEN")
    # Send message to my chat on Telegram
    requests.get("https://api.telegram.org/bot" + api_token + "/sendMessage?chat_id=" + chat_id + "&text=" + str)


# Configuration part
load_dotenv()   # Load env variables from .env file
minimum_seats = int(os.getenv("MINIMUM_SEATS"))  # The minimum number of seats over which you want to be notified
telegram_chat_id = os.getenv("CHAT_ID")
URL = os.getenv("URL")  # The URL of the event on fansale
opt = Options()
opt.headless = True     # Run the browser in headless mode so that it can be run by a cronjob
browser = webdriver.Firefox(options=opt)
wait = WebDriverWait(browser, 10)

# Emulate the browser and request the page
browser.get(URL)
wait.until(title_contains("I migliori biglietti per"))  # Wait after challenge validation, when page is fully loaded
tickets = browser.find_elements(By.CLASS_NAME, "NumberOfTicketsInOffer")
for t in tickets:
    text = t.get_attribute('innerText')
    if t.is_displayed():
        if int(text) >= minimum_seats:
            send_notification("There are " + text + " seats available!", telegram_chat_id)
browser.close()

# Log the current time just to check later that everything ran correctly
logfile = open("./log.txt", "a")
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
logfile.write(current_time + "\n")
logfile.close()

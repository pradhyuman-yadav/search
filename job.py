from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import datetime
import discord
from dotenv import load_dotenv
import os
from _google_search import DecoderGoogle
from _database_connection import JsonDatabase
from _linkedin import DecoderLinkedin
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

load_dotenv()  # This loads the variables from .env
discord_webook_link = os.getenv("DISCORD_WEBHOOK_TEST")
now = datetime.datetime.now()

# TODO
# 1 - Work on Linkedin Job Posting
# 2 - Introduce GPT Resume compare for specific jobs
# 3 - Try to interpret other job boards as well
##

######### Database Setup
# Initialize the JSON database
# database = os.getenv("DATABASE_NAME")
# db = JsonDatabase(database)
# Setting data
# db.set('post1', {'title': 'Hello World', 'content': 'This is an example post.'})

######### Discord Setup
webhook = discord.SyncWebhook.from_url(discord_webook_link)
today = datetime.date.today()
formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
print("Bot active on {} at {}".format(today, formatted_now))
webhook.send("Bot active on Date: {} at Time: {}".format(today, formatted_now))


######### Chrome Setup
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--start-fullscreen")

# Enable logging
capabilities = DesiredCapabilities.CHROME
capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}  # Capturing all browser logs

# Mock location - latitude, longitude, and accuracy
latitude = 40.712776
longitude = -74.005974
accuracy = 100

# Enable the overriding of geolocation
params = {
    "latitude": latitude,
    "longitude": longitude,
    "accuracy": accuracy
}

# Create a driver with the configured options
service = webdriver.ChromeService()
driver = webdriver.Chrome(service=service, options=chrome_options)
# driver.execute_cdp_cmd("Emulation.setGeolocationOverride", params)
driver.maximize_window()
driver.execute_cdp_cmd("Page.setGeolocationOverride", params)
time.sleep(1)

# google = DecoderGoogle(driver=driver, keyword="remote software engineer site:https://apply.workable.com/*", webhook=webhook)
# google = DecoderGoogle(driver=driver, keyword="instagram", webhook=webhook, database_file=JsonDatabase("database/" + os.getenv("GOOGLE_DATABASE_NAME")))
# google.load()
# google.search()
# webhook.send(driver.current_url)

#Linkedin
webhook.send("Linkedin Page active")
linkedin = DecoderLinkedin(driver=driver, webhook=webhook, database_file=JsonDatabase("database/" + os.getenv("LINKEDIN_DATABASE_NAME")), keyword='Software')
linkedin.load()
# linkedin.search()
# linkedin.getJobsAndLinks()
logs = driver.get_log('browser')

with open('browser_logs.txt', 'w') as file:
    for entry in logs:
        # Each entry is a dictionary. Convert it to a string and write to the file.
        # You can format this as needed; here's a simple example:
        file.write(f"{entry['timestamp']} - {entry['level']} - {entry['message']}\n")

driver.close()

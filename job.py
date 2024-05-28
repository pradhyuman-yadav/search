from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import datetime
import discord
from dotenv import load_dotenv
import os
from google_search import DecoderGoogle
from database_connection import JsonDatabase

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
database = os.getenv("DATABASE_NAME")
db = JsonDatabase(database)
# Setting data
db.set('post1', {'title': 'Hello World', 'content': 'This is an example post.'})

######### Discord Setup
webhook = discord.SyncWebhook.from_url(discord_webook_link)
today = datetime.date.today()
formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
print("Bot active on {} at {}", today, formatted_now)
webhook.send("Bot active on Date: {} at Time: {} using Database: {}".format(today, formatted_now, database))


######### Chrome Setup
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")

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
driver.execute_cdp_cmd("Page.setGeolocationOverride", params)
time.sleep(1)

# google = DecoderGoogle(driver=driver, keyword="remote software engineer site:https://apply.workable.com/*", webhook=webhook)
google = DecoderGoogle(driver=driver, keyword="instagram", webhook=webhook, database_file=db)
google.load()
google.search()
webhook.send(driver.current_url)


driver.close()

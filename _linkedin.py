from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
from urllib.parse import quote


class DecoderLinkedin:
    def __init__(self, driver: webdriver, webhook: str, database_file, keyword='New Grad', location='United States'):
        self.driver:webdriver = driver
        self.keyword = keyword
        self.location = location
        self.webhook = webhook
        self.database = database_file

    def load(self):
        """Go to the Linkedin public job search page"""
        self.driver.get("https://www.linkedin.com/jobs/search?keywords=" + quote(self.keyword) +"&f_TPR=r86400&position=1&pageNum=0")
        time.sleep(2)

    def search(self):
        y=self.driver.find_elements(By.CLASS_NAME, 'results-context-header__job-count')[0].text
        print("Number of jobs searched : "+y)

        #### First time run only
        # last_height = self.driver.execute_script("return document.body.scrollHeight") - 1000
        # self.driver.execute_script(f"""window.scrollTo({{left: 0, top: {last_height}, behavior: 'smooth'}});""")
        
        
        
        for i in range(1,20):
            # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            self.driver.execute_script(f"""window.scrollTo({{left: 0, top: {last_height - 500}, behavior: 'smooth'}});""")
            time.sleep(3)

            # self.driver.execute_script("window.scrollTo({left: 0, top: document.body.scrollHeight, behavior: 'smooth'});")
            
            try:
                x=self.driver.find_element(By.XPATH, "//button[@aria-label='See more jobs']")
                self.driver.execute_script("arguments[0].click();", x)
                time.sleep(3)
            except NoSuchElementException:
                # Handle the case where the button is not found
                print("Button not found, continuing with the rest of the code.")
            finally:
                # This block will execute whether or not the exception was raised
                time.sleep(3)

    def getJobsAndLinks(self):
        ul=self.driver.find_element(By.XPATH, '//ul[@class="jobs-search__results-list"]')
        try:
            list_items = ul.find_elements(By.TAG_NAME, 'li')
            discord_message = ""
            for item in list_items:
                try:
                    anchor = item.find_element(By.XPATH, './/div/a')
                    span = item.find_element(By.XPATH, './/div/a/span')
                    href = anchor.get_attribute('href')
                    text = span.text
                    if self.database.get(href) is None:      
                        print(f'Link: {href}, Text: {text}')
                        self.database.set(f'{href}', {'title': f'{text}', 'link': f'{href}'})

                        if(len(discord_message + f"Text: {text}, HREF: {href}\n")>2000):
                            self.webhook.send(discord_message)
                            discord_message = ""

                        discord_message += f"Text: {text}, HREF: {href}\n"

                except NoSuchElementException:
                    print("Missing element in this item.")
        except NoSuchElementException:
            print("The UL element was not found on the page.")
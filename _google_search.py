from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


class DecoderGoogle:
    def __init__(self, driver, keyword, webhook, database_file):
        self.driver = driver
        self.keyword = keyword
        self.webhook = webhook
        self.database = database_file

    def load(self):
        """Go to the Google home page"""
        self.driver.get("https://www.google.com")

    def search(self):
        search_box = self.driver.find_element(By.NAME, "q")
        # Send the search query to the search box
        search_box.send_keys(self.keyword)

        # Simulate pressing Enter
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        ### Time based search argument for Google = "&tbs=qdr:h" "&tbs=qdr:d"
        #Time based URL modification
        current_url = self.driver.current_url
        print("Current URL: "+current_url)
        time_based_url = current_url+"&tbs=qdr:d"
        print("Modified URL:"+time_based_url)
        self.driver.get(time_based_url)
        time.sleep(2)
        for i in range(1,10):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
        self.send_message()

    def send_message(self):
        h3_elements = self.driver.find_elements(By.TAG_NAME, "h3")
        discord_message = ""

        # Iterate through each <h3> element
        for h3 in h3_elements:
            try:
                # Find the parent <a> tag of each <h3> element
                parent_anchor = h3.find_element(By.XPATH, "./ancestor::a")

                # Get the href attribute from the parent <a> tag
                href = parent_anchor.get_attribute('href')

                # Print the text of the <h3> and the href of the parent <a>
                if self.database.get(href) is None:
                    print(f"Text: {h3.text}, HREF: {href}")
                    self.database.set(f'{href}', {'title': f'{h3.text}', 'link': f'{href}'})

                    if(len(discord_message + f"Text: {h3.text}, HREF: {href}\n")>2000):
                        self.webhook.send(discord_message)
                        discord_message = f"Text: {h3.text}, HREF: {href}"

                    discord_message += f"Text: {h3.text}, HREF: {href}\n"
            except Exception as e:
                print(f"Error finding parent anchor or href for an H3: {str(e)}")
                pass

        self.webhook.send(discord_message)
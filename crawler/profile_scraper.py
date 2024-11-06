from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re
from lxml import etree

class ProfileScraper:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        self.driver.get("https://linkedin.com/login")
        time.sleep(2)
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)

    def scrape_profiles(self, url):
        self.driver.get(url)
        time.sleep(3)
        src = self.driver.page_source
        soup = BeautifulSoup(src, "html.parser")
        dom = etree.HTML(str(soup))
        profile_links = set()
        
        section = dom.xpath('//*[@id="profile-content"]/div/div[2]/div/div/aside/section[2]')
        for element in section:
            links = element.xpath('.//a')
            for link in links:
                href = link.get("href")
                if re.match(r"^https://www.linkedin.com/in/[a-zA-Z0-9-]+", href):
                    profile_links.add(href.split('?')[0])
        
        return list(profile_links)

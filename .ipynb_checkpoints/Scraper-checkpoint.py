import os
import json
import time
from utils import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

class Scraper:

    def __init__(self, mypath):
        self.mypath = mypath

        # selenium
        self.options = Options()
        self.options.add_argument("--start-maximized")
        self.chromedriver_path = os.path.join(self.mypath, 'SeleniumDrivers', 'chromedriver.exe')
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe" # route to chrome exe path
        self.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        self.options.add_argument(f'user-agent={self.userAgent}')
        self.browser = webdriver.Chrome(options=self.options, executable_path=self.chromedriver_path)
        self.delay = 10 # seconds

    def implicit_wait(self, xpath):
        try:
            myElem = WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
            print("item is ready")
        except TimeoutException:
            print("Loading took too much time!")
            
            
mypath = utils.mypath
scrape = Scraper(mypath)
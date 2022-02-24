import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

class scraper:
    
    def __init__(self):
        self.mypath = os.getcwd()
        self.yahoo_fin_req = os.path.dirname(self.mypath)
        self.data_manager = os.path.dirname(self.yahoo_fin_req)
        self.home_dir = os.path.dirname(self.data_manager)

        # database path 
        self.database = os.path.join(self.home_dir, 'Database')
        self.database_stock_data = os.path.join(self.database, 'stock_data')
        self.database_stock = os.path.join(self.database_stock_data, 'stock')
        self.database_stock_properties = os.path.join(self.database_stock_data, 'stock_properties')
        
        # selenium
        self.options = Options()
        self.chromedriver_path = os.path.join(self.mypath, 'SeleniumDrivers', 'chromedriver.exe')
        self.options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe" # route to chrome exe path
        self.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        self.options.add_argument(f'user-agent={self.userAgent}')
        self.browser = webdriver.Chrome(options=self.options, executable_path=self.chromedriver_path)
        self.delay = 10 # seconds
        
    def open_json(self, filename):
        with open(f'{filename}', 'r', encoding='utf-8') as f:
            d = json.load(f)
        return(d)

    def save_json(self, data, filename):
        with open(f'{filename}', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        

    # selenium functions
    def close_selenium(self):
        self.browser.close()
        
    def go_web(self, link_address):
        self.browser.maximize_window()
        self.browser.get(link_address)
        
    def click_item(self, xpath):
        self.browser.find_element_by_xpath(xpath).click()
        
    def implicit_wait(self, xpath):
        try:
            myElem = WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
            print("item is ready")
        except TimeoutException:
            print("Loading took too much time!")
            
fx = scraper()
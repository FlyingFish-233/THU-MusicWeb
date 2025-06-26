import selenium
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests

# WebDriverWait的等待时间上限
WDW_LIM = 10

class BaseCrawler:

    def __init__(self):
        self.driver = selenium.webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.get('https://y.qq.com/n/ryqq/singer_list/')
        self.driver.maximize_window()


    @staticmethod
    def download_image(url, path):
        r = requests.get(url)
        r.raise_for_status()
        with open(path, 'wb') as f:
            f.write(r.content)


    def login(self):
        login_button = WebDriverWait(self.driver, WDW_LIM).until(
            EC.presence_of_element_located((By.XPATH, '//a[@class="top_login__link"]'))
        )
        login_button.click()
        WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, '//img[@class="top_login__cover js_userInfo_img"]'))
        )

if __name__ == '__main__':
    crawler = BaseCrawler()
    crawler.login()
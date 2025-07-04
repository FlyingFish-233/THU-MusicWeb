from selenium.webdriver.common.by import By

import time
import os
import json

from BaseCrawler import BaseCrawler

SINGER_MAX = 300
path = 'singer/urls.json'

class URLCrawler(BaseCrawler):

    def __init__(self):
        super().__init__()
        os.makedirs('singer/', exist_ok=True)
        self.urls = []


    def save(self):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.urls, f)


    def crawl(self):
        # 向下滚动
        for i in range(5):
            time.sleep(0.5)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 获取歌手的url
        singer_tags = self.driver.find_elements(By.XPATH, '//a[@class="singer_list__cover"]')
        singer_urls = [singer_tag.get_attribute('href') for singer_tag in singer_tags]
        singer_tags = self.driver.find_elements(By.XPATH, '//a[@class="singer_list_txt__link js_singer"]')
        singer_urls += [singer_tag.get_attribute('href') for singer_tag in singer_tags]
        self.urls = singer_urls[:SINGER_MAX]
        self.save()


def getSingerURL(crawl=False):
    if crawl:
        crawler = URLCrawler()
        crawler.crawl()
    with open(path, 'r', encoding='utf-8') as f:
        urls = json.load(f)
        return urls
    

if __name__ == '__main__':
    urls = getSingerURL(crawl=True)
    print(len(urls))
    print(urls)
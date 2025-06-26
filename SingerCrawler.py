from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import os
from tqdm import tqdm
import json

from BaseCrawler import BaseCrawler
from URLCrawler import getSingerURL

# WebDriverWait的等待时间上限
WDW_LIM = 10

# 一个json文件存储的歌手数量
SINGER_BATCH_SIZE = 10

# 存储歌手图片的路径
img_dir = 'singer/img/'
# 存储歌手信息的路径
json_dir = 'singer/json/'

class SingerCrawler(BaseCrawler):

    def __init__(self):
        super().__init__()
        os.makedirs(img_dir, exist_ok=True)
        os.makedirs(json_dir, exist_ok=True)
        self.urls = getSingerURL()
        self.singers = []
    

    def crawl_singer_page(self, url, id):
        self.driver.get(url)
        # 歌手图片
        img_tag = WebDriverWait(self.driver, WDW_LIM).until(
            EC.presence_of_element_located((By.XPATH, '//img[@class="data__photo"]'))
        )
        img_url = img_tag.get_attribute('src')
        img_path = os.path.join(img_dir, f'{id}.jpg')
        SingerCrawler.download_image(img_url, img_path)
        # 歌手名字
        name_tag = self.driver.find_element(By.XPATH, '//h1[@class="data__name_txt"]')
        name = name_tag.get_attribute("textContent")
        # 歌手简介
        try:
            description_tag = self.driver.find_element(By.XPATH, '//div[@class="data__desc_txt"]')
            description = description_tag.get_attribute("textContent")
        except NoSuchElementException:
            description = ""
        # 歌手条目信息
        info_items_tag = self.driver.find_element(By.XPATH, '//ul[@class="mod_data_statistic"]')
        info_items = info_items_tag.get_attribute("textContent")
        # 更新歌手列表
        self.singers.append({
            'id':id,
            'name':name,
            'img_path':img_path,
            'description':description,
            'info_items':info_items,
            'url':url
        })
    

    def crawl(self):
        for i, url in enumerate(tqdm(self.urls, desc='爬取进度')):
            self.crawl_singer_page(url, i + 1)
            if (i + 1) % SINGER_BATCH_SIZE == 0 or i == len(self.urls) - 1:
                self.save(i // SINGER_BATCH_SIZE + 1)


    def save(self, idx):
        path = os.path.join(json_dir, f'singer{idx}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.singers, f)
            self.singers = []


def getSingerInfo(idx, crawl=False):
    if crawl:
        crawler = SingerCrawler()
        crawler.login()
        crawler.crawl()
    path = os.path.join(json_dir, f'singer{idx}.json')
    with open(path, 'r', encoding='utf-8') as f:
        singers = json.load(f)
        return singers


if __name__ == '__main__':
    singers = getSingerInfo(1, crawl=False)
    for singer in singers:
        print(singer['url'])
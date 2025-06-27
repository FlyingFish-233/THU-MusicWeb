from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import os
import time
from tqdm import tqdm
import json

from BaseCrawler import BaseCrawler
from SingerCrawler import getSongURL

# WebDriverWait的等待时间上限
WDW_LIM = 10

# 一个json文件存储的歌曲数量
SONG_BATCH_SIZE = 100

# 存储歌曲图片的路径
img_dir = 'song/img/'
# 存储歌曲信息的路径
json_dir = 'song/json/'

class SongCrawler(BaseCrawler):

    def __init__(self):
        super().__init__()
        os.makedirs(img_dir, exist_ok=True)
        os.makedirs(json_dir, exist_ok=True)
        self.urls = getSongURL()
        self.songs = []
    

    def crawl_song_page(self, url, id):
        self.driver.get(url)
        # 歌曲图片
        img_tag = WebDriverWait(self.driver, WDW_LIM).until(
            EC.presence_of_element_located((By.XPATH, '//img[@class="data__photo"]'))
        )
        img_url = img_tag.get_attribute('src')
        img_path = os.path.join(img_dir, f'{id}.jpg')
        SongCrawler.download_image(img_url, img_path)
        # 歌曲名字
        name_tag = self.driver.find_element(By.XPATH, '//h1[@class="data__name_txt"]')
        name = name_tag.get_attribute("textContent")
        # 歌曲简介
        try:
            description_tag = self.driver.find_element(By.XPATH, '//div[@class="about__cont"]')
            description = description_tag.get_attribute("textContent")
        except NoSuchElementException:
            description = ""
        # 歌曲条目信息
        info_items_tag = self.driver.find_element(By.XPATH, '//ul[@class="data__info"]')
        info_items = info_items_tag.get_attribute("textContent")
        # 歌手名字
        singer_name_tag = self.driver.find_element(By.XPATH, '//div[@class="data__singer"]')
        singer_name = singer_name_tag.get_attribute("textContent")
        # 歌词
        time.sleep(0.5)
        lyric_tag = self.driver.find_element(By.XPATH, '//div[@class="lyric__cont_box"]')
        lyric = lyric_tag.get_attribute("textContent")
        if lyric == '暂无歌词':
            time.sleep(2)
            lyric_tag = self.driver.find_element(By.XPATH, '//div[@class="lyric__cont_box"]')
            lyric = lyric_tag.get_attribute("textContent")
        # 更新self.songs
        self.songs.append({
            'id':id,
            'name':name,
            'img_path': img_path,
            'lyric': lyric,
            'description': description,
            'info_items':info_items,
            'url':url,
            'singer_name':singer_name,
        })
    

    # 保存歌曲信息
    def save(self, idx):
        path = os.path.join(json_dir, f'song{idx}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.songs, f)
            self.songs = []
    

    def crawl(self):
        for i, url in enumerate(tqdm(self.urls, desc='爬取进度')):
            self.crawl_song_page(url, i)
            if (i + 1) % SONG_BATCH_SIZE == 0 or i == len(self.urls) - 1:
                self.save(i // SONG_BATCH_SIZE + 1)


def getSongInfo(idx, crawl=False):
    if crawl:
        crawler = SongCrawler()
        crawler.login()
        crawler.crawl()
    file_id = idx // SONG_BATCH_SIZE + 1
    path = os.path.join(json_dir, f'song{file_id}.json')
    with open(path, 'r', encoding='utf-8') as f:
        songs = json.load(f)
        for song in songs:
            if song['id'] == idx:
                return song
        raise IndexError(f'没有以{idx}为id的歌曲')


if __name__ == '__main__':
    song = getSongInfo(0, crawl=False)
    print(song)

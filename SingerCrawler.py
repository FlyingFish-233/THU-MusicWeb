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

# 一个歌手爬取的歌曲数量
SONG_PER_SINGER = 10

# 存储歌手图片的路径
img_dir = 'singer/img/'
# 存储歌手信息的路径
json_dir = 'singer/json/'
# 存储歌曲url的路径
song_path = 'song/urls.json'
# 存储歌手-歌曲对应关系的路径
edge_path = 'song/ss_edges.json'

class SingerCrawler(BaseCrawler):

    def __init__(self):
        super().__init__()
        os.makedirs(img_dir, exist_ok=True)
        os.makedirs(json_dir, exist_ok=True)
        os.makedirs('song/', exist_ok=True)
        self.urls = getSingerURL()
        self.singers = []
        self.song_urls = {}
        self.ss_edges = []
    

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
        # 歌曲的url及其与歌手的对应关系
        song_tags = self.driver.find_elements(By.XPATH, '//span[@class="songlist__songname_txt"]/a')
        for i in range(min(len(song_tags), SONG_PER_SINGER)):
            song_url = song_tags[i].get_attribute('href')
            if song_url in self.song_urls:
                song_id = self.song_urls[song_url]
            else:
                song_id = len(self.song_urls)
                self.song_urls[song_url] = song_id
            self.ss_edges.append((id, song_id))
    

    # 保存歌手信息
    def save(self, idx):
        path = os.path.join(json_dir, f'singer{idx}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.singers, f)
            self.singers = []

    
    # 保存歌曲及歌手-歌曲对应关系
    def save_songs(self):
        song_urls = [""] * len(self.song_urls)
        for song_url, song_id in self.song_urls.items():
            song_urls[song_id] = song_url
        with open(song_path, 'w', encoding='utf-8') as f:
            json.dump(song_urls, f)
        with open(edge_path, 'w', encoding='utf-8') as f:
            json.dump(self.ss_edges, f)
    

    def crawl(self):
        for i, url in enumerate(tqdm(self.urls, desc='爬取进度')):
            self.crawl_singer_page(url, i)
            if (i + 1) % SINGER_BATCH_SIZE == 0 or i == len(self.urls) - 1:
                self.save(i // SINGER_BATCH_SIZE + 1)
        self.save_songs()


def getSingerInfo(idx, crawl=False):
    if crawl:
        crawler = SingerCrawler()
        crawler.login()
        crawler.crawl()
    file_id = idx // SINGER_BATCH_SIZE + 1
    path = os.path.join(json_dir, f'singer{file_id}.json')
    with open(path, 'r', encoding='utf-8') as f:
        singers = json.load(f)
        for singer in singers:
            if singer['id'] == idx:
                return singer
        raise IndexError(f'没有以{idx}为id的歌手')
    

def getSongURL(crawl=False):
    if crawl:
        crawler = SingerCrawler()
        crawler.login()
        crawler.crawl()
    with open(song_path, 'r', encoding='utf-8') as f:
        song_urls = json.load(f)
        return song_urls
    

def getSSEdge(crawl=False):
    if crawl:
        crawler = SingerCrawler()
        crawler.login()
        crawler.crawl()
    with open(edge_path, 'r', encoding='utf-8') as f:
        ss_edges = json.load(f)
        return ss_edges


if __name__ == '__main__':
    singer = getSingerInfo(0, crawl=False)
    print(singer)
    song_urls = getSongURL(crawl=False)
    print(len(song_urls))
    ss_edges = getSSEdge(crawl=False)
    print(len(ss_edges))

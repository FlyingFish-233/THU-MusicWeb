import selenium
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import time
import os
import requests
from tqdm import tqdm
import json

class QQCrawler:
    WDW_LIM = 10
    SINGER_MAX = 300
    SONG_PER_SINGER = 10
    SINGER_BATCH_SIZE = 10

    def __init__(self):
        # 初始url
        self.start_url = 'https://y.qq.com/n/ryqq/singer_list/'
        # 创建文件夹
        self.dirs = ['singer/', 'singer/img/', 'song/', 'song/img/']
        for dir in self.dirs:
            if not os.path.exists(dir):
                os.makedirs(dir)
        # 谷歌驱动
        self.driver = selenium.webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.get(self.start_url)
        self.driver.maximize_window() 
        # 歌手及歌曲信息
        self.singer_num = 0
        self.song_num = 0
        self.singers = []
        self.songs = []


    @staticmethod
    def download_image(url, path):
        r = requests.get(url)
        r.raise_for_status()
        with open(path, 'wb') as f:
            f.write(r.content)


    def crawl_song(self, url, singer):
        self.driver.get(url)
        # 歌曲id
        self.song_num += 1
        id = self.song_num
        # 歌曲图片
        img_tag = WebDriverWait(self.driver, QQCrawler.WDW_LIM).until(
            EC.presence_of_element_located((By.XPATH, '//img[@class="data__photo"]'))
        )
        img_url = img_tag.get_attribute('src')
        img_path = os.path.join('song/img/', f'{id}.jpg')
        QQCrawler.download_image(img_url, img_path)
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
        print(info_items)
        # 更新self.songs
        song = {
            'id':id,
            'name':name,
            'img_path': img_path,
            'lyric': lyric,
            'description': description,
            'info_items':info_items,
            'url':url,
            'singer_id':singer['id'],
            'singer_name':singer_name,
        }
        self.songs.append(song)


    def crawl_singer(self, url):
        self.driver.get(url)
        # 歌手id
        self.singer_num += 1
        id = self.singer_num
        # 歌手图片
        img_tag = WebDriverWait(self.driver, QQCrawler.WDW_LIM).until(
            EC.presence_of_element_located((By.XPATH, '//img[@class="data__photo"]'))
        )
        img_url = img_tag.get_attribute('src')
        img_path = os.path.join('singer/img/', f'{id}.jpg')
        QQCrawler.download_image(img_url, img_path)
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
        # 更新self.singers
        singer = {
            'id':id,
            'name':name,
            'img_path':img_path,
            'description':description,
            'info_items':info_items,
            'url':url
        }
        self.singers.append(singer)
        # 爬取歌曲
        song_tags = self.driver.find_elements(By.XPATH, '//span[@class="songlist__songname_txt"]/a')
        song_urls = [song_tags[i].get_attribute('href') for i in range(min(len(song_tags), QQCrawler.SONG_PER_SINGER))]
        for song_url in song_urls:
            self.crawl_song(song_url, singer)
    
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
        # 爬取歌手信息
        start_index = 0
        for i, url in enumerate(tqdm(singer_urls[start_index:QQCrawler.SINGER_MAX], desc='爬取进度')):
            self.crawl_singer(url)
            idx = start_index + i
            if (idx + 1) % QQCrawler.SINGER_BATCH_SIZE == 0 or idx == QQCrawler.SINGER_MAX - 1:
                self.save(idx // QQCrawler.SINGER_BATCH_SIZE + 1)


    def login(self):
        login_button = WebDriverWait(self.driver, QQCrawler.WDW_LIM).until(
            EC.presence_of_element_located((By.XPATH, '//a[@class="top_login__link"]'))
        )
        login_button.click()
        WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, '//img[@class="top_login__cover js_userInfo_img"]'))
        )

    def save(self, idx):
        with open(f'singer/singer{idx}.json', 'w', encoding='utf-8') as f:
            json.dump(self.singers, f)
            self.singers = []
        with open(f'song/song{idx}.json', 'w', encoding='utf-8') as f:
            json.dump(self.songs, f)
            self.songs = []

def get_singers(idx):
    with open(f'singer/singer{idx}.json', 'r', encoding='utf-8') as f:
        singers = json.load(f)
    return singers

def get_songs(idx):
    with open('song/song{idx}.json', 'r', encoding='utf-8') as f:
        songs = json.load(f)
    return songs

if __name__ == '__main__':
    crawler = QQCrawler()
    crawler.login()
    crawler.crawl()
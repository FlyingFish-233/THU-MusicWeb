import os
import sys

from Music.models import Singer
from Music.models import Song

# 将Crawler文件夹添加到path中
root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(root, 'Crawler/'))

from Crawler.SingerCrawler import getSingerInfo, getSSEdge
from Crawler.SongCrawler import getSongInfo

singer_num = 300
song_num = 2866

def load_singer():
    for i in range(singer_num):
        os.chdir('Crawler') # 工作路径需要在Crawler文件夹下
        singer = getSingerInfo(i)
        os.chdir('..')
        Singer.objects.create(
            id = singer['id'],
            name = singer['name'],
            img_path = singer['img_path'],
            description = singer['description'],
            info_items = singer['info_items'],
            url = singer['url']
        )

# python manage.py shell
# from load_singer import load_singer
# load_singer()

if __name__ == '__main__':
    load_singer()
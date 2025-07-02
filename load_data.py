import os
import sys
from tqdm import tqdm

from Music.models import Singer
from Music.models import Song

# 将Crawler文件夹添加到path中
root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(root, 'Crawler/'))

from Crawler.SingerCrawler import getSingerInfo, getSSEdge
from Crawler.SongCrawler import getSongInfo

singer_num = 300
song_num = 2871

def load_singer():
    for i in tqdm(range(singer_num), desc='歌手导入进度'):
        os.chdir('Crawler') # 工作路径需要在Crawler文件夹下
        singer = getSingerInfo(i)
        os.chdir('..')
        Singer.objects.create(
            id = singer['id'],
            name = singer['name'],
            img_path = singer['img_path'],
            description = '\n'.join(singer['description']),
            info_items = singer['info_items'],
            url = singer['url']
        )

def load_song():
    for i in tqdm(range(song_num), desc='歌曲导入进度'):
        os.chdir('Crawler')
        song = getSongInfo(i)
        os.chdir('..')
        Song.objects.create(
            id = song['id'],
            name = song['name'],
            img_path = song['img_path'],
            lyric = '\n'.join(song['lyric']),
            description = song['description'],
            info_items = song['info_items'],
            url = song['url'],
            singer_name = song['singer_name']
        )


def load_ss_edge():
    os.chdir('Crawler')
    ss_edges = getSSEdge()
    os.chdir('..')
    for singer_id, song_id in tqdm(ss_edges, desc='歌手-歌曲关系导入进度'):
        singer = Singer.objects.get(id=singer_id)
        song = Song.objects.get(id=song_id)
        song.singers.add(singer)


'''
python manage.py shell
from load_data import *
load_singer()
load_song()
load_ss_edge()
'''
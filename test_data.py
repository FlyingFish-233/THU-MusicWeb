from Music.models import Singer
from Music.models import Song

def test_singer():
    print("歌手数量：", Singer.objects.count())
    print("名字中含‘周’的歌手数量：", Singer.objects.filter(name__contains="周").count())
    
    singer = Singer.objects.get(name="周杰伦")
    print(f"ID: {singer.id}")
    print(f"姓名: {singer.name}")
    print(f"图片路径: {singer.img_path}")
    print(f"描述: {singer.description}")
    print(f"信息项: {singer.info_items}")
    print(f"URL: {singer.url}")

    print("\n关联歌曲：")
    for song in singer.songs.all():
        print(f"- {song.name} (ID: {song.id})")


def test_song():
    print("歌曲总数：", Song.objects.count())
    print("名字中含‘爱’的歌曲数量：", Song.objects.filter(name__contains="爱").count())

    song = Song.objects.get(id=0)
    print(f"ID: {song.id}")
    print(f"歌曲名: {song.name}")
    print(f"图片路径: {song.img_path}")
    print(f"歌词: {song.lyric}")
    print(f"描述: {song.description}")
    print(f"信息项: {song.info_items}")
    print(f"URL: {song.url}")
    print(f"歌手名: {song.singer_name}")
    
    print("\n关联歌手：")
    for singer in song.singers.all():
        print(f"- {singer.name} (ID: {singer.id})")


'''
python manage.py shell
from test_data import *
test_singer()
test_song()
'''
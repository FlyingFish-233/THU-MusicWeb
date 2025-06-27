from Music.models import Singer

def singer_test():
    print("歌手数量：", Singer.objects.count())
    print("名字中含‘周’的歌手数量：", Singer.objects.filter(name__contains="周").count())
    singer = Singer.objects.get(name="周杰伦")
    print(f"ID: {singer.id}")
    print(f"姓名: {singer.name}")
    print(f"图片路径: {singer.img_path}")
    print(f"描述: {singer.description}")
    print(f"信息项: {singer.info_items}")
    print(f"URL: {singer.url}")
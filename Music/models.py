from django.db import models


# Create your models here.
class Singer(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    img_path = models.CharField(max_length=100)
    description = models.TextField(blank=True) # 允许字符串为空
    info_items = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name


class Song(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    img_path = models.CharField(max_length=100)
    lyric = models.TextField(blank=True)
    description = models.TextField(blank=True)
    info_items = models.CharField(max_length=100)
    url = models.URLField()
    singer_name = models.CharField(max_length=100)
    singers = models.ManyToManyField(Singer, related_name='songs') # 建立多对多关系

    def __str__(self):
        return self.name
    

class Comment(models.Model):
    song = models.ForeignKey(Song, models.CASCADE)
    user = models.CharField(max_length=100)
    comment_content = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} : {self.comment_content}'
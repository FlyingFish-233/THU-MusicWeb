from Music.models import Singer, Song, Comment
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

LIST_NUM = 20

def song_list(request, id):
    song_start = (id - 1) * LIST_NUM
    song_end = min(id * LIST_NUM - 1, Song.objects.count() - 1)
    if song_start >= Song.objects.count():
        return HttpResponseRedirect('/song')
    songs = Song.objects.filter(id__range=(song_start, song_end))
    
    template = loader.get_template("song/list.html")
    context = {
        'songs' : songs,
    }
    return HttpResponse(template.render(context, request))


def song_detail(request, id):
    song = get_object_or_404(Song, id=id)

    template = loader.get_template("song/detail.html")
    context = {
        'song' : song,
    }
    return HttpResponse(template.render(context, request))


def singer_list(request, id):
    singer_start = (id - 1) * LIST_NUM
    singer_end = min(id * LIST_NUM - 1, Singer.objects.count() - 1)
    if singer_start >= Singer.objects.count():
        return HttpResponseRedirect('/singer')
    singers = Singer.objects.filter(id__range=(singer_start, singer_end))
    
    template = loader.get_template("singer/list.html")
    context = {
        'singers' : singers,
    }
    return HttpResponse(template.render(context, request))


def singer_detail(request, id):
    singer = get_object_or_404(Singer, id=id)

    template = loader.get_template("singer/detail.html")
    context = {
        'singer' : singer,
    }
    return HttpResponse(template.render(context, request))


from Music.models import Singer, Song, Comment
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

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
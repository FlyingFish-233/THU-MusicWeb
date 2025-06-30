from Music.models import Singer, Song, Comment
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage

LIST_NUM = 20

def song_list(request):
    page_number = request.GET.get('page', 1)
    try:
        all_songs = Song.objects.all().order_by('id')
        paginator = Paginator(all_songs, LIST_NUM)
        page_obj = paginator.page(page_number)
        context = {
            'songs': page_obj.object_list,
            'page_obj': page_obj,
        }
        return render(request, "song/list.html", context)
    except EmptyPage:
        return HttpResponseRedirect('/song')


def song_detail(request, id):
    song = get_object_or_404(Song, id=id)

    template = loader.get_template("song/detail.html")
    context = {
        'song' : song,
    }
    return HttpResponse(template.render(context, request))


def singer_list(request):
    page_number = request.GET.get('page', 1)
    try:
        all_singers = Singer.objects.all().order_by('id')
        paginator = Paginator(all_singers, LIST_NUM)
        page_obj = paginator.page(page_number)
        context = {
            'singers': page_obj.object_list,
            'page_obj': page_obj,
        }
        return render(request, "singer/list.html", context)
    except EmptyPage:
        return HttpResponseRedirect('/singer')


def singer_detail(request, id):
    singer = get_object_or_404(Singer, id=id)

    template = loader.get_template("singer/detail.html")
    context = {
        'singer' : singer,
    }
    return HttpResponse(template.render(context, request))


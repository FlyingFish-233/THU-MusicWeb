from Music.models import Singer, Song, Comment
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages
from django.urls import reverse

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
        return redirect('/song')


def song_detail(request, id):
    song = get_object_or_404(Song, id=id)

    context = {
        'song' : song,
        'comments': song.comment_set.all(),
    }
    return render(request, "song/detail.html", context)


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
        return redirect('/singer')


def singer_detail(request, id):
    singer = get_object_or_404(Singer, id=id)

    context = {
        'singer' : singer,
    }
    return render(request, "singer/detail.html", context)


def comment(request, id):
    song = get_object_or_404(Song, id=id)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        comment_content = request.POST.get('comment')
        
        if not username or not comment_content:
            messages.error(request, "用户名和评论内容不能为空！")
        elif len(username) > 20 or len(comment_content) > 100:
            messages.error(request, "用户名和评论内容分别不能超过20字符和100字符！")
        else:
            Comment.objects.create(
                song=song,
                user=username,
                comment_content=comment_content
            )
            messages.success(request, "评论发布成功！")
    return redirect(reverse('song_detail', kwargs={'id': id}) + '#commentMainBlock')
from Music.models import Singer, Song, Comment
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages
from django.db.models import Q
import time

LIST_NUM = 20

def song_list(request):
    query = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)

    start_time = time.time()

    if not query or len(query) > 20:
        songs = Song.objects.all().order_by('id')
        page_base_url = f'song?page='
    else:
        songs = Song.objects.filter(
            Q(name__icontains=query) |
            Q(singer_name__icontains=query) |
            Q(lyric__icontains=query)
        ).distinct().order_by('id')
        page_base_url = f'song?q={query}&page='

    paginator = Paginator(songs, LIST_NUM)
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        return redirect('song')
    
    end_time = time.time()
    
    context = {
        'songs': page_obj.object_list,
        'page_obj': page_obj,
        'query': query,
        'page_base_url': page_base_url,
        'songs_num': songs.count(),
        'search_time': f'{end_time - start_time:.4f}s'
    }
    return render(request, "song/list.html", context)


def song_detail(request, id):
    song = get_object_or_404(Song, id=id)

    context = {
        'song' : song,
        'comments': song.comment_set.all(),
    }
    return render(request, "song/detail.html", context)

def singer_list(request):
    query = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)
    start_time = time.time()

    if not query or len(query) > 20:
        singers = Singer.objects.all().order_by('id')
        page_base_url = f'singer?page='
    else:
        singers = Singer.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        ).distinct().order_by('id')
        page_base_url = f'singer?q={query}&page='

    paginator = Paginator(singers, LIST_NUM)
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        return redirect('singer')
    
    end_time = time.time()
    
    context = {
        'singers': page_obj.object_list,
        'page_obj': page_obj,
        'query': query,
        'page_base_url': page_base_url,
        'singers_num': singers.count(),
        'search_time': f'{end_time - start_time:.4f}s'
    }
    return render(request, "singer/list.html", context)


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

    return redirect(f'song/detail/{id}#commentMainBlock')

from django.urls import path, include
import Music.views as views

urlpatterns = [
    path('', views.song_list, {'id': 1}, name='root'),
    path('song', views.song_list, {'id': 1}, name='song'),
    path('song/<int:id>', views.song_list, name='song_list'),
    path('song/detail/<int:id>', views.song_detail, name='song_detail'),
    path('singer', views.singer_list, {'id': 1}, name='singer'),
    path('singer/<int:id>', views.singer_list, name='singer_list'),
    path('singer/detail/<int:id>', views.singer_detail, name='singer_detail'),
]
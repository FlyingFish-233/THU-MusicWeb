from django.urls import path, include
import Music.views as views

urlpatterns = [
    path('', views.song_list, {'id': 1}, name='root'),
    path('song', views.song_list, {'id': 1}, name='song'),
    path('song/<int:id>', views.song_list, name='song_list'),
]
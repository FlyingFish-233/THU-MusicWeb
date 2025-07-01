from django.urls import path, include
import Music.views as views

urlpatterns = [
    path('', views.song_list, name='home'),
    path('song', views.song_list, name='song'),
    path('song/detail/<int:id>', views.song_detail, name='song_detail'),
    path('singer', views.singer_list, name='singer'),
    path('singer/detail/<int:id>', views.singer_detail, name='singer_detail'),
    path('comment/<int:id>', views.comment, name='comment'),
]
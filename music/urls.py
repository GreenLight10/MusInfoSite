from django.urls import path

from .views import *


urlpatterns = [
    path('', base, name='base'),
    path('genres/', genres, name='genres'),
    path('artists/', artists, name='artists'),
    path('news/', news, name='news'),
    path('login/', loginF, name='login'),
    path('logout/', logoutF, name='logout'),
    path('registration/', registrationF, name='registration'),
    path('profileEd/', profile_editor, name='profile_editor'),
    path('posts/', cat_posts, name='posts'),
    path('posts/<slug:slug>/', post_detail_cat, name='post_detail_cat'),
    path('posts/detpost/<slug:slug>/',
         PostDetailView.as_view(), name='post_detail'),
    path('kabinet/', kabinet, name='kabinet'),
    path('genres/genre/<slug:slug>/', artist_genre, name='artist_genre'),
    path('<slug:slug>/', artist_detail, name='artist_detail'),
    path('genres/<slug:slug>/', genre_detail, name='genre_detail'),
    path('news/<slug:slug>/', new_detail, name='new_detail'),
    path('artists/<slug:slug>/', albums, name='albums'),
    path('artists/albums/<slug:slug>/', album_detail, name='album_detail'),
]
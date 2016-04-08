from django.conf.urls import include, url
from django.contrib import admin
from tweets import views #gets all our view functions

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),

    url(r'^register$', views.Register.as_view(), name='register'),
    url(r'^login$', views.Login.as_view(), name='login'),
    url(r'^logout$', views.Logout.as_view(), name='logout'),

    url(r'^create$', views.Create_Tweet.as_view(), name="create"),
    url(r'^(?P<pk>[\d]+)/edit$', views.Edit.as_view(), name='edit'),
    url(r'^(?P<pk>[\d]+)/delete$', views.Delete.as_view(), name='delete'),

    url(r'^timeline$', views.Get_All.as_view(), name="timeline"),
    url(r'^(?P<pk>[\d]+)/profile$', views.Profile.as_view(), name='profile'),
    url(r'^(?P<pk>[\d]+)/repost$', views.Repost.as_view(), name='repost'),
    url(r'^(?P<pk>[\d]+)/up$', views.Up.as_view(), name='up'),
    url(r'^(?P<pk>[\d]+)/down$', views.Down.as_view(), name='down'),

    url(r'^search_user$', views.Search_User.as_view(), name="search_user"),
    url(r'^search_tag$', views.Search_Tag.as_view(), name="search_tag"),
]


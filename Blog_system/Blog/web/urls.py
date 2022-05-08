from django.contrib import admin
from django.urls import path

from Blog import settings
from Blog.web import views
from django.views.static import serve

urlpatterns = [
    path("getCategory/", views.getCategory, name="getCategory"),
    path("getLabel/", views.getLabel, name="getLabel"),
    path("uploadImg/", views.uploadImg.as_view(), name='uploadImg'),
    path("publish/", views.Publish.as_view(), name="publish"),
    path("postList/", views.PostList.as_view(), name="getPosts"),
    path("post/", views.Post.as_view(), name="getPost"),
    path("byLabel/", views.ByLabel.as_view(), name="getPostByLabel"),
    path("byCategory/", views.ByCategory.as_view(), name="getPostByCategory"),
    path("count/", views.Count.as_view(), name="Count"),
    path("getImg/", views.GetImg.as_view(), name="getImg"),
    path("search/", views.Search.as_view(), name="Search"),
    path("comment/", views.Comment.as_view(), name="Comment"),
    path("hot/",views.Hot.as_view(),name="Hot"),
]

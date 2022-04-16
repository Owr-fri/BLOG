from django.contrib import admin
from django.urls import path
from Blog.web import views

urlpatterns = [
    path("getCode/", views.GetCode.as_view(), name="getCode"),
    path("login/", views.Login.as_view(), name="login"),
    path("getCategory/",views.getCategory,name="getCategory"),
    path("getLabel/",views.getLabel,name="getLabel"),
    path("api/uploadImg/",views.uploadImg,name='uploadImg'),
    path("api/publish/",views.Publish.as_view(),name="publish"),
    path("getPosts/",views.GetPosts.as_view(),name="getPosts"),
    path("getPost/",views.GetPost.as_view(),name="getPost"),
    path("like/",views.Like.as_view(),name="like"),
    path("getPostByLabel/",views.GetPostByLabel.as_view(),name="getPostByLabel"),
    path("getPostByCategory/",views.GetPostByCategory.as_view(),name="getPostByCategory"),
]

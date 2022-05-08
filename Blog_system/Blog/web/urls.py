from django.contrib import admin
from django.urls import path

from Blog import settings
from Blog.web import views
from django.views.static import serve

urlpatterns = [
    path("getCode/", views.GetCode.as_view(), name="getCode"),
    path("login/", views.Login.as_view(), name="login"),
    path("getCategory/", views.getCategory, name="getCategory"),
    path("getLabel/", views.getLabel, name="getLabel"),
    path("api/uploadImg/", views.uploadImg.as_view(), name='uploadImg'),
    path("api/publish/", views.Publish.as_view(), name="publish"),
    path("getPosts/", views.GetPosts.as_view(), name="getPosts"),
    path("getPost/", views.GetPost.as_view(), name="getPost"),
    path("like/", views.Like.as_view(), name="like"),
    path("getPostByLabel/", views.GetPostByLabel.as_view(), name="getPostByLabel"),
    path("getPostByCategory/", views.GetPostByCategory.as_view(), name="getPostByCategory"),
    path("pictures/", views.Picture.as_view(), name="publishPicture"),
    path("getPictureDesc/", views.GetPictureDesc.as_view(), name="getPictureDesc"),
    path("getPictureRec/", views.GetPictureRec.as_view(), name="getPictureRec"),
    path("getCount/", views.GetCount.as_view(), name="getCount"),
    path("getImg/", views.GetImg.as_view(),name="getImg"),
    path("updatePicture/", views.UpdatePicture.as_view(), name="updatePicture"),
    path("search/",views.Search.as_view(),name="Search"),
    path("isAdmin/",views.IsAdmin.as_view(),name="isAdmin"),
    path("info/",views.UserInfo.as_view(),name='userInfo'),
    path("comment/",views.Comment.as_view(),name='comment'),
    path('avatar/',views.Avatar.as_view(),name='avatar'),
    path('register/',views.Register.as_view(),name="register")
]

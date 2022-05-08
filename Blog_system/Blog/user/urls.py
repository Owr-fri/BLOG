from django.contrib import admin
from django.urls import path
from Blog.user import views
from django.views.static import serve

urlpatterns = [
    path("code/", views.Code.as_view(), name="Code"),
    path("login/", views.Login.as_view(), name="Login"),
    path("info/", views.Info.as_view(), name="Info"),
    path("comment/", views.Comment.as_view(), name="Comment"),
    path("avatar/", views.Avatar.as_view(), name="Avatar"),
    path("register/", views.Register.as_view(), name="Register"),
    path("like/", views.Like.as_view(), name="Like"),
    path("admin/", views.Admin.as_view(), name="Admin"),
]

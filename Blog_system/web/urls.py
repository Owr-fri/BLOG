from django.contrib import admin
from django.urls import path
from web import views

urlpatterns = [
    path("getCode/", views.GetCode.as_view(), name="getCode"),
    path("login/", views.Login.as_view(), name="login")
]

from django.urls import path
from Blog.picture import views

urlpatterns = [
    path("", views.Picture.as_view(), name="Picture"),
    path("update/", views.Update.as_view(), name="Update"),
    path("describe/", views.Describe.as_view(), name="Describe"),
    path("recommend/", views.Recommend.as_view(), name="Recommend"),
]

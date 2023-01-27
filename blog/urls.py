from django.urls import path
from . import views

urlpatterns = [
    path('', views.StartingPage.as_view(), name="starting-page"),
    path("posts", views.Posts.as_view(), name="posts-page"),
    path("posts/<slug:slug>", views.PostDetail.as_view(), name="post-detail-page"),
    path("read-later", views.ReadLaterView.as_view(), name="read-later")
]
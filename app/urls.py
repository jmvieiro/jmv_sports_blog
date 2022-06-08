from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

app_name = 'blogjmv'

urlpatterns = [

    path("", Index.as_view(), name="index"),

    path("login/", login_request, name="login"),
    path("register/", register, name="register"),
    path("logout/", LogoutView.as_view(template_name="logout.html"), name="logout"),

    path("about/", About.as_view(), name="about"),
    path("post_detail/<pk>", PostDetail.as_view(), name="post_detail"),
    path("post_like/<id>", post_like, name="post_like"),
    path("comment_create/<id>", comment_create, name="comment_create"),
    path("post_by_subject/<pk>", PostBySubject.as_view(), name="post_by_subject"),
    path("post_by_author/<pk>", PostByAuthor.as_view(), name="post_by_author"),

]

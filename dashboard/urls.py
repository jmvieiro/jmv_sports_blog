from django.urls import path
from .views import *

app_name = 'dashboard'

urlpatterns = [
    
    path("admin/", AuthAdmin.as_view(), name="admin"),

    path("subject/index/", subject_index, name="subject_index"),
    path("subject/form/", subject_form, name="subject_form"),
    path("subject/form/<id>", subject_form, name="subject_form"),
    path("subject/create_or_update/", subject_create_or_update,
         name="subject_create_or_update"),
    path("subject/update_state/<id>", subject_update_state,
         name="subject_update_state"),
    path("subject/delete/<id>", subject_delete,
         name="subject_delete"),
    path("subject/delete/confirm/<id>", subject_delete_confirm,
         name="subject_delete_confirm"),

    path("post/index/", AuthPostIndex.as_view(), name="post_index"),
    path("post/form/", post_form, name="post_form"),
    path("post/form/<id>", post_form, name="post_form"),
    path("post/create_or_update/", post_create_or_update,
         name="post_create_or_update"),
    path("post/update_state/<id>", post_update_state,
         name="post_update_state"),
    path("post/delete/<id>", post_delete, name="post_delete"),
    path("post/delete/confirm/<id>", post_delete_confirm,
         name="post_delete_confirm"),

    path("user/form/", user_form, name="user_form"),
    path("user/index/", user_index, name="user_index"),
    path("user/edit_avatar/", user_edit_avatar, name="user_edit_avatar"),

    path("chat/index/", chat_index, name="chat_index"),
    path("chat/index/<id>", chat_index, name="chat_index"),

]
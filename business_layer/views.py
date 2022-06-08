
# Create your views here.
from .models import *


# get- revisado


def get_subjects():
    subjects = []
    posts = get_posts(is_active=True)
    for post in posts:
        if post.subject.is_active:
            subjects.append(post.subject)
    return list(set(subjects))


def get_posts(is_active=None, key_word=None):
    posts = []
    if is_active is None:
        if key_word is None:
            _posts = Post.objects.all()
        else:
            _posts = Post.objects.filter(title__icontains=key_word).__or__(Post.objects.filter(
                subtitle__icontains=key_word)).__or__(Post.objects.filter(content__icontains=key_word))
    else:
        if key_word is None:
            _posts = Post.objects.filter(is_active=is_active)
        else:
            _posts = Post.objects.filter(is_active=is_active, title__icontains=key_word).__or__(Post.objects.filter(
                is_active=is_active, subtitle__icontains=key_word)).__or__(Post.objects.filter(is_active=is_active, content__icontains=key_word))
    for post in _posts:
        if post.author.is_active and post.subject.is_active:
            try:
                post.avatar = Avatar.objects.get(user=post.author)
            except:
                pass
            posts.append(post)
    return posts


def get_authors():
    authors = []
    posts = get_posts(is_active=True)
    for post in posts:
        if post.author.is_active:
            authors.append(post.author)
    return list(set(authors))


def get_post_by_id(id):
    try:
        post = Post.objects.get(pk=id, is_active=True)
        try:
            post.avatar = Avatar.objects.get(user=post.author)
        except:
            pass        
        return post
    except Post.DoesNotExist:
        return None


def get_post_comments(post):
    try:
        return Comment.objects.filter(post=post, is_active=True).order_by('-ts_created')
    except Comment.DoesNotExist:
        return []


def get_subject_by_id(id):
    try:
        return Subject.objects.get(pk=id, is_active=True)
    except Subject.DoesNotExist:
        return None


def get_posts_by_subject(subject_id):
    try:
        posts = []
        _posts = Post.objects.filter(subject=subject_id, is_active=True)
        for post in _posts:
            try:
                post.avatar = Avatar.objects.get(user=post.author)
            except:
                pass
            posts.append(post)
        return posts
    except Post.DoesNotExist:
        return []


def get_author_by_id(id):
    try:
        return User.objects.get(pk=id, is_active=True)
    except User.DoesNotExist:
        return None


def get_posts_by_author(author_id):
    try:
        posts = []
        _posts = Post.objects.filter(author=author_id, is_active=True)
        for post in _posts:
            try:
                post.avatar = Avatar.objects.get(user=post.author)
            except:
                pass
            posts.append(post)
        return posts
    except Post.DoesNotExist:
        return []

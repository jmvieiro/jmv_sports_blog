from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField()

    def __str__(self):
        return self.name


class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f"Avatar del usuario: {self.user.username}"

class Post(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.RESTRICT)
    subject = models.ForeignKey(Subject, on_delete=models.RESTRICT)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    ts_created = models.DateTimeField(editable=False, default=timezone.now)
    ts_updated = models.DateTimeField(editable=False, default=timezone.now)
    is_active = models.BooleanField()
    likes = models.IntegerField(default=0)
    avatar = models.ForeignKey(Avatar, on_delete=models.RESTRICT, null=True, blank=True)
    
    def __str__(self):
        return self.title


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name='sender')
    receiver = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name='receiver')
    content = models.TextField()
    ts_created = models.DateTimeField(editable=False, default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.RESTRICT)
    author = models.ForeignKey(User, on_delete=models.RESTRICT)
    text = models.TextField()
    ts_created = models.DateTimeField(editable=False, default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.post.id} - {self.text}'


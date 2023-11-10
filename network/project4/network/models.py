from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return self.username


class Post(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    content = models.CharField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='users')
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return self.content

    def serialize(self):
        return {
            'id': self.id,
            'user': self.user.username,
            'content': self.content,
            'timestamp': self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            'likes': str(self.likes),
            'likes_count': str(self.like_count)
        }


class Following(models.Model):
    pass

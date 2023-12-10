from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    def __str__(self):
        return self.username


class Puzzle(models.Model):
    date = models.DateField(auto_now_add=False)
    puzzle = models.JSONField()
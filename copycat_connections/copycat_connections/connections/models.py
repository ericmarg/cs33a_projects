from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    solved = models.ManyToManyField("Puzzle", blank=True)

    def __str__(self):
        return self.username


class Puzzle(models.Model):
    date = models.DateField(auto_now_add=False)
    number = models.IntegerField()
    puzzle = models.JSONField()

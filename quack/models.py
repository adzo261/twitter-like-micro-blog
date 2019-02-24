from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Quack(models.Model):
    tags = models.CharField(max_length=100)
    content = models.TextField(max_length=250)
    date_posted = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='fans')

    @property
    def total_likes(self):
        """
        Likes for the company
        :return: Integer: Likes for the company
        """
        return self.likes.count()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_joined = models.DateField(default=timezone.now())
    location = models.TextField(max_length=30, blank=True)

    def __str__(self):
        return f'{self.user.username}\'s Profile'

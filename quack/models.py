from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.TextField(max_length=100)


class Quack(models.Model):
    tags = models.ManyToManyField(Tag, blank=True, related_name='tags')
    content = models.TextField(max_length=250)
    date_posted = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='fans')

    @property
    def likes_count(self):
        """
        Number of likes for this post formatted
        """
        return self.likes.count() if self.likes.count() < 1000 else str(self.likes.count()//1000)+"K"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_joined = models.DateField(default=timezone.now())
    location = models.TextField(max_length=30, blank=True)

    def __str__(self):
        return f'{self.user.username}\'s Profile'

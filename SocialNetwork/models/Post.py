# Package: SocialNetwork.models

from django.conf import settings
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=150, blank=False, null=False)  # Post title.
    body = models.TextField()  # Post body.
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')  # Post auther.
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL)  # Post Likes.

    def __str__(self):
        return '%s(Author: %s)' % (self.title, self.creator.username)

    @property
    def likes_count(self):
        """
        Count the post likes
        :return: The number of post likes
        """
        return self.likes.count()





from django.db import models
from posts.models import Post


class PostLikes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.post) + " " + str(self.like_time)

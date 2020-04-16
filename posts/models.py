from django.db import models
from accounts.models import Profile


class Post(models.Model):
    owner = models.ForeignKey(Profile, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now=True)
    liked_by = models.ManyToManyField(Profile, related_name='liked_posts')
    disliked_by = models.ManyToManyField(Profile, related_name='unliked_posts')

    def __str__(self):
        return self.title
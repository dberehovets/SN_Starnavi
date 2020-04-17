from django.db import models
from posts.models import Post
from accounts.models import Profile


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.post) + " " + str(self.like_date)


class UserActivity(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    activity_time = models.DateTimeField(auto_now=True)
    activity = models.TextField(max_length=200, default="some activity.")

    def __str__(self):
        return self.user.username + " " + self.activity + " " + str(self.activity_time.date())

    class Meta:
        verbose_name_plural = 'User Activities'

from django.contrib import admin
from analytics.models import PostLike, UserActivity

admin.site.register(PostLike)
admin.site.register(UserActivity)
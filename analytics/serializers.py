from rest_framework import serializers
from analytics.models import PostLike, UserActivity


class UserActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserActivity
        exclude = ('id', )
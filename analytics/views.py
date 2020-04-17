from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from rest_framework.response import Response

from analytics.models import PostLike, UserActivity
from analytics.serializers import UserActivitySerializer
from posts.models import Post
from accounts.models import Profile

from datetime import datetime, timedelta

import pytz

from django.conf import settings


class PostLikesView(APIView):
    """
    API view providing information of how many likes were made during a particular period.
    Should receive "date_from" and "date_to" in request parameters.
    """

    def post(self, request, post_id, format=None):

        date_from = datetime.strptime(request.data.get('date_from'), "%Y-%m-%d")
        date_to = datetime.strptime(request.data.get('date_to'), "%Y-%m-%d")

        date_range = self.daterange(date_from, date_to)

        post = Post.objects.get(id=post_id)

        results = {'post_title': post.title}

        for date in date_range:
            likes = PostLike.objects.filter(post=post, like_date=date)
            results[str(date.date())] = likes.count()

        return Response(results, status=status.HTTP_200_OK)

    @classmethod
    def daterange(cls, start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
def user_last_activity(request, user_id):
    """
    Use this view to get user activity.
    """
    user = Profile.objects.get(id=user_id)
    last_login = user.last_login.astimezone(pytz.timezone(settings.TIME_ZONE))

    # If there is a need to receive all user activity instead of just last activity,
    # delete first() at the end of this string and add many=True to UserActivitySerializer
    last_activity = UserActivity.objects.filter(user=user).order_by("-activity_time").first()

    results = {
        'user_last_login': last_login,
        'last activity': UserActivitySerializer(last_activity, many=False).data
    }

    return Response(results, status=status.HTTP_200_OK)
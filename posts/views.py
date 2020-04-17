from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from posts.models import Post
from posts.serializers import PostListSerializer, PostCreationSerializer
from accounts.models import Profile
from analytics.models import UserActivity

from django.shortcuts import get_object_or_404
from django.dispatch import receiver, Signal
from django.http import Http404

user_activity_signal = Signal(providing_args=['user', 'activity'])


class PostList(generics.ListAPIView):
    """
    API view showing list of all posts. GET method adds activity 'viewed the posts' to user activity log.
    """
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

    def get(self, request, *args, **kwargs):

        # Checking of exception is needed if you are logged in as 'admin' and want to see posts list.
        # Admin activity is not added to activity log.

        try:
            user = get_object_or_404(Profile, id=request.user.id)
            user_activity_signal.send(Post, user=user, activity='viewed the posts.')
        except Http404:
            pass
        return self.list(request, *args, **kwargs)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view allowing to view, update or delete a post of a user. GET, PUT, DELETE methods add particular activity
    to user activity log.
    """
    queryset = Post.objects.all()
    serializer_class = PostCreationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        try:
            user = get_object_or_404(Profile, id=request.user.id)
            user_activity_signal.send(Post, user=user, activity='viewed post.')
        except Http404:
            pass
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        try:
            user = get_object_or_404(Profile, id=request.user.id)
            user_activity_signal.send(Post, user=user, activity='updated post.')
        except Http404:
            pass
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            user = get_object_or_404(Profile, id=request.user.id)
            user_activity_signal.send(Post, user=user, activity='deleted post.')
        except Http404:
            pass
        return self.destroy(request, *args, **kwargs)


class PostCreation(generics.CreateAPIView):
    """
    Post creation API view
    """
    queryset = Post.objects.all()
    serializer_class = PostCreationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        owner = get_object_or_404(Profile, id=self.request.user.id)
        serializer.save(owner=owner)
        # add activity to user log
        user_activity_signal.send(Post, user=owner, activity='created post.')


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, post_id):
    """
    Use this view for adding like to a post
    """
    user = Profile.objects.get(id=request.user.id)
    post = Post.objects.get(id=post_id)

    if user not in post.liked_by.all():
        post.liked_by.add(user)

    if user in post.disliked_by.all():
        post.disliked_by.remove(user)

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dislike_post(request, post_id):
    """
    Use this view for adding dislike to a post
    """
    user = Profile.objects.get(id=request.user.id)
    post = Post.objects.get(id=post_id)

    if user in post.liked_by.all():
        post.liked_by.remove(user)

    if user not in post.disliked_by.all():
        post.disliked_by.add(user)

    return Response(status=status.HTTP_200_OK)


@receiver(user_activity_signal)
def register_user_activity(sender, **kwargs):
    """
    Signal receiver and register. Is used for registration of user's activity and adding it to a table in database
    """
    UserActivity.objects.create(user=kwargs['user'], activity=kwargs['activity'])
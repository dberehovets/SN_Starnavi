from rest_framework import generics, permissions, status
from rest_framework.response import Response
from posts.models import Post
from posts.serializers import PostListSerializer, PostCreationSerializer
from accounts.models import Profile
from rest_framework.decorators import api_view, permission_classes


class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PostCreation(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        owner = Profile.objects.get(id=self.request.user.id)
        serializer.save(owner=owner)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, post_id):
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
    user = Profile.objects.get(id=request.user.id)
    post = Post.objects.get(id=post_id)

    if user in post.liked_by.all():
        post.liked_by.remove(user)

    if user not in post.disliked_by.all():
        post.disliked_by.add(user)

    return Response(status=status.HTTP_200_OK)

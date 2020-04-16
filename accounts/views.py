from rest_framework import generics
from accounts.models import Profile
from accounts.serializers import ProfileListSerializer, ProfileCreationSerializer


class UserList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer


class UserCreation(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileCreationSerializer
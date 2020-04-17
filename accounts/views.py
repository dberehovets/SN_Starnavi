from accounts.models import Profile
from accounts.serializers import ProfileListSerializer, ProfileCreationSerializer
from rest_framework import generics


class UserList(generics.ListAPIView):
    """
    API view showing list of users which are instances Profile model.
    Users created with a django command "createsuperuser" are not shown.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    API view showing user details.
    Users created with a django command "createsuperuser" are not shown.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer


class UserCreation(generics.CreateAPIView):
    """
    API view for creation a new user.
    Users created with a django command "createsuperuser" are not shown.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileCreationSerializer



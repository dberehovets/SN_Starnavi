from accounts.models import Profile
from posts.models import Post
from rest_framework import serializers


class ProfileListSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())

    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'posts']


class ProfileCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = super(ProfileCreationSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SN_Starnavi.settings')

import django
django.setup()

## FAKER
import random
from accounts.models import Profile
from posts.models import Post
from faker import Faker

fakegen = Faker()

with open("config.txt") as file:

    values = [int(line.split()[-1]) for line in file.readlines()]  # Get values from config file.

    number_of_users = values[0]
    max_posts_per_user = values[1]
    max_likes_per_user = values[2]


def create_users(number_of_users, max_posts_per_user):  # Creating users. Creating posts of the users.
    for _ in range(number_of_users):
        username = fakegen.email()
        password = fakegen.password()
        first_name = fakegen.first_name()
        last_name = fakegen.last_name()

        user = Profile.objects.get_or_create(
                username=username,
                email=username,
                password=password,
                first_name=first_name,
                last_name=last_name
        )[0]
        for _ in range(random.randrange(0, max_posts_per_user)):
            create_post(user)


def create_post(user):   # Creates one post per user
    title = fakegen.sentence()
    text = fakegen.text()
    Post.objects.get_or_create(
        owner=user,
        title=title,
        text=text
    )


def add_post_likes(max_likes_per_user):   # Adding likes randomly

    users = Profile.objects.all()

    for user in users:
        for _ in range(random.randrange(0, max_likes_per_user)):
            post = Post.objects.order_by("?").first()
            post.liked_by.add(user)


if __name__ == "__main__":
    create_users(number_of_users, max_posts_per_user)   # Call our functions
    add_post_likes(max_likes_per_user)

from django.urls import path
from posts import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostList.as_view(), name="post_list"),
    path('<int:post_id>/', views.PostDetail.as_view(), name='post_detail'),
    path('create/', views.PostCreation.as_view(), name='post_creation'),
    path('<int:post_id>/like/', views.like_post, name='post_like'),
    path('<int:post_id>/dislike/', views.dislike_post, name='post_dislike'),
]
from django.urls import path
from analytics import views

app_name = 'analytics'

urlpatterns = [
    path('post/<int:post_id>/', views.PostLikesView.as_view(), name="post_likes"),
    path('user/<int:user_id>/', views.user_last_activity, name='user_activity'),
]
from django.urls import path
from accounts.views import UserList, UserDetail, UserCreation

app_name = 'accounts'

urlpatterns = [
    path('users/', UserList.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('create/', UserCreation.as_view(), name='create_user'),
]

from django.urls import path

from . import views

urlpatterns = [

    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('posts/', views.PostsView.as_view(), name='posts'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post detail'),
    path('users/<str:username>/posts/', views.UserPostsView.as_view(), name='user posts'),

]



from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('posts/<int:post_id>', views.update_post, name='post'),
    path('user/<str:user_id>', views.profile, name='post'),
    path('following', views.following, name='following')
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('play', views.play, name='play'),
    path('stats', views.stats, name='stats'),
    path('mark_puzzle_solved', views.mark_puzzle_solved, name='mark_puzzle_solved'),
    path('archive', views.play_archived_puzzle, name='archive'),
    path('play/<date>', views.play, name='play'),
]
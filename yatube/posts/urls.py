from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.post_create, name='post_create'),
    path('follow/', views.follow_index, name='follow_index'),
    path('group/create/', views.group_create, name='group_create'),
    path('group/<slug:slug>/', views.group_posts, name='group_list'),
    path('group/<slug:slug>/delete', views.group_delete, name='group_delete'),
    path('group/<slug:slug>/edit', views.group_edit, name='group_edit'),
    path('groups/', views.groups, name='groups'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/delete', views.post_delete, name='post_delete'),
    path(
        'posts/<int:post_id>/comment/',
        views.add_comment,
        name='add_comment'
    ),
    path('posts/<post_id>/edit/', views.post_edit, name='post_edit'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path(
        'profile/<str:username>/follow/',
        views.profile_follow,
        name='profile_follow'
    ),
    path(
        'profile/<str:username>/unfollow/',
        views.profile_unfollow,
        name='profile_unfollow'
    ),
]

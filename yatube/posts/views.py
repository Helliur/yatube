from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from yatube.settings import CACHE_TIME

from .forms import CommentForm, GroupForm, PostForm
from .models import Follow, Group, Post, User
from .utils import paginator

SHOW_COUNT: int = 10


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    posts = Post.objects.filter(
        author__following__user=request.user
    )
    page_obj = paginator(posts, SHOW_COUNT, request)
    context = {
        'page_obj': page_obj,
        'index_header': True
    }
    return render(request, 'posts/follow.html', context)


@login_required
def group_create(request):
    form = GroupForm(
        request.POST or None,
    )
    context = {
        'form': form,
        'group_create': True
    }
    if not form.is_valid():
        return render(request, 'posts/create_group.html', context)
    group = form.save(commit=False)
    group.author = request.user
    group.save()
    return redirect('posts:groups')


@login_required
def group_edit(request, slug):
    group = get_object_or_404(Group, slug=slug)
    form = GroupForm(
        request.POST or None,
        instance=group,
    )
    context = {
        'form': form,
        'is_edit': True,
        'group': group,
    }
    if not form.is_valid():
        return render(request, 'posts/create_group.html', context)

    group = form.save(commit=True)
    return redirect('posts:groups')


@login_required
def group_delete(request, slug):
    group = get_object_or_404(Group, slug=slug)
    group.delete()
    return redirect('posts:groups')


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    page_obj = paginator(posts, SHOW_COUNT, request)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def groups(request):
    groups = Group.objects.all
    context = {
        'groups': groups,
        'groups_page': True
    }
    return render(request, 'posts/groups.html', context)


@cache_page(CACHE_TIME, key_prefix='index_page')
def index(request):
    posts = Post.objects.all()
    page_obj = paginator(posts, SHOW_COUNT, request)
    context = {
        'page_obj': page_obj,
        'index_header': True,
        'index': True
    }
    return render(request, 'posts/index.html', context)


@login_required
def post_create(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None
    )
    context = {
        'form': form,
        'post_create': True
    }
    if not form.is_valid():
        return render(request, 'posts/create_post.html', context)
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('posts:profile', request.user.username)


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author.username == request.user.username:
        post.delete()
    return redirect('posts:profile', request.user.username)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('created')
    count = post.author.posts.count()
    form = CommentForm(
        request.POST or None
    )
    context = {
        'comments': comments,
        'count': count,
        'form': form,
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('posts:profile', request.user.username)

    form = PostForm(
        request.POST or None,
        instance=post,
        files=request.FILES or None
    )
    context = {
        'form': form,
        'is_edit': True,
        'post': post,
    }
    if not form.is_valid():
        return render(request, 'posts/create_post.html', context)

    post = form.save(commit=True)
    return redirect('posts:post_detail', post.id)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    page_obj = paginator(posts, SHOW_COUNT, request)
    count = posts.count()
    following = author.following.filter(user=request.user.id).exists()
    context = {
        'author': author,
        'count': count,
        'following': following,
        'page_obj': page_obj,
        'profile': True
    }
    return render(request, 'posts/profile.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    following = request.user.follower.filter(author=author).exists()
    if request.user != author and not following:
        follow = Follow(user=request.user, author=author)
        follow.save()
    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request, username):
    follow = Follow.objects.filter(
        user=request.user,
        author=get_object_or_404(User, username=username)
    )
    follow.delete()
    return redirect('posts:profile', username)

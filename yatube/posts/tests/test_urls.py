from http import HTTPStatus

from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Follow, Group, Post, User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author_client = Client()
        cls.user_author = User.objects.create_user(username="HasNoName")
        cls.user_no_author = User.objects.create_user(username="NoAuthor")
        cls.group = Group.objects.create(
            description="Тестовое описание",
            slug="slug",
            title="Тестовое название"
        )
        cls.post = Post.objects.create(
            author=cls.user_author,
            text="Тестовый текст",
            group=cls.group
        )
        cls.author = Client()
        cls.author.force_login(cls.user_author)
        cls.no_author = Client()
        cls.no_author.force_login(cls.user_no_author)

    def SetUp(self):
        cache.clear()

    def test_create_url_exists_at_desired_location(self):
        """Страница /create/ доступна авторизованному пользователю."""
        response = self.author.get(reverse('posts:post_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_group_url_exists_at_desired_location(self):
        """Страница /group/<slug:slug>/ доступна любому пользователю."""
        response = self.client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': f'{self.group.slug}'}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_guest_post_edit_redirect(self):
        """Проверка редиректа неавторизованного пользователя при попытке
        открыть страницу редактированяи поста
        """
        response = self.client.get(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': f'{self.post.id}'}
            ),
            follow=True
        )
        redirect_address = (
            f'{reverse("users:login")}'
            '?next='
            f'{reverse("posts:post_edit",kwargs={"post_id": self.post.id})}'
        )
        self.assertRedirects(response, redirect_address)

    def test_guest_user_comment_redirect(self):
        response = self.client.get(
            reverse(
                'posts:add_comment',
                kwargs={'post_id': f'{self.post.id}'},
            ),
            follow=True
        )
        redirect_address = (
            f'{reverse("users:login")}'
            '?next='
            f'{reverse("posts:add_comment",kwargs={"post_id": self.post.id})}'
        )
        self.assertRedirects(response, redirect_address)

    def test_home_url_exists_at_desired_location(self):
        """Страница / доступна любому пользователю."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_index_page_cache(self):
        """Кэширование index страницы"""
        post_to_delete = Post.objects.create(
            author=self.user_author,
            text="Тестовый текст",
        )
        cache.clear()
        response = self.client.get(reverse('posts:index'))
        post_to_delete.delete()
        cached_response = self.client.get(reverse('posts:index'))
        cache.clear()
        cache_cleared_response = self.client.get(reverse('posts:index'))
        self.assertEqual(response.content, cached_response.content)
        self.assertNotEqual(response.content, cache_cleared_response.content)

    def test_new_post_followed_author_on_follow_page(self):
        """Пост появляется в ленте у пользователя,
        подписавшегося на автора
        """
        response = self.no_author.get(
            reverse('posts:follow_index')
        )
        self.assertFalse(len(response.context['page_obj']))
        Follow.objects.create(
            user=self.user_no_author,
            author=self.user_author
        )
        response = self.no_author.get(
            reverse('posts:follow_index')
        )
        self.assertTrue(len(response.context['page_obj']))

    def test_no_author_post_edit_redirect(self):
        """Проверка редиректа не автора поста при попытке
        открыть страницу редактирования чужого поста"""
        response = self.no_author.get(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': f'{self.post.id}'}
            ),
            follow=True
        )
        redirect_address = reverse(
            'posts:profile',
            kwargs={'username': f'{self.user_no_author.username}'}
        )
        self.assertRedirects(response, redirect_address)

    def test_no_new_post_unfollowed_author_on_follow_page(self):
        """Пост не появляется в ленте у пользователя,
        не подписавшегося на автора
        """
        response = self.author.get(
            reverse('posts:follow_index')
        )
        self.assertFalse(len(response.context['page_obj']))
        Follow.objects.create(
            user=self.user_no_author,
            author=self.user_author
        )
        response = self.author.get(
            reverse('posts:follow_index')
        )
        self.assertFalse(len(response.context['page_obj']))

    def test_post_detail_url_exists_at_desired_location(self):
        """Страница /posts/<int:post_id>/ доступна любому пользователю."""
        response = self.client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': f'{self.post.id}'}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_url_exists_at_desired_location_authorized(self):
        """Страница /posts/<post_id>/edit/ доступна авторизованному
        пользователю."""
        response = self.author.get(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': f'{self.post.id}'}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_url_exists_at_desired_location(self):
        """Страница /profile/<str:username>/ доступна любому пользователю."""
        response = self.client.get(
            reverse(
                'posts:profile',
                kwargs={'username': f'{self.user_author.username}'}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unexising_page_url(self):
        """Переход на несуществующую страницу выдаст ошибку 404"""
        response = self.author.get('unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_user_can_subscribe(self):
        """Авторизованный пользователь может подписываться на автора"""
        response = self.no_author.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': f'{self.user_author.username}'}
            )
        )
        redirect_address = reverse(
            'posts:profile',
            kwargs={'username': f'{self.user_author.username}'}
        )
        self.assertRedirects(response, redirect_address)
        self.assertTrue(
            Follow.objects.filter(
                user=self.user_no_author,
                author=self.user_author
            ).exists()
        )

    def test_user_can_unsubscribe(self):
        """Авторизованный пользователь может отписываться на автора"""
        Follow.objects.create(
            user=self.user_no_author,
            author=self.user_author
        )
        response = self.no_author.get(
            reverse(
                'posts:profile_unfollow',
                kwargs={'username': f'{self.user_author.username}'}
            )
        )
        redirect_address = reverse(
            'posts:profile',
            kwargs={'username': f'{self.user_author.username}'}
        )
        self.assertRedirects(response, redirect_address)
        self.assertFalse(
            Follow.objects.filter(
                user=self.user_no_author,
                author=self.user_author
            ).exists()
        )

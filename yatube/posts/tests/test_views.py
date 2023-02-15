import shutil
import tempfile

from django import forms
from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from posts.models import Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="User1")
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.uploaded_file_path = 'posts/small.gif'
        cls.group = Group.objects.create(
            description="Test",
            slug="slug",
            title="Group"
        )
        cls.post = Post.objects.create(
            text='Post',
            author=cls.user,
            group=cls.group,
            image=cls.uploaded
        )

    def SetUp(self):
        cache.clear()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_pages_show_correct_context(self):
        """Index, group_list и profile сформированы с правильным контекстом"""
        adresses = (
            reverse('posts:index'),
            reverse(
                'posts:group_list',
                kwargs={'slug': f'{self.group.slug}'}
            ),
            reverse(
                'posts:profile',
                kwargs={'username': f'{self.user.username}'}
            ),
            reverse(
                'posts:post_detail',
                kwargs={'post_id': f'{self.post.id}'}
            )
        )
        for address in adresses:
            cache.clear()
            response = self.authorized_client.get(address)
            first_object = (
                response.context.get('post')
                or response.context['page_obj'][0]
            )
            self.assertEqual(first_object.text, self.post.text),
            self.assertEqual(first_object.author.username, self.user.username),
            self.assertEqual(first_object.group.title, self.group.title),
            self.assertEqual(first_object.image.name, self.uploaded_file_path),

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': f'{self.group.slug}'}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': f'{self.user.username}'}
            ): 'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': f'{self.post.id}'}
            ): 'posts/post_detail.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': f'{self.post.id}'}
            ): 'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_create_page_show_correct_context(self):
        """Post_create и post_edit сформированы с правильным контекстом."""
        url_names = (
            reverse('posts:post_create'),
            reverse(
                'posts:post_edit',
                kwargs={'post_id': f'{self.post.id}'}
            )
        )
        for url in url_names:
            response = self.authorized_client.get(url)
            form_fields = {
                'text': forms.fields.CharField,
                'group': forms.fields.ChoiceField,
                'image': forms.fields.ImageField
            }
            for value, expected in form_fields.items():
                with self.subTest(value=value):
                    form_field = response.context.get('form').fields.get(value)
                    self.assertIsInstance(form_field, expected)


class PaginatorViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="User")
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
            description="Test",
            slug="slug2",
            title="Group2"
        )
        cls.posts = [
            Post(
                author=cls.user,
                group=cls.group,
                text='Post' + str(i),
            ) for i in range(13)
        ]
        Post.objects.bulk_create(cls.posts)

    # Проверка паджинатора главной страницы
    def test_first_index_page_contains_ten_records(self):
        cache.clear()
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_index_page_contains_three_records(self):
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    # Проверка паджинатора страницы группы
    def test_first_group_list_page_contains_ten_records(self):
        response = self.client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': f'{self.group.slug}'}
            )
        )
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_group_list_page_contains_three_records(self):
        response = self.client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': f'{self.group.slug}'}
            ) + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), 3)

    # Проверка паджинатора страницы пользователя
    def test_first_profile_page_contains_ten_records(self):
        response = self.client.get(
            reverse(
                'posts:profile',
                kwargs={'username': f'{self.user.username}'}
            )
        )
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_profile_page_contains_three_records(self):
        response = self.client.get(
            reverse(
                'posts:profile',
                kwargs={'username': f'{self.user.username}'}
            ) + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), 3)

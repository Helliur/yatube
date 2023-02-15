from django.test import TestCase
from posts.models import Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост для теста',
        )

    def test_group_have_correct_help_text(self):
        """help_text в полях модели Group совпадает с ожидаемым."""
        group = self.group
        help_texts = {
            'description': 'Описание группы',
            'slug': 'Короткий адрес группы',
            'title': 'Название группы'
        }
        for field, expected_value in help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).help_text, expected_value)

    def test_group_have_correct_object_names(self):
        """Проверяем, что у модели Group корректно работает __str__."""

        str_group = PostModelTest.group
        expected_object_name = str_group.title
        self.assertEqual(expected_object_name, self.group.title)

    def test_group_have_correct_verbose_name(self):
        """Проверяем содержание verbose_name у полей модели Group"""

        group = self.group
        verbose_names = {
            'description': 'Описание группы',
            'slug': 'Короткий адрес группы',
            'title': 'Название группы',
        }
        for field, expected_value in verbose_names.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).verbose_name, expected_value)

    def test_post_have_correct_help_text(self):
        """help_text в полях модели Post совпадает с ожидаемым."""
        post = self.post
        help_texts = {
            'author': 'Автор поста',
            'group': 'Группа, к которой будет относиться пост',
            'pub_date': 'Дата публикации поста',
            'text': 'Введите текст поста',
        }
        for field, expected_value in help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value)

    def test_post_have_correct_object_names(self):
        """Проверяем, что у модели Post корректно работает __str__."""

        str_post = PostModelTest.post
        expected_object_name = str_post.text[:15]
        self.assertEqual(expected_object_name, self.post.text[:15])

    def test_post_have_correct_verbose_name(self):
        """Проверяем содержание verbose_name у полей модели Post"""

        post = self.post
        verbose_names = {
            'author': 'Автор поста',
            'group': 'Группа',
            'pub_date': 'Дата публикации поста',
            'text': 'Текст поста'
        }
        for field, expected_value in verbose_names.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)

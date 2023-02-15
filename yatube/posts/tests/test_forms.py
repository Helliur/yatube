import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from posts.forms import PostForm
from posts.models import Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="User")
        cls.post = Post.objects.create(
            text='text',
            author=cls.user
        )
        cls.form = PostForm()
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

    def setUp(self):
        self.uploaded = SimpleUploadedFile(
            name='small_1.gif',
            content=self.small_gif,
            content_type='image/gif'
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_add_comment(self):
        """Валидная форма добавляет коммент к посту."""
        comments_count = self.post.comments.count()
        form_data = {
            'text': 'text',
        }
        response = self.authorized_client.post(
            reverse(
                'posts:add_comment', kwargs={'post_id': f'{self.post.id}'}
            ),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail', kwargs={'post_id': f'{self.post.id}'}
            )
        )
        self.assertTrue(
            self.post.comments.filter(
                author=self.user,
                text=form_data['text']
            ).exists()
        )
        self.assertEqual(self.post.comments.count(), comments_count + 1)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'image': self.uploaded,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse(
                'posts:profile', kwargs={'username': f'{self.user.username}'}
            )
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text=form_data['text'],
                author=self.user,
                image=f'posts/{self.uploaded.name}',
            ).exists()
        )

    def test_edit_post(self):
        """Валидная форма редактирует запись в Post."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'text edited',
            'image': self.uploaded
        }
        response = self.authorized_client.post(
            reverse(
                'posts:post_edit', args={self.post.id}
            ),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail', kwargs={'post_id': f'{self.post.id}'}
            )
        )
        self.assertEqual(
            form_data['text'],
            Post.objects.get(id=self.post.id).text
        ),
        self.assertTrue(
            Post.objects.get(id=self.post.id).image
        ),
        self.assertEqual(Post.objects.count(), posts_count)

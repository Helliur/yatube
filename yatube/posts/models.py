from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    description = models.TextField(
        verbose_name='Описание группы',
        help_text='Описание группы',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Короткий адрес группы',
        help_text='Короткий адрес группы'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название группы',
        help_text='Название группы'
    )

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    author = models.ForeignKey(
        User,
        help_text='Автор поста',
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор поста',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        help_text='Группа, к которой будет относиться пост',
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
    )
    image = models.ImageField(
        'Картинка',
        blank=True,
        upload_to='posts/',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text='Дата публикации поста',
        verbose_name='Дата публикации поста',
    )
    text = models.TextField(
        help_text='Введите текст поста',
        verbose_name='Текст поста',
    )

    def __str__(self) -> str:
        return self.text[:15]

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text='Дата публикации комментария',
        verbose_name='Дата публикации комментария',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(
        help_text='Введите текст комментария',
        verbose_name='Текст комментария',
    )


class Follow(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

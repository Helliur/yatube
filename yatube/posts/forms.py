from django import forms

from .models import Comment, Group, Post


class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = (
            'text',
        )


class GroupForm(forms.ModelForm):
    class Meta():
        model = Group
        fields = (
            'title',
            'description',
            'slug',
        )


class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = (
            'text',
            'group',
            'image'
        )
        help_texts = {
            "group": {
                "edit": "Группа, к которой относится пост",
                "new": "Группа, к которой будет относиться пост",
            },
            "text": {
                "edit": "Текст поста",
                "new": "Текст нового поста",
            },
        }

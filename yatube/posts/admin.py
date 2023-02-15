from django.contrib import admin

from .models import Comment, Group, Post


class CommentAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
    list_display = (
        'post',
        'author',
        'text',
        'created'
    )
    search_fields = ('author', 'text')


class GroupAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
    list_display = (
        'title',
        'slug',
        'description'
    )
    search_fields = ('title',)


class PostAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group'
    )
    list_editable = ('group',)
    list_filter = (
        'pub_date',
        'group',
    )
    search_fields = ('text',)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Post, PostAdmin)

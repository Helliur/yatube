# Generated by Django 2.2.16 on 2022-09-05 08:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20220905_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='author',
            field=models.ForeignKey(help_text='Автор группы', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор группы'),
        ),
    ]
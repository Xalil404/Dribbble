# Generated by Django 4.2.16 on 2024-09-30 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0021_comment_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='name',
        ),
    ]
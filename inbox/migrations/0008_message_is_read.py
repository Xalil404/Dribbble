# Generated by Django 4.2.16 on 2024-09-25 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inbox', '0007_rename_body_message_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 4.2.16 on 2024-09-19 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_profile_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
    ]
# Generated by Django 4.2.1 on 2023-05-07 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_user_follows_userfollows_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
    ]

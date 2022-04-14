# Generated by Django 2.2.16 on 2022-04-14 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220414_0532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('moderator', 'Moderator'), ('admin', 'Administrator'), ('superuser', 'Superuser')], default='user', max_length=16),
        ),
    ]

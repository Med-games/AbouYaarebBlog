# Generated by Django 4.2.9 on 2024-01-23 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_video_delete_videos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='email',
        ),
    ]

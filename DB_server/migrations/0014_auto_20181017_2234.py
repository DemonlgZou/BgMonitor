# Generated by Django 2.1.1 on 2018-10-17 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DB_server', '0013_video_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='end_at',
            field=models.DateTimeField(null=True, verbose_name='视频结束时间'),
        ),
        migrations.AlterField(
            model_name='video',
            name='start_at',
            field=models.DateTimeField(null=True, verbose_name='视频开始时间'),
        ),
    ]

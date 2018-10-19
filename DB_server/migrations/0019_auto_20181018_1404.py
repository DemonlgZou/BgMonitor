# Generated by Django 2.1.1 on 2018-10-18 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DB_server', '0018_video_create_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='stat',
            field=models.CharField(choices=[('generating', '生成中'), ('created', '生成完毕'), ('null', '没有报告')], max_length=256, verbose_name='视频状态'),
        ),
    ]

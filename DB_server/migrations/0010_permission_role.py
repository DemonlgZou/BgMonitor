# Generated by Django 2.1.1 on 2018-10-17 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DB_server', '0009_auto_20181016_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=None, related_name='role', to='DB_server.Role', verbose_name='权限信息'),
        ),
    ]

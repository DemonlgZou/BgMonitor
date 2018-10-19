# Generated by Django 2.1.1 on 2018-10-17 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DB_server', '0014_auto_20181017_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='host',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='video', to='DB_server.Host'),
        ),
        migrations.AlterField(
            model_name='video',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='video', to='DB_server.Staff'),
        ),
    ]
# Generated by Django 3.2.4 on 2021-07-08 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='telegram_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='vk_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

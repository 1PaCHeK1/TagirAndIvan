# Generated by Django 3.2.4 on 2021-07-08 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=256)),
                ('telegram_id', models.IntegerField(blank=True)),
                ('vk_id', models.IntegerField(blank=True)),
            ],
        ),
    ]
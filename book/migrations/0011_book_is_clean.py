# Generated by Django 3.2.12 on 2023-10-10 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0010_auto_20231001_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_clean',
            field=models.BooleanField(default=False, verbose_name='整備されたデータ判定'),
        ),
    ]

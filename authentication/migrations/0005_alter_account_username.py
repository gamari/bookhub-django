# Generated by Django 3.2.12 on 2023-10-11 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20231001_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(default='noname', max_length=12, unique=True),
        ),
    ]

# Generated by Django 3.2.12 on 2023-10-29 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selection', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookselection',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
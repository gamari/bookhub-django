# Generated by Django 3.2.12 on 2023-11-05 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='description',
        ),
        migrations.AddField(
            model_name='note',
            name='content',
            field=models.TextField(blank=True, max_length=10000, null=True),
        ),
    ]

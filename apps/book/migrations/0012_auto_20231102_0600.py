# Generated by Django 3.2.12 on 2023-11-02 06:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0011_auto_20231102_0513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='tags',
        ),
        migrations.DeleteModel(
            name='BookTag',
        ),
    ]

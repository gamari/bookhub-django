# Generated by Django 3.2.12 on 2023-09-30 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_alter_bookshelf_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='出版社'),
        ),
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='書籍説明'),
        ),
        migrations.AlterField(
            model_name='book',
            name='published_date',
            field=models.DateField(blank=True, null=True, verbose_name='出版日'),
        ),
        migrations.AlterField(
            model_name='book',
            name='thumbnail',
            field=models.URLField(blank=True, null=True, verbose_name='サムネイル'),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=255, verbose_name='書籍名'),
        ),
    ]
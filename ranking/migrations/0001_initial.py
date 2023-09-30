# Generated by Django 3.2.12 on 2023-09-30 16:11

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0008_bookshelf_books'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeeklyRanking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyRankingEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_count', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.book')),
                ('ranking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='ranking.weeklyranking')),
            ],
            options={
                'ordering': ['-added_count'],
            },
        ),
    ]

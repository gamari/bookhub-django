# Generated by Django 3.2.12 on 2023-10-14 09:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0012_auto_20231013_1811'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookSelection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, null=True, verbose_name='セレクション説明')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('books', models.ManyToManyField(related_name='in_selections', to='book.Book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selections', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 3.0.7 on 2020-07-28 14:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0002_auto_20200728_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='art_post', to=settings.AUTH_USER_MODEL),
        ),
    ]
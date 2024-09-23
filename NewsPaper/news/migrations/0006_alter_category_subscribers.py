# Generated by Django 5.1 on 2024-09-18 01:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_subscriberscategory_category_subscribers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(blank=True, null=True, related_name='category', through='news.SubscribersCategory', to=settings.AUTH_USER_MODEL),
        ),
    ]

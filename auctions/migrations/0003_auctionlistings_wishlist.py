# Generated by Django 3.2.3 on 2021-06-14 01:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlistings'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlistings',
            name='wishlist',
            field=models.ManyToManyField(blank=True, related_name='item', to=settings.AUTH_USER_MODEL),
        ),
    ]

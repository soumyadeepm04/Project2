# Generated by Django 3.2.3 on 2021-06-14 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20210614_1809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='item',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='item',
            field=models.ManyToManyField(null=True, to='auctions.AuctionListings'),
        ),
    ]

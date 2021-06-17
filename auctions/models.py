from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    starting_bid = models.IntegerField()
    urls = models.URLField(null=True, blank=True)
    price = models.IntegerField(null = True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    open = models.CharField(max_length = 10, null = True, editable=False)
    category = models.CharField(max_length = 100, null = True, blank= True)

    class Meta:
        verbose_name_plural = 'Auction Listings'
# Square var1 = new Square() -- valid
# Rectangle var2 = var1  
# (Square)var2.property_of_Square

# Rectangle var1 = new Rectangle() -- invalid
# Square var2 = var1

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    item = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, null = True, related_name="item")

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    bid = models.IntegerField()

class Comments(models.Model):
    item = models.ForeignKey(AuctionListings, on_delete = models.CASCADE, null = True)
    comment = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Comments'
from auctions.models import AuctionListings, User
from django.contrib import admin
from .models import Bid, Comments, User, AuctionListings
# Register your models here.
admin.site.register(User)
admin.site.register(AuctionListings)
admin.site.register(Comments)
admin.site.register(Bid)
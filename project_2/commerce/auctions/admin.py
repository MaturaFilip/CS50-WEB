from django.contrib import admin
from .models import Auction, Bid, Comment
# Register your models here.

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "author", "body", "start_bid", "created", "status"]
    list_filter = ["status", "created", "author"]
    date_hierarchy = "created"
    ordering = ["status", "created"]


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ["id", "auction", "bidder", "amount", "created"]
    date_hierarchy = "created"
    ordering = ["created"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "auction", "user_name", "comment_name", "body", "created"]
    date_hierarchy = "created"
    ordering = ["created"]



from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


# query manager to show only ACTIVE auctions -> can simplify queries
class ActiveManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Auction.Status.ACTIVE)
        )

# Auction model
class Auction(models.Model):

    # active and inactive auction
    # enums used
    class Status(models.TextChoices):
        ACTIVE = 'AC', 'Active'
        INACTIVE = 'IN', 'Inactive'

    title = models.CharField(max_length=250)

    # author of the auction
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name = "user_auctions"
    )
    body = models.TextField()
    figure_url = models.CharField(max_length=250, null=True)
    start_bid = models.PositiveIntegerField()
    # created / updated
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # active vs inactive
    status = models.CharField(
        max_length = 2,
        choices = Status,
        default=Status.ACTIVE,
    )

    # TODO add tags:

    # metadata
    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    # query managers
    objects = models.Manager()
    active = ActiveManager()

    # TODO Define canonical URL (to use auction.get_absolute)

    def __str__(self):
        return self.title
    
#######
#BIDS##
#######
class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete = models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name = "user_bids"
    )
    # Validation form need to be added t forms.py
    amount = models.PositiveBigIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return f"Auction: {self.auction}; Bidder: {self.bidder}; {self.amount} $"


##############
###COMMENTS###
##############
class Comment(models.Model):
    auction = models.ForeignKey(
        # related_name => we can use auction.comments.all()
        # it shows all the comment for given auction
        Auction, on_delete=models.CASCADE, related_name="comments"
    )

    user_name = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name = "user_comment"
    )

    comment_name = models.CharField(max_length=80)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
    
    def __str__(self):
        return f"Comment by {self.user_name} on {self.auction}"
    
#############
#USER EXTEND#
#############
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
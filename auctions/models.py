from django.db.models import ForeignKey, CharField, IntegerField, BooleanField, DateTimeField, CASCADE, Model
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class User(AbstractUser):
    def __str__(self):
        return f'User: {self.username}'


class Category(Model):
    name = CharField(max_length=64)

    def __str__(self):
        return f'Category: {self.name}'


class Auction(Model):
    user = ForeignKey(User, CASCADE, related_name='auctions')
    date = DateTimeField(auto_now_add=True)
    title = CharField(max_length=128)
    description = CharField(max_length=1080)
    price = IntegerField()
    image = CharField(max_length=512)
    category = ForeignKey(Category, CASCADE,
                          blank=True, null=True, related_name='auctions')
    closed = BooleanField(default=False)

    def __str__(self):
        return f'Auction: {self.title} by {self.user}'


class Bid(Model):
    user = ForeignKey(User, CASCADE, related_name='bids')
    auction = ForeignKey(Auction, CASCADE, related_name='bids')
    bid = IntegerField()
    won = BooleanField(default=False)

    def __str__(self):
        return f'Bid: {self.bid} by {self.user} to {self.auction}'


class Comment(Model):
    user = ForeignKey(User, CASCADE, related_name='comments')
    auction = ForeignKey(Auction, CASCADE, related_name='comments')
    comment = CharField(max_length=256)
    date = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment: {self.comment}, {self.user}'


class Whitelist(Model):
    user = ForeignKey(User, CASCADE, related_name='whitelist')
    auction = ForeignKey(Auction, CASCADE, related_name='whitelist')

    def __str__(self):
        return f'Whitelist: {self.user}, {self.auction}'

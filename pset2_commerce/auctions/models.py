from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listings", blank=True, related_name="watchers")

    def __str__(self):
        return f"{self.username}"


class Listings(models.Model):
    class Categories(models.TextChoices):
        AUTO = "Auto Parts"
        CLOTHING = "Clothing, Shoes, Accessories"
        SPORTING = "Sporting Goods"
        TOYS = "Toys"
        HOBBIES = "Hobbies"
        HOME = "Home and Garden"
        JEWELRY = "Jewelry and Watches"
        HEALTH = "Health and Beauty"
        INDUSTRIAL = "Industrial"
        PET = "Pet Supplies"
        BABY = "Baby Essentials"
        ELECTRONICS = "Electronics"
        COLLECTIBLES = "Collectibles and Art"
        MEDIA = "Books, Movies, Music"

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    listed_by = models.ForeignKey(User, related_name='listings_listed_by', on_delete=models.CASCADE)
    list_price = models.DecimalField(max_digits=11, decimal_places=2)
    category = models.CharField(max_length=28, choices=Categories.choices, null=True, blank=True)
    date_listed = models.DateTimeField(auto_now_add=True)
    highest_bid = models.ForeignKey("Bids", on_delete=models.CASCADE, null=True, blank=True)
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, related_name='listings_winner', default=None,
                               null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Title: {self.title}, seller: {self.listed_by}"


class Bids(models.Model):
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Amount: {self.amount}, Listing: {self.listing}, Bidder: {self.bidder}"


class Comments(models.Model):
    text = models.TextField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

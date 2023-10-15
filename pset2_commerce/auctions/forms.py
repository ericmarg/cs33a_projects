from django.forms import ModelForm
from .models import *


class ListingForm(ModelForm):
    class Meta:
        model = Listings
        fields = ["title", "description", "list_price", "category", "image_url"]


class BidForm(ModelForm):
    class Meta:
        model = Bids
        fields = ["amount"]


class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ["text"]

# Generated by Django 4.2.5 on 2023-10-12 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0002_remove_listings_bids_count"),
    ]

    operations = [
        migrations.AddField(
            model_name="listings",
            name="image_url",
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name="listings",
            name="category",
            field=models.CharField(
                blank=True,
                choices=[
                    ("AUT", "Auto Parts"),
                    ("CLO", "Clothing, Shoes, Accessories"),
                    ("SPO", "Sporting Goods"),
                    ("TOY", "Toys"),
                    ("HOB", "Hobbies"),
                    ("HOM", "Home and Garden"),
                    ("JEW", "Jewelry and Watches"),
                    ("HEA", "Health and Beauty"),
                    ("IND", "Industrial"),
                    ("PET", "Pet Supplies"),
                    ("BAB", "Baby Essentials"),
                    ("ELE", "Electronics"),
                    ("COL", "Collectibles and Art"),
                    ("MED", "Books, Movies, Music"),
                ],
                max_length=3,
            ),
        ),
    ]

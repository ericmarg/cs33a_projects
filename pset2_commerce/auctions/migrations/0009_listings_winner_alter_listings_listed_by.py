# Generated by Django 4.2.5 on 2023-10-13 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0008_comments_listing"),
    ]

    operations = [
        migrations.AddField(
            model_name="listings",
            name="winner",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="listings_winner",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="listings",
            name="listed_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="listings_listed_by",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

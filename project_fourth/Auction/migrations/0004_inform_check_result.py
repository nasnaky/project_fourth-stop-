# Generated by Django 4.0.5 on 2022-08-10 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auction', '0003_auction_check_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='inform',
            name='check_result',
            field=models.BooleanField(default=False),
        ),
    ]

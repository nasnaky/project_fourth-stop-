# Generated by Django 4.0.5 on 2022-08-10 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auction', '0004_inform_check_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarm',
            name='check_see',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 3.1.2 on 2020-10-11 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_bid_won'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='description',
            field=models.CharField(max_length=1080),
        ),
    ]

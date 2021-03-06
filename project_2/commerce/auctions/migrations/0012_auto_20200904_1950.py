# Generated by Django 3.1 on 2020-09-04 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auctions_buyer'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctions',
            name='buy_price',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='auctions',
            name='start_bid',
            field=models.DecimalField(decimal_places=2, max_digits=9, null=True),
        ),
    ]

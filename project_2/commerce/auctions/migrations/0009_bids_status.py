# Generated by Django 3.1 on 2020-09-04 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20200903_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='bids',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]

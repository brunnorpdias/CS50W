# Generated by Django 3.1 on 2020-09-03 20:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20200903_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='item',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='item',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item', to='auctions.auctions'),
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='user',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]

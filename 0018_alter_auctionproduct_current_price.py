# Generated by Django 4.2.5 on 2024-02-19 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_auctionproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionproduct',
            name='current_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]

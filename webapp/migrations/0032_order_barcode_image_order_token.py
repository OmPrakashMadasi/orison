# Generated by Django 5.1.5 on 2025-03-04 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0031_alter_order_phone_alter_order_total_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='barcode_image',
            field=models.ImageField(blank=True, null=True, upload_to='barcodes/'),
        ),
        migrations.AddField(
            model_name='order',
            name='token',
            field=models.UUIDField(blank=True, editable=False, null=True, unique=True),
        ),
    ]

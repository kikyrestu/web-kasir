# Generated by Django 5.1.4 on 2024-12-21 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kasir', '0005_alter_transaksidetail_barang'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiptsettings',
            name='printer_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

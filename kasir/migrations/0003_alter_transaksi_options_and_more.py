# Generated by Django 5.1.4 on 2024-12-19 06:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kasir', '0002_remove_produk_stok_minimal_alter_produk_kategori_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaksi',
            options={'verbose_name': 'Transaksi', 'verbose_name_plural': 'Transaksi'},
        ),
        migrations.RenameField(
            model_name='transaksi',
            old_name='dibayar',
            new_name='bayar',
        ),
        migrations.RemoveField(
            model_name='transaksi',
            name='no_invoice',
        ),
        migrations.AddField(
            model_name='transaksi',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='TransaksiDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),
                ('harga', models.DecimalField(decimal_places=2, max_digits=10)),
                ('produk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kasir.produk')),
                ('transaksi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kasir.transaksi')),
            ],
        ),
        migrations.DeleteModel(
            name='DetailTransaksi',
        ),
    ]

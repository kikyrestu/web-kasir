from django.contrib import admin
from .models import Barang, StoreSettings, ReceiptSettings, SystemSettings

# Unregister jika sudah terdaftar
if admin.site.is_registered(Barang):
    admin.site.unregister(Barang)

@admin.register(Barang)
class BarangAdmin(admin.ModelAdmin):
    list_display = [
        'no',
        'nama_barang',
        'kategori',
        'hp_beli',
        'h_jual',
        'stok',
        'total_hp_beli',
        'total_h_jual',
        'tgl_terjual',
        'tgl_stok_masuk'
    ]
    
    list_editable = [
        'nama_barang',
        'kategori',
        'hp_beli',
        'h_jual',
        'stok'
    ]
    
    readonly_fields = ['total_hp_beli', 'total_h_jual']  # Karena dihitung otomatis
    search_fields = ['no', 'nama_barang', 'kategori']
    list_filter = ['kategori', 'tgl_terjual', 'tgl_stok_masuk']
    list_per_page = 25

@admin.register(StoreSettings)
class StoreSettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'updated_at')

@admin.register(ReceiptSettings)
class ReceiptSettingsAdmin(admin.ModelAdmin):
    list_display = ('paper_size', 'show_logo', 'updated_at')

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ('currency', 'timezone', 'low_stock_threshold', 'updated_at')
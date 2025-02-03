from django.db import models
from django.db.models import Sum
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from simple_history.models import HistoricalRecords
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64
from django.utils import timezone
from django.conf import settings

class Barang(models.Model):
    no = models.CharField(max_length=50, primary_key=True)
    nama_barang = models.CharField(max_length=255)
    kategori = models.CharField(max_length=100, blank=True, null=True)
    hp_beli = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    h_jual = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    stok = models.IntegerField(default=0)
    total_hp_beli = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    total_h_jual = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    tgl_terjual = models.DateField(null=True, blank=True)
    tgl_stok_masuk = models.DateField(default=timezone.now)
    barcode = models.CharField(max_length=13, unique=True, null=True, blank=True)
    history = HistoricalRecords()

    def generate_barcode(self):
        if not self.barcode:
            return None
        rv = BytesIO()
        EAN = barcode.get_barcode_class('ean13')
        EAN(str(self.barcode).zfill(13), writer=ImageWriter()).write(rv)
        image_string = base64.b64encode(rv.getvalue()).decode()
        return f'data:image/png;base64,{image_string}'

    def is_stok_menipis(self):
        return self.stok <= self.stok_minimal

    def clean(self):
        if self.hpp > self.h_jual:
            raise ValidationError('HPP tidak boleh lebih besar dari harga jual')

    def save(self, *args, **kwargs):
        self.clean()
        self.total_hp_beli = self.hp_beli * self.stok
        self.total_h_jual = self.h_jual * self.stok
        super().save(*args, **kwargs)

    def profit_per_item(self):
        return self.h_jual - self.hpp

    def total_profit(self):
        return self.profit_per_item() * self.stok

    def __str__(self):
        return f"{self.no} - {self.nama_barang}"

    def kurangi_stok(self, jumlah):
        if self.stok >= jumlah:
            self.stok -= jumlah
            self.stok_keluar += jumlah
            self.save()
            return True
        return False

    class Meta:
        verbose_name_plural = "Barang"

# Resource untuk import/export Excel
class BarangResource(resources.ModelResource):
    class Meta:
        model = Barang
        import_id_fields = ['no']
        fields = ('no', 'nama_barang', 'kategori', 'hpp', 'h_jual', 
                 'stok', 'hb_beli', 'hb_jual', 'tgl_terjual', 'tgl_stok_masuk')

# Views untuk grafik
from django.db.models.functions import TruncDate
from django.db.models import Count

def get_penjualan_chart_data():
    return (Barang.objects
            .filter(tgl_terjual__isnull=False)
            .annotate(tanggal=TruncDate('tgl_terjual'))
            .values('tanggal')
            .annotate(total=Count('id'))
            .order_by('tanggal'))

# Admin
@admin.register(Barang)
class BarangAdmin(ImportExportModelAdmin):
    resource_class = BarangResource
    list_display = ('no', 'nama_barang', 'kategori', 'hpp', 'h_jual', 
                   'stok', 'stok_minimal', 'barcode_image', 'status_stok')
    list_editable = ('nama_barang', 'kategori', 'hpp', 'h_jual', 
                    'stok', 'stok_minimal', 'barcode')
    list_filter = ('kategori', 'tgl_terjual', 'tgl_stok_masuk')
    search_fields = ('nama_barang', 'kategori', 'barcode')
    ordering = ('no',)
    change_list_template = 'admin/kasir/barang/change_list.html'

    def barcode_image(self, obj):
        if obj.generate_barcode():
            return mark_safe(f'<img src="{obj.generate_barcode()}" height="50"/>')
        return "No barcode"
    
    def status_stok(self, obj):
        if obj.is_stok_menipis():
            return mark_safe('<span style="color: red;">Stok Menipis!</span>')
        return "Normal"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        
        metrics = {
            'total_barang': qs.count(),
            'total_stok': qs.aggregate(Sum('stok'))['stok__sum'],
            'stok_menipis': qs.filter(stok__lte=models.F('stok_minimal')).count(),
            'penjualan_chart': get_penjualan_chart_data(),
        }
        
        response.context_data['summary'] = metrics
        return response

class Kategori(models.Model):
    nama = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'kasir_kategori'
        
    def __str__(self):
        return self.nama

class Produk(models.Model):
    id = models.AutoField(primary_key=True)
    no = models.CharField(max_length=50, unique=True, default='AUTO')
    kode_barang = models.CharField(max_length=10, unique=True, blank=True, null=True)
    nama_barang = models.CharField(max_length=255)
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True)
    hp_beli = models.DecimalField(max_digits=10, decimal_places=2)
    h_jual = models.DecimalField(max_digits=10, decimal_places=2)
    stok = models.IntegerField(default=0)
    tgl_terjual = models.DateTimeField(null=True, blank=True)
    tgl_stok_masuk = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Produk'
        verbose_name_plural = 'Produk'
        
    def __str__(self):
        return self.nama_barang

class Transaksi(models.Model):
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    tanggal = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    bayar = models.DecimalField(max_digits=10, decimal_places=2)
    kembalian = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Transaksi"
        verbose_name_plural = "Transaksi"

    def __str__(self):
        return f"Transaksi #{self.id} - {self.tanggal}"

class TransaksiDetail(models.Model):
    transaksi = models.ForeignKey(Transaksi, on_delete=models.CASCADE)
    produk = models.ForeignKey(
        Produk, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    qty = models.IntegerField()
    harga = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.qty * self.harga

    def get_subtotal(self):
        return self.qty * self.harga

    def __str__(self):
        return f"{self.transaksi.id} - {self.produk.nama_barang if self.produk else 'Deleted'} x {self.qty}"

    class Meta:
        verbose_name = "Detail Transaksi"
        verbose_name_plural = "Detail Transaksi"

# Tambahkan model baru untuk settings
class StoreSettings(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nama Toko")
    address = models.TextField(verbose_name="Alamat")
    phone = models.CharField(max_length=20, verbose_name="Telepon")
    email = models.EmailField(verbose_name="Email")
    logo = models.ImageField(upload_to='store_logo/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pengaturan Toko"
        verbose_name_plural = "Pengaturan Toko"

class ReceiptSettings(models.Model):
    header = models.TextField(verbose_name="Header Struk", blank=True)
    footer = models.TextField(verbose_name="Footer Struk", blank=True)
    paper_size = models.CharField(
        max_length=10,
        choices=[('58mm', '58mm'), ('80mm', '80mm')],
        default='58mm'
    )
    show_logo = models.BooleanField(default=True)
    printer_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pengaturan Struk"
        verbose_name_plural = "Pengaturan Struk"

class SystemSettings(models.Model):
    currency = models.CharField(
        max_length=10,
        choices=[('IDR', 'Rupiah'), ('USD', 'Dollar')],
        default='IDR'
    )
    date_format = models.CharField(
        max_length=20,
        choices=[
            ('DD/MM/YYYY', 'DD/MM/YYYY'),
            ('MM/DD/YYYY', 'MM/DD/YYYY'),
            ('YYYY-MM-DD', 'YYYY-MM-DD')
        ],
        default='DD/MM/YYYY'
    )
    timezone = models.CharField(
        max_length=50,
        choices=[
            ('Asia/Jakarta', 'WIB'),
            ('Asia/Makassar', 'WITA'),
            ('Asia/Jayapura', 'WIT')
        ],
        default='Asia/Jakarta'
    )
    low_stock_threshold = models.IntegerField(default=10)
    enable_email_notifications = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pengaturan Sistem"
        verbose_name_plural = "Pengaturan Sistem"

class Module(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50)
    order = models.IntegerField(default=1)
    template = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    access_admin = models.BooleanField(default=True)
    access_kasir = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class PPOBSaldo(models.Model):
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Saldo PPOB: Rp {self.balance}"

class PPOBSaldoHistory(models.Model):
    TIPE_CHOICES = (
        ('IN', 'Masuk'),
        ('OUT', 'Keluar'),
    )
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_before = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=3, choices=TIPE_CHOICES)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_type_display()} - Rp {self.amount}"

class OperationalExpense(models.Model):
    TIPE_CHOICES = (
        ('IN', 'Pemasukan'),
        ('OUT', 'Pengeluaran'),
    )
    
    tanggal = models.DateField()
    deskripsi = models.TextField()
    jumlah = models.DecimalField(max_digits=10, decimal_places=2)
    tipe = models.CharField(max_length=3, choices=TIPE_CHOICES)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Biaya Operasional"
        verbose_name_plural = "Biaya Operasional"
        ordering = ['-tanggal']

    def __str__(self):
        return f"{self.get_tipe_display()} - {self.deskripsi} - Rp {self.jumlah}"


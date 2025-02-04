from django.urls import path
from . import views

app_name = 'kasir'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('transaksi/', views.transaksi, name='transaksi'),
    path('transaksi/<int:transaction_id>/delete/', views.delete_transaction, name='delete_transaction'),
    path('produk/', views.produk, name='produk'),
    path('laporan/', views.laporan, name='laporan'),
    path('export-excel/', views.export_excel, name='export_excel'),
    path('api/product/<int:product_id>/', views.product_api, name='product_api_detail'),
    path('import-products/', views.import_products, name='import_products'),
    path('download-template/', views.download_template, name='download_template'),
    path('add-product/', views.add_product, name='add_product'),
    path('produk/tambah/', views.tambah_produk, name='tambah_produk'),
    path('add-kategori/', views.add_kategori, name='add_kategori'),
    path('get-kategoris/', views.get_kategoris, name='get_kategoris'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('delete-products-batch/', views.delete_products_batch, name='delete_products_batch'),
    path('product/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('settings/', views.settings, name='settings'),
    path('settings/store/update/', views.update_store_info, name='update_store_info'),
    path('settings/receipt/update/', views.update_receipt_settings, name='update_receipt_settings'),
    path('settings/system/update/', views.update_system_settings, name='update_system_settings'),
    path('settings/backup/', views.backup_data, name='backup_data'),
    path('settings/restore/', views.restore_data, name='restore_data'),
    path('kategori/', views.kategori_produk, name='kategori_produk'),
    path('kategori/add/', views.tambah_kategori, name='tambah_kategori'),
    path('kategori/<int:kategori_id>/update/', views.update_kategori, name='update_kategori'),
    path('import-kategori-from-produk/', views.import_kategori_from_produk, name='import_kategori_from_produk'),
    path('product/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:pk>/', views.get_product, name='get_product'),
    path('kategori/<int:pk>/edit/', views.edit_kategori, name='edit_kategori'),
    path('search-products/', views.search_products, name='search_products'),
    path('process-transaction/', views.process_transaction, name='process_transaction'),
    path('print-receipt/<int:transaksi_id>/', views.print_receipt, name='print_receipt'),
    path('kategori/hapus/', views.hapus_kategori, name='hapus_kategori'),
    path('products/search/', views.search_products, name='search_products'),
    path('laporan/sales-report/', views.get_sales_report, name='get_sales_report'),
    path('laporan/profit-loss/', views.get_profit_loss_report, name='get_profit_loss_report'),
    path('laporan/profit-loss/export/', views.export_profit_loss, name='export_profit_loss'),
    path('laporan/export-stock/', views.export_stock_report, name='export_stock_report'),
    path('get-sales-data/', views.get_sales_data, name='get_sales_data'),
    path('export-sales-report/', views.export_sales_report, name='export_sales_report'),
    path('search-products-transaksi/', views.search_products_transaksi, name='search_products_transaksi'),
    path('test-print/', views.test_print, name='test_print'),
    path('export/stock/excel/', views.export_stock_excel, name='export_stock_excel'),
    path('export/stock/pdf/', views.export_stock_pdf, name='export_stock_pdf'),
    path('laporan/cashflow/pdf/', views.generate_cashflow_pdf, name='generate_cashflow_pdf'),
    path('generate-cashflow-pdf/', views.generate_cashflow_pdf, name='generate_cashflow_pdf'),
    path('module/save/', views.save_module, name='save_module'),
    path('module/get/', views.get_module, name='get_module'),
    path('module/toggle/', views.toggle_module, name='toggle_module'),
    path('ppob/', views.ppob_view, name='ppob'),
    path('settings/module/save/', views.save_module, name='save_module'),
    path('settings/module/get/', views.get_module, name='get_module'),
    path('settings/module/toggle/', views.toggle_module, name='toggle_module'),
    path('<str:module_path>/', views.module_view, name='module'),
    path('ppob/add-saldo/', views.ppob_add_saldo, name='ppob_add_saldo'),
    path('ppob/beli-pulsa/', views.ppob_beli_pulsa, name='ppob_beli_pulsa'),
    path('ppob/beli-paket-data/', views.ppob_beli_paket_data, name='ppob_beli_paket_data'),
    path('ppob/beli-token/', views.ppob_beli_token, name='ppob_beli_token'),
    path('ppob/bayar-pdam/', views.ppob_bayar_pdam, name='ppob_bayar_pdam'),
    path('ppob/tarik-tunai/', views.ppob_tarik_tunai, name='ppob_tarik_tunai'),
    path('ppob/transfer/', views.ppob_transfer, name='ppob_transfer'),
    path('ppob/chart-data/', views.ppob_chart_data, name='ppob_chart_data'),
    path('ppob/today-summary/', views.ppob_today_summary, name='ppob_today_summary'),
    path('ppob/export/', views.ppob_export, name='ppob_export'),
    path('ppob/ewallet/', views.ppob_ewallet, name='ppob_ewallet'),
    path('ppob/get-data/', views.ppob_get_data, name='ppob_get_data'),
    path('settings/backup-database/', views.backup_database, name='backup_database'),
    path('settings/restore-database/', views.restore_database, name='restore_database'),
    path('api/get-profit-loss-report/', views.get_profit_loss_report, name='get_profit_loss_report'),
    path('fix-transactions/', views.fix_transaction_details, name='fix_transactions'),
]

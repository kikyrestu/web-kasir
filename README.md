# Web Kasir

![GitHub repo size](https://img.shields.io/github/repo-size/kikyrestu/web-kasir)
![GitHub stars](https://img.shields.io/github/stars/kikyrestu/web-kasir?style=social)
![GitHub license](https://img.shields.io/github/license/kikyrestu/web-kasir)
![GitHub issues](https://img.shields.io/github/issues/kikyrestu/web-kasir)

Web Kasir adalah sistem kasir berbasis web yang dirancang untuk membantu pengelolaan transaksi di toko atau bisnis kecil dengan fitur yang lengkap dan mudah digunakan.

## 🎯 Fitur Utama
- ✅ Manajemen Produk (Tambah, Edit, Hapus, Stok, Kategori)
- ✅ Manajemen Transaksi (Pencatatan, Edit, Refund)
- ✅ Cetak Struk via Printer Thermal
- ✅ Laporan Penjualan (Harian, Bulanan, Tahunan)
- ✅ Manajemen Pelanggan
- ✅ Multi-user dengan Hak Akses
- ✅ Dashboard Statistik Penjualan
- ✅ Integrasi Barcode Scanner
- ✅ Export Data ke Excel/PDF
- ✅ Notifikasi Stok Menipis

## 📌 Teknologi yang Digunakan
- **Frontend**: HTML, CSS, JavaScript, Vue.js (Opsional)
- **Backend**: Python, Django
- **Database**: PostgreSQL, SQLite (Opsional)
- **Libraries**: Django Rest Framework, Bootstrap, jQuery, Axios
- **Auth & Security**: Django Authentication, JWT
- **Deployment**: Docker, Nginx, Gunicorn

## 🔧 Cara Instalasi

### 1. Clone Repositori
   ```sh
   git clone https://github.com/kikyrestu/web-kasir.git
   ```
### 2. Masuk ke Direktori Proyek
   ```sh
   cd web-kasir
   ```
### 3. Buat Virtual Environment & Install Dependencies
   ```sh
   python -m venv venv
   source venv/bin/activate  # Untuk Linux/Mac
   venv\Scripts\activate  # Untuk Windows
   pip install -r requirements.txt
   ```
### 4. Konfigurasi Environment
   Salin file `.env.example` menjadi `.env` dan sesuaikan konfigurasi database.
   ```sh
   cp .env.example .env
   ```
### 5. Migrasi dan Seeder Database
   ```sh
   python manage.py migrate
   python manage.py loaddata seed_data.json
   ```
### 6. Jalankan Server
   ```sh
   python manage.py runserver
   ```

## 📸 Screenshot Tampilan
![Screenshot](https://ibb.co.com/GfyQwrdx)

## 📜 Dokumentasi API
Untuk integrasi dengan sistem lain, silakan lihat dokumentasi API di [`docs/API.md`](docs/API.md).

## 🤝 Kontribusi
Kami menyambut kontribusi dari siapa saja! Ikuti langkah-langkah berikut untuk berkontribusi:

1. Fork repositori ini
2. Buat branch fitur baru (`git checkout -b fitur-baru`)
3. Commit perubahan (`git commit -m 'Menambahkan fitur baru'`)
4. Push ke branch (`git push origin fitur-baru`)
5. Buat Pull Request

## 🛠 Roadmap
- [ ] Integrasi dengan Payment Gateway
- [ ] Mode Offline
- [ ] Pembuatan Aplikasi Mobile
- [ ] Integrasi AI untuk Prediksi Stok

## 📄 Lisensi
Proyek ini dilisensikan di bawah lisensi MIT - lihat [LICENSE](LICENSE) untuk detail lebih lanjut.

---
Dibuat dengan ❤️ oleh [kikyrestu](https://github.com/kikyrestu)

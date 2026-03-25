# 🚀 Portfolio Pribadi — Python & Flask

Website portfolio pribadi yang dibangun dari nol pakai **Python** dan **Flask**. Desain dark-mode premium dengan animasi smooth, fully responsive, dan kini dilengkapi dengan **Admin Dashboard** (Sistem CMS sederhana dengan SQLite) untuk mengelola Project dan Blog.

---

## ✨ Fitur Unggulan

| Fitur | Keterangan |
|---|---|
| 🌑 **Dark Mode Premium** | Desain gelap elegan dengan efek glassmorphism dan animated background |
| 🗄️ **Admin Dashboard** | CMS internal untuk mengelola Project & Blog langsung via UI (`/admin`) |
| 📝 **Sistem Blog** | Fitur blog terintegrasi lengkap dengan halaman detail artikel & komentar |
| 🗃️ **SQLite Database** | Penyimpanan data dinamis dan ringan (otomatis dibuat) |
| ⌨️ **Typewriter Effect** | Animasi mengetik role/title di hero section |
| 📊 **Skill Bars Animasi** | Progress bar muncul smooth saat di-scroll |
| 🔍 **Project Filter** | Filter kartu project berdasarkan status secara real-time |
| 📱 **Fully Responsive** | Mobile-first design dengan hamburger menu |
| ✉️ **Form Kontak** | Terintegrasi dengan SMTP untuk mengirim email langsung |
| 🔌 **REST API Lengkap** | Endpoint JSON untuk data project, stats, dan integrasi GitHub API |
| 🏷️ **Dark/Light Mode** | Tombol switch tema di navbar |

---

## 📁 Struktur Folder

```text
web-portfolio/
├── app.py                  # Entry point Flask + routing & konfigurasi utama
├── database.py             # Logika database, fungsi CRUD menggunakan SQLite
├── portfolio.db            # File database SQLite (ter-generate otomatis)
├── requirements.txt        # Daftar dependency Python
├── README.md               # Dokumentasi ini
├── .gitignore              # File yang diabaikan Git
├── static/
│   ├── style.css           # Stylesheet utama
│   └── main.js             # Logika interaksi & animasi frontend
└── templates/
    ├── index.html          # Template HTML halaman utama
    ├── blog.html           # Template daftar artikel blog
    ├── project_detail.html # Template detail project
    ├── admin.html          # Dashboard admin panel
    └── ...                 # Template HTML pendukung lainnya
```

---

## ⚡ Cara Menjalankan

### 1. Clone repository ini

```bash
git clone https://github.com/username/web-portfolio.git
cd web-portfolio
```

### 2. Buat virtual environment (opsional tapi disarankan)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependency

```bash
pip install -r requirements.txt
```

*(Opsional: Install `requests` jika ingin mengaktifkan fitur GitHub API)*

### 4. Jalankan server

```bash
python app.py
```
*Note: Database `portfolio.db` akan terbuat otomatis pada run pertama.*

### 5. Buka di browser

```text
http://127.0.0.1:5000
```

---

## 🎨 Cara Kustomisasi

### 1. Ubah Data Profil Statis
Data profil dasar (Nama, Bio, Tagline) dan daftar keahlian (Skills) masih diatur secara hardcode di **`app.py`** bagian atas. Edit dict `profile` dan list `skills` sesuai gaya lo.

Ganti juga `EMAIL_CONFIG` di dalam `app.py` agar form kontak mengirim pesan langsung ke email lo.

### 2. Kelola Project & Blog (via Admin Panel)
Kini aplikasi portfolio lo sudah dinamis! Nggak perlu edit kodingan lagi untuk nambah portfolio atau nulis blog.

1. Buka browser dan pergi ke: `http://127.0.0.1:5000/admin/login`
2. Masukkan password admin. *(Default: `admin1234` — **Pastikan lo ganti password ini di `app.py` sebelum deploy!**)*
3. Lo sekarang bisa tambah, edit, delete **Project** dan **Blog Post** beserta melihat jumlah views/visitor statistik langsung dari UI!

---

## 🛠️ Teknologi yang Dipakai

- **Python 3.x** — Bahasa utama
- **Flask 3.x** — Web micro-framework
- **SQLite3** — Database bawaan (via modul sqlite3)
- **Jinja2** — Template engine (sudah include di Flask)
- **HTML5 / CSS3** — Struktur & styling
- **Vanilla JavaScript** — Interaksi & animasi (tanpa library eksternal)
- **Google Fonts** — Typography

---

## 📡 API Endpoint

| Method | Endpoint | Keterangan |
|---|---|---|
| `GET` | `/` | Halaman utama portfolio |
| `GET` | `/blog` | Halaman daftar artikel blog |
| `GET` | `/project/<id>` | Halaman detail project tertentu |
| `GET` | `/api/projects` | Data semua project dalam format JSON |
| `GET` | `/api/portfolio` | Mengembalikan JSON gabungan profil, skill, status |
| `GET` | `/api/stats` | JSON statistik total project, artikel, dan total visitor |
| `GET` | `/api/github-repos` | Ambil 6 repo GitHub publik ter-update lo secara dinamis |

---

## 📦 Requirements

```text
Flask>=3.0.0
requests>=2.0.0  # Untuk integrasi GitHub API
```

---

## 🗺️ Roadmap

- [x] Dark mode premium
- [x] Typewriter & scroll animations
- [x] Project filter by status
- [x] Dark/Light mode toggle
- [x] Halaman detail per project
- [x] Sistem admin dashboard (CMS)
- [x] Blog / Artikel section
- [x] Integrasi database (SQLite)
- [ ] Multi-bahasa (ID/EN)
- [ ] Deploy ke Railway / Render

---

## 📄 Lisensi

**Personal License (Lisensi Pribadi)**

Hak Cipta © 2026 Achmad Fauzan. Proyek ini dikembangkan dari nol sebagai bagian dari portofolio pribadi.

Anda diperbolehkan untuk melihat dan mempelajari kode sumber proyek ini. Namun, Anda **tidak diperkenankan** untuk menyalin, mendistribusikan ulang, mencetak ulang, atau menggunakan rekam jejak kode maupun desain visual proyek ini untuk tujuan komersial atau diklaim sebagai portofolio pribadi Saya tanpa seizin dari pembuat.

### 📞 Kontak
Jika ada pertanyaan atau ingin berdiskusi, silakan hubungi saya melalui:
- **GitHub**: [@Achmddfzn](https://github.com/Achmddfzn)
- **Discord**: `henka#2552` *(silakan ubah dengan username Discord asli kamu)*

---

<p align="center">
  Dibuat dengan ❤️ oleh <a href="https://github.com/Achmddfzn">Achmad Fauzan</a> pakai Python & Flask &nbsp;|&nbsp; 2026
</p>

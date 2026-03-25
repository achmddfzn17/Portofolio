import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'portfolio.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    # ─── Visitors Table ────────────────────────────────────────────────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            ip        TEXT,
            page      TEXT,
            timestamp TEXT
        )
    ''')

    # ─── Blog Posts Table ──────────────────────────────────────────────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS blog_posts (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            judul   TEXT NOT NULL,
            slug    TEXT UNIQUE NOT NULL,
            konten  TEXT NOT NULL,
            excerpt TEXT,
            tags    TEXT,
            tanggal TEXT,
            status  TEXT DEFAULT 'publish'
        )
    ''')

    # ─── Projects Table (for admin management) ────────────────────────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nama      TEXT NOT NULL,
            deskripsi TEXT,
            detail    TEXT,
            teknologi TEXT,
            icon      TEXT DEFAULT '🔧',
            github    TEXT DEFAULT '#',
            demo      TEXT DEFAULT '#',
            status    TEXT DEFAULT 'Perencanaan'
        )
    ''')

    # ─── Comments Table ────────────────────────────────────────────────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            post_slug TEXT NOT NULL,
            nama      TEXT NOT NULL,
            komentar  TEXT NOT NULL,
            tanggal   TEXT NOT NULL
        )
    ''')

    # ─── Seed Projects ────────────────────────────────────────────────────────
    c.execute('SELECT COUNT(*) FROM projects')
    if c.fetchone()[0] == 0:
        seed_projects = [
            ("Bot Telegram Penjawab Otomatis", "Bot Python canggih untuk membalas pesan secara otomatis.", "Bot ini dilengkapi fitur handler.", "Python,Telebot", "🤖", "#", "#", "Perencanaan"),
            ("Data Analisis Penjualan", "Menganalisis tren penjualan kopi.", "Menggunakan dataset CSV.", "Python,Pandas", "☕", "#", "#", "Perencanaan"),
            ("Aplikasi Kasir CLI", "Program kasir sederhana berbasis teks.", "Aplikasi CLI lengkap CRUD.", "Python,OOP", "🧾", "#", "#", "Perencanaan"),
            ("Website Portfolio Ini", "Portfolio pribadi dibangun dengan Flask.", "Backend dengan Flask, Frontend murni.", "Python,Flask", "🌐", "https://github.com/Achmddfzn", "https://portofolio--achmddfzn.replit.app/", "Selesai")
        ]
        c.executemany(
            'INSERT INTO projects (nama, deskripsi, detail, teknologi, icon, github, demo, status) VALUES (?,?,?,?,?,?,?,?)',
            seed_projects
        )

    # ─── Seed Blog Posts ───────────────────────────────────────────────────────
    c.execute('SELECT COUNT(*) FROM blog_posts')
    if c.fetchone()[0] == 0:
        seed_posts = [
            (
                'Belajar Flask dari Nol: Panduan Pemula',
                'belajar-flask',
                '''<p>Flask adalah micro-framework Python yang ringan namun powerful. Berbeda dengan Django yang "batteries included", Flask memberikan kebebasan penuh untuk memilih komponen yang dibutuhkan.</p>
<h2>Kenapa Flask?</h2>
<p>Flask cocok untuk pemula karena minimnya boilerplate code. Cukup beberapa baris Python, website lo sudah bisa jalan.</p>
<pre><code>from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Halo Dunia!"</code></pre>
<h2>Struktur Folder yang Baik</h2>
<p>Selalu pisahkan logika, template, dan static file. Ini memudahkan maintenance di masa depan.</p>
<p>Happy coding!</p>''',
                'Flask adalah micro-framework Python yang ringan namun powerful untuk membangun web app.',
                'Python,Flask,Tutorial',
                '2026-03-01',
                'publish'
            ),
            (
                'Tips Git untuk Developer Pemula',
                'tips-git',
                '''<p>Git adalah version control system yang wajib dikuasai oleh setiap developer. Dengan Git, lo bisa tracking perubahan kode, kolaborasi dengan tim, dan balik ke versi sebelumnya kapanpun.</p>
<h2>Perintah Git Paling Sering Dipakai</h2>
<pre><code>git init          # Inisiasi repo baru
git add .         # Staging semua perubahan
git commit -m ""  # Simpan snapshot
git push          # Upload ke GitHub
git pull          # Download perubahan terbaru</code></pre>
<h2>Tips Nulis Commit Message</h2>
<p>Commit message yang bagus adalah ringkas, jelas, dan dalam bentuk imperatif. Contoh: "Add login feature" bukan "Added login feature".</p>''',
                'Panduan Git untuk developer pemula: perintah dasar, tips commit message, dan workflow yang baik.',
                'Git,GitHub,Tools',
                '2026-03-10',
                'publish'
            ),
            (
                'Kenapa Python Jadi Bahasa Favorit Gue',
                'kenapa-python',
                '''<p>Dari sekian banyak bahasa pemrograman yang ada, Python selalu jadi pilihan pertama gue. Bukan tanpa alasan — Python punya filosofi yang elegan dan ekosistem yang luar biasa besar.</p>
<h2>Sintaks yang Bersih</h2>
<p>Python memaksa programmer untuk menulis kode yang rapi dan terbaca. Indentasi bukan opsional, melainkan bagian dari sintaks itu sendiri.</p>
<h2>Serbaguna</h2>
<p>Python bisa dipakai untuk web development (Flask, Django), data science (Pandas, Numpy), automation, AI/ML, dan masih banyak lagi. Satu bahasa, banyak domain.</p>
<h2>Komunitas Besar</h2>
<p>Stuck di suatu masalah? Kemungkinan besar sudah ada yang tanya di Stack Overflow atau ada librarynya di PyPI. Ekosistem Python sangat mature.</p>''',
                'Alasan kenapa Python jadi bahasa pemrograman favorit: sintaks bersih, serbaguna, dan komunitas besar.',
                'Python,Opini',
                '2026-03-20',
                'publish'
            ),
        ]
        c.executemany(
            'INSERT INTO blog_posts (judul, slug, konten, excerpt, tags, tanggal, status) VALUES (?,?,?,?,?,?,?)',
            seed_posts
        )

    conn.commit()
    conn.close()


def log_visitor(ip, page):
    from datetime import datetime
    conn = get_db()
    conn.execute(
        'INSERT INTO visitors (ip, page, timestamp) VALUES (?, ?, ?)',
        (ip, page, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    )
    conn.commit()
    conn.close()


def get_visitor_count():
    conn = get_db()
    count = conn.execute('SELECT COUNT(*) FROM visitors').fetchone()[0]
    conn.close()
    return count


def get_all_posts(only_published=True):
    conn = get_db()
    if only_published:
        rows = conn.execute(
            'SELECT * FROM blog_posts WHERE status=? ORDER BY tanggal DESC',
            ('publish',)
        ).fetchall()
    else:
        rows = conn.execute(
            'SELECT * FROM blog_posts ORDER BY tanggal DESC'
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_post_by_slug(slug):
    conn = get_db()
    row = conn.execute('SELECT * FROM blog_posts WHERE slug=?', (slug,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_post_by_id(pid):
    conn = get_db()
    row = conn.execute('SELECT * FROM blog_posts WHERE id=?', (pid,)).fetchone()
    conn.close()
    return dict(row) if row else None


def save_post(judul, slug, konten, excerpt, tags, tanggal, status, pid=None):
    conn = get_db()
    if pid:
        conn.execute(
            'UPDATE blog_posts SET judul=?, slug=?, konten=?, excerpt=?, tags=?, tanggal=?, status=? WHERE id=?',
            (judul, slug, konten, excerpt, tags, tanggal, status, pid)
        )
    else:
        conn.execute(
            'INSERT INTO blog_posts (judul, slug, konten, excerpt, tags, tanggal, status) VALUES (?,?,?,?,?,?,?)',
            (judul, slug, konten, excerpt, tags, tanggal, status)
        )
    conn.commit()
    conn.close()


def delete_post(pid):
    conn = get_db()
    conn.execute('DELETE FROM blog_posts WHERE id=?', (pid,))
    conn.commit()
    conn.close()


# ─── Projects CRUD ─────────────────────────────────────────────────────────────

def get_all_projects():
    conn = get_db()
    rows = conn.execute('SELECT * FROM projects ORDER BY id DESC').fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_project_by_id(pid):
    conn = get_db()
    row = conn.execute('SELECT * FROM projects WHERE id=?', (pid,)).fetchone()
    conn.close()
    return dict(row) if row else None

def save_project(nama, deskripsi, detail, teknologi, icon, github, demo, status, pid=None):
    conn = get_db()
    if pid:
        conn.execute('''
            UPDATE projects 
            SET nama=?, deskripsi=?, detail=?, teknologi=?, icon=?, github=?, demo=?, status=?
            WHERE id=?
        ''', (nama, deskripsi, detail, teknologi, icon, github, demo, status, pid))
    else:
        conn.execute('''
            INSERT INTO projects (nama, deskripsi, detail, teknologi, icon, github, demo, status)
            VALUES (?,?,?,?,?,?,?,?)
        ''', (nama, deskripsi, detail, teknologi, icon, github, demo, status))
    conn.commit()
    conn.close()

def delete_project(pid):
    conn = get_db()
    conn.execute('DELETE FROM projects WHERE id=?', (pid,))
    conn.commit()
    conn.close()


# ─── Comments CRUD ─────────────────────────────────────────────────────────────

def get_comments(post_slug):
    conn = get_db()
    rows = conn.execute(
        'SELECT * FROM comments WHERE post_slug=? ORDER BY id DESC',
        (post_slug,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_comment(post_slug, nama, komentar, tanggal):
    conn = get_db()
    conn.execute(
        'INSERT INTO comments (post_slug, nama, komentar, tanggal) VALUES (?,?,?,?)',
        (post_slug, nama, komentar, tanggal)
    )
    conn.commit()
    conn.close()

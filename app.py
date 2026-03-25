from flask import (
    Flask, render_template, jsonify, request,
    redirect, url_for, session, flash
)
import smtplib
import ssl
import os
import json
from datetime import datetime

from database import (
    init_db, log_visitor, get_visitor_count,
    get_all_posts, get_post_by_slug, get_post_by_id,
    save_post, delete_post,
    get_all_projects, get_project_by_id, save_project, delete_project,
    get_comments, add_comment
)

# Try importing requests for GitHub API (optional)
try:
    import requests as req
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

app = Flask(__name__)
app.secret_key = 'p0rtf0li0-achmad-secret-2026'  # Ganti sebelum deploy!

# ─── Config ────────────────────────────────────────────────────────────────────

EMAIL_CONFIG = {
    "smtp_host":  "smtp.gmail.com",
    "smtp_port":  465,
    "sender":     "achmddfzn@gmail.com",    # Gmail lo
    "password":   "",                        # App Password Gmail (bukan password biasa!)
    "recipient":  "achmddfzn@gmail.com",    # Tujuan penerima pesan
}

ADMIN_PASSWORD  = "admin1234"       # Ganti sebelum deploy!
GITHUB_USERNAME = "Achmddfzn"

# ─── Init Database ─────────────────────────────────────────────────────────────

with app.app_context():
    init_db()

# ─── Visitor Logger (before every request) ────────────────────────────────────

@app.before_request
def track_visitor():
    skip = (
        request.path.startswith('/static') or
        request.path.startswith('/admin') or
        request.path.startswith('/api') or
        request.path.startswith('/favicon')
    )
    if not skip:
        log_visitor(request.remote_addr, request.path)

# ─── Data Portfolio ────────────────────────────────────────────────────────────

skills = [
    {"kategori": "Language", "list": [
        {"nama": "Python",     "level": 80},
        {"nama": "JavaScript", "level": 55},
        {"nama": "HTML/CSS",   "level": 70},
        {"nama": "SQL",        "level": 60},
    ]},
    {"kategori": "Framework & Library", "list": [
        {"nama": "Flask",         "level": 75},
        {"nama": "Pandas",        "level": 70},
        {"nama": "Matplotlib",    "level": 65},
        {"nama": "BeautifulSoup", "level": 60},
    ]},
    {"kategori": "Tools", "list": [
        {"nama": "Git & GitHub", "level": 65},
        {"nama": "VS Code",      "level": 85},
        {"nama": "Postman",      "level": 60},
        {"nama": "Linux CLI",    "level": 55},
    ]},
]

profile = {
    "nama":     "Achmad Fauzan",
    "tagline":  "Turning Ideas Into Code, One Line at a Time.",
    "bio":      "Halo! Gue adalah seorang Python developer pemula yang passionate dalam membangun solusi digital. Gue suka eksplorasi hal baru mulai dari automation, data analysis, sampai web development.",
    "email":    "achmddfzn@gmail.com",
    "github":   "https://github.com/Achmddfzn",
    "linkedin": "https://linkedin.com",
    "twitter":  "https://twitter.com",
    "lokasi":   "Indonesia 🇮🇩",
    "status":   "Open for Opportunities",
}

# ─── Main Routes ───────────────────────────────────────────────────────────────

@app.route('/')
def home():
    return render_template(
        'index.html',
        profile=profile,
        my_projects=get_all_projects(),
        skills=skills
    )


@app.route('/project/<int:pid>')
def project_detail(pid):
    project = get_project_by_id(pid)
    if not project:
        return render_template('404.html', profile=profile), 404
    # Related: same tech tag, excluding current
    all_projects = get_all_projects()
    related = [p for p in all_projects if p['id'] != pid
               and any(t.strip() in project['teknologi'] for t in p['teknologi'].split(','))][:3]
    return render_template('project_detail.html', project=project, related=related, profile=profile)


# ─── Blog Routes ───────────────────────────────────────────────────────────────

@app.route('/blog')
def blog():
    posts = get_all_posts()
    # collect unique tags
    all_tags = set()
    for p in posts:
        if p.get('tags'):
            for t in p['tags'].split(','):
                all_tags.add(t.strip())
    return render_template('blog.html', posts=posts, tags=sorted(all_tags), profile=profile)


@app.route('/blog/<slug>')
def blog_post(slug):
    post = get_post_by_slug(slug)
    if not post:
        return render_template('404.html', profile=profile), 404
    all_posts    = get_all_posts()
    idx          = next((i for i, p in enumerate(all_posts) if p['slug'] == slug), None)
    prev_post    = all_posts[idx + 1] if idx is not None and idx + 1 < len(all_posts) else None
    next_post    = all_posts[idx - 1] if idx is not None and idx > 0 else None
    return render_template('blog_post.html', post=post, prev_post=prev_post, next_post=next_post, profile=profile)


# ─── Email Route ───────────────────────────────────────────────────────────────

@app.route('/send-email', methods=['POST'])
def send_email():
    data    = request.get_json() or request.form
    nama    = data.get('nama', '').strip()
    email   = data.get('email', '').strip()
    pesan   = data.get('pesan', '').strip()

    if not all([nama, email, pesan]):
        return jsonify({'ok': False, 'msg': 'Semua field wajib diisi.'}), 400

    cfg = EMAIL_CONFIG
    if not cfg['password']:
        # No SMTP configured — just simulate success for demo
        return jsonify({'ok': True, 'msg': 'Pesan terkirim! (mode demo)'}), 200

    try:
        subject = f"[Portfolio] Pesan dari {nama}"
        body    = f"Dari    : {nama} <{email}>\n\nPesan:\n{pesan}"
        message = f"Subject: {subject}\nFrom: {cfg['sender']}\nTo: {cfg['recipient']}\n\n{body}"
        ctx     = ssl.create_default_context()
        with smtplib.SMTP_SSL(cfg['smtp_host'], cfg['smtp_port'], context=ctx) as server:
            server.login(cfg['sender'], cfg['password'])
            server.sendmail(cfg['sender'], cfg['recipient'], message.encode('utf-8'))
        return jsonify({'ok': True, 'msg': 'Pesan berhasil terkirim!'}), 200
    except Exception as e:
        return jsonify({'ok': False, 'msg': f'Gagal mengirim: {str(e)}'}), 500


# ─── GitHub API Route ──────────────────────────────────────────────────────────

@app.route('/api/github-repos')
def github_repos():
    if not REQUESTS_AVAILABLE:
        return jsonify({'ok': False, 'msg': 'requests not installed'}), 500
    try:
        url      = f'https://api.github.com/users/{GITHUB_USERNAME}/repos'
        params   = {'sort': 'updated', 'per_page': 6, 'type': 'public'}
        headers  = {'Accept': 'application/vnd.github.v3+json', 'User-Agent': 'portfolio-app'}
        response = req.get(url, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            repos = response.json()
            result = [{
                'name':        r['name'],
                'description': r['description'] or 'Tidak ada deskripsi.',
                'url':         r['html_url'],
                'language':    r['language'] or 'N/A',
                'stars':       r['stargazers_count'],
                'forks':       r['forks_count'],
            } for r in repos]
            return jsonify({'ok': True, 'repos': result})
        return jsonify({'ok': False, 'msg': f'GitHub API error {response.status_code}'}), 502
    except Exception as e:
        return jsonify({'ok': False, 'msg': str(e)}), 500


@app.route('/api/projects')
def api_projects():
    return jsonify(get_all_projects())


@app.route('/api/stats')
def api_stats():
    return jsonify({
        'total_projects': len(get_all_projects()),
        'total_posts':    len(get_all_posts()),
        'total_visitors': get_visitor_count(),
    })


@app.route('/api/portfolio')
def api_portfolio():
    return jsonify({
        'profile': profile,
        'skills': skills,
        'projects': get_all_projects()
    })


@app.route('/api/comments/<slug>', methods=['GET', 'POST'])
def api_comments(slug):
    if request.method == 'POST':
        data = request.get_json()
        if not data or not data.get('nama') or not data.get('komentar'):
            return jsonify({'ok': False, 'msg': 'Nama dan komentar wajib diisi'}), 400
        
        now = datetime.now().strftime('%d %b %Y, %H:%M')
        add_comment(slug, data['nama'].strip()[:50], data['komentar'].strip()[:500], now)
        return jsonify({'ok': True, 'msg': 'Komentar berhasil ditambahkan'})
        
    # GET
    return jsonify({'ok': True, 'comments': get_comments(slug)})

# ─── Admin Routes ──────────────────────────────────────────────────────────────

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
    error = None
    if request.method == 'POST':
        pwd = request.form.get('password', '')
        if pwd == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        error = 'Password salah!'
    return render_template('admin_login.html', error=error, profile=profile)


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('home'))


@app.route('/admin')
@admin_required
def admin_dashboard():
    posts    = get_all_posts(only_published=False)
    visitors = get_visitor_count()
    projects = get_all_projects()
    return render_template(
        'admin.html',
        posts=posts,
        projects=projects,
        visitors=visitors,
        profile=profile
    )


@app.route('/admin/blog/new', methods=['GET', 'POST'])
@admin_required
def admin_new_post():
    if request.method == 'POST':
        judul   = request.form.get('judul', '').strip()
        slug    = request.form.get('slug', '').strip().replace(' ', '-').lower()
        konten  = request.form.get('konten', '').strip()
        excerpt = request.form.get('excerpt', '').strip()
        tags    = request.form.get('tags', '').strip()
        tanggal = request.form.get('tanggal', datetime.now().strftime('%Y-%m-%d'))
        status  = request.form.get('status', 'publish')
        save_post(judul, slug, konten, excerpt, tags, tanggal, status)
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_post_form.html', post=None, profile=profile)


@app.route('/admin/blog/edit/<int:pid>', methods=['GET', 'POST'])
@admin_required
def admin_edit_post(pid):
    post = get_post_by_id(pid)
    if not post:
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        judul   = request.form.get('judul', '').strip()
        slug    = request.form.get('slug', '').strip().replace(' ', '-').lower()
        konten  = request.form.get('konten', '').strip()
        excerpt = request.form.get('excerpt', '').strip()
        tags    = request.form.get('tags', '').strip()
        tanggal = request.form.get('tanggal', post['tanggal'])
        status  = request.form.get('status', 'publish')
        save_post(judul, slug, konten, excerpt, tags, tanggal, status, pid=pid)
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_post_form.html', post=post, profile=profile)


@app.route('/admin/blog/delete/<int:pid>', methods=['POST'])
@admin_required
def admin_delete_post(pid):
    delete_post(pid)
    return redirect(url_for('admin_dashboard'))


# ─── Admin Project Routes ─────────────────────────────────────────────────────────

@app.route('/admin/project/new', methods=['GET', 'POST'])
@admin_required
def admin_new_project():
    if request.method == 'POST':
        nama      = request.form.get('nama', '').strip()
        deskripsi = request.form.get('deskripsi', '').strip()
        detail    = request.form.get('detail', '').strip()
        teknologi = request.form.get('teknologi', '').strip()
        icon      = request.form.get('icon', '🔧').strip()
        github    = request.form.get('github', '#').strip()
        demo      = request.form.get('demo', '#').strip()
        status    = request.form.get('status', 'Perencanaan').strip()
        save_project(nama, deskripsi, detail, teknologi, icon, github, demo, status)
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_project_form.html', project=None, profile=profile)

@app.route('/admin/project/edit/<int:pid>', methods=['GET', 'POST'])
@admin_required
def admin_edit_project(pid):
    project = get_project_by_id(pid)
    if not project:
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        nama      = request.form.get('nama', '').strip()
        deskripsi = request.form.get('deskripsi', '').strip()
        detail    = request.form.get('detail', '').strip()
        teknologi = request.form.get('teknologi', '').strip()
        icon      = request.form.get('icon', '🔧').strip()
        github    = request.form.get('github', '#').strip()
        demo      = request.form.get('demo', '#').strip()
        status    = request.form.get('status', 'Perencanaan').strip()
        save_project(nama, deskripsi, detail, teknologi, icon, github, demo, status, pid=pid)
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_project_form.html', project=project, profile=profile)

@app.route('/admin/project/delete/<int:pid>', methods=['POST'])
@admin_required
def admin_delete_project(pid):
    delete_project(pid)
    return redirect(url_for('admin_dashboard'))


# ─── Error Handlers ────────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', profile=profile), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('404.html', profile=profile, code=500), 500


# ─── Run ───────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True, port=5000)

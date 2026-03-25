/* ─── main.js — Portfolio Interactions (100% original) ──────────────────── */

// ─── Theme Toggle ─────────────────────────────────────────────────────────────
const themeToggle = document.getElementById('theme-toggle');
const savedTheme = localStorage.getItem('theme');

if (savedTheme === 'light') {
    document.body.classList.add('light');
    if (themeToggle) themeToggle.textContent = '☀️';
}

if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        const isLight = document.body.classList.toggle('light');
        themeToggle.textContent = isLight ? '☀️' : '🌙';
        localStorage.setItem('theme', isLight ? 'light' : 'dark');
    });
}

// ─── Loading Splash Screen ────────────────────────────────────────────────────
const loader = document.getElementById('loader');
if (loader) {
    const fill = document.getElementById('loader-fill');
    const txt = document.getElementById('loader-text');
    const msgs = ['Memuat portfolio...', 'Menyiapkan data...', 'Hampir siap...'];
    let pct = 0, mi = 0;
    const iv = setInterval(() => {
        pct += Math.random() * 20 + 5;
        if (fill) fill.style.width = Math.min(pct, 95) + '%';
        if (txt && mi < msgs.length) { txt.textContent = msgs[mi++]; }
        if (pct >= 95) clearInterval(iv);
    }, 300);
    window.addEventListener('load', () => {
        if (fill) fill.style.width = '100%';
        setTimeout(() => {
            loader.classList.add('loader-done');
            setTimeout(() => loader.remove(), 500);
        }, 400);
    });
}

// ─── Custom Cursor ────────────────────────────────────────────────────────────
const cursorDot = document.getElementById('cursor-dot');
const cursorRing = document.getElementById('cursor-ring');

if (cursorDot && cursorRing) {
    let rx = 0, ry = 0; // ring position (lerped)
    let dx = 0, dy = 0; // dot/target position

    document.addEventListener('mousemove', (e) => {
        dx = e.clientX;
        dy = e.clientY;
        cursorDot.style.transform = `translate(${dx - 4}px, ${dy - 4}px)`;
    });

    (function animateRing() {
        rx += (dx - rx) * 0.12;
        ry += (dy - ry) * 0.12;
        cursorRing.style.transform = `translate(${rx - 16}px, ${ry - 16}px)`;
        requestAnimationFrame(animateRing);
    })();

    // Grow ring on interactive elements
    document.querySelectorAll('a, button, .project-card, .blog-card, .tag').forEach(el => {
        el.addEventListener('mouseenter', () => cursorRing.classList.add('cursor-hover'));
        el.addEventListener('mouseleave', () => cursorRing.classList.remove('cursor-hover'));
    });
}

// ─── Particle Background ──────────────────────────────────────────────────────
const canvas = document.getElementById('particles');
if (canvas) {
    const ctx = canvas.getContext('2d');
    let W, H, pts;

    function resizeCanvas() {
        W = canvas.width = canvas.offsetWidth;
        H = canvas.height = canvas.offsetHeight;
    }

    function makeParticles(n) {
        return Array.from({ length: n }, () => ({
            x: Math.random() * W,
            y: Math.random() * H,
            vx: (Math.random() - 0.5) * 0.3,
            vy: (Math.random() - 0.5) * 0.3,
            r: Math.random() * 1.5 + 0.5,
            a: Math.random() * 0.4 + 0.1,
        }));
    }

    function drawParticles() {
        ctx.clearRect(0, 0, W, H);
        pts.forEach(p => {
            // move
            p.x += p.vx;
            p.y += p.vy;
            if (p.x < 0) p.x = W;
            if (p.x > W) p.x = 0;
            if (p.y < 0) p.y = H;
            if (p.y > H) p.y = 0;
            // draw dot
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(108,99,255,${p.a})`;
            ctx.fill();
        });
        // draw connecting lines
        for (let i = 0; i < pts.length; i++) {
            for (let j = i + 1; j < pts.length; j++) {
                const d = Math.hypot(pts[i].x - pts[j].x, pts[i].y - pts[j].y);
                if (d < 120) {
                    ctx.beginPath();
                    ctx.moveTo(pts[i].x, pts[i].y);
                    ctx.lineTo(pts[j].x, pts[j].y);
                    ctx.strokeStyle = `rgba(108,99,255,${0.08 * (1 - d / 120)})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(drawParticles);
    }

    resizeCanvas();
    pts = makeParticles(60);
    drawParticles();
    window.addEventListener('resize', () => { resizeCanvas(); pts = makeParticles(60); });
}

// ─── Scroll Progress Bar ──────────────────────────────────────────────────────
const progressBar = document.getElementById('scroll-progress');

// ─── Copy Email Button ────────────────────────────────────────────────────────
const copyBtn = document.getElementById('copy-email-btn');
const toast = document.getElementById('toast');
let toastTimer;

if (copyBtn) {
    copyBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const email = copyBtn.getAttribute('data-email');
        navigator.clipboard.writeText(email).then(() => {
            copyBtn.textContent = '✓';
            copyBtn.classList.add('copied');
            if (toast) toast.classList.add('show');
            clearTimeout(toastTimer);
            toastTimer = setTimeout(() => {
                copyBtn.textContent = '⎘';
                copyBtn.classList.remove('copied');
                if (toast) toast.classList.remove('show');
            }, 2500);
        });
    });
}

// ─── Navbar scroll + progress bar ────────────────────────────────────────────
const navbar = document.getElementById('navbar');
const backToTop = document.getElementById('back-to-top');

window.addEventListener('scroll', () => {
    const scrolled = window.scrollY;
    const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
    if (progressBar) progressBar.style.width = maxScroll > 0 ? (scrolled / maxScroll * 100) + '%' : '0%';
    if (navbar) navbar.classList.toggle('scrolled', scrolled > 50);
    if (backToTop) backToTop.classList.toggle('visible', scrolled > 400);
});

// ─── Mobile hamburger menu ────────────────────────────────────────────────────
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('nav-links');

if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('open');
        hamburger.classList.toggle('open');
    });
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('open');
            hamburger.classList.remove('open');
        });
    });
}

// ─── Back to Top ─────────────────────────────────────────────────────────────
if (backToTop) {
    backToTop.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// ─── Typewriter Effect ────────────────────────────────────────────────────────
const typeEl = document.getElementById('typewriter');
if (typeEl) {
    const words = ['Python Dev 🐍', 'Web Builder 🌐', 'Problem Solver 🧠', 'Open to Work ✅'];
    let wi = 0, ci = 0, deleting = false;

    function typeLoop() {
        const word = words[wi];
        const current = deleting ? word.slice(0, ci--) : word.slice(0, ++ci);
        typeEl.textContent = current;
        let delay = deleting ? 60 : 110;
        if (!deleting && ci === word.length) { delay = 1800; deleting = true; }
        else if (deleting && ci === 0) { deleting = false; wi = (wi + 1) % words.length; }
        setTimeout(typeLoop, delay);
    }
    typeLoop();
}

// ─── Count-Up Animation ───────────────────────────────────────────────────────
function countUp(el, target, duration = 1200) {
    const isSpecial = isNaN(parseInt(target));
    if (isSpecial) return;
    const end = parseInt(target);
    const step = Math.ceil(end / (duration / 16));
    let cur = 0;
    const timer = setInterval(() => {
        cur = Math.min(cur + step, end);
        el.textContent = cur + '+';
        if (cur >= end) clearInterval(timer);
    }, 16);
}

// ─── Scroll Reveal & Count-Up Trigger ────────────────────────────────────────
const revealEls = document.querySelectorAll('.section, .project-card, .skill-group, .blog-card');
const statNums = document.querySelectorAll('.stat-num');
const skillFills = document.querySelectorAll('.skill-fill');
let statsAnimated = false, skillsAnimated = false;

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.12 });

revealEls.forEach(el => {
    el.classList.add('reveal');
    observer.observe(el);
});

// Count-up + skill bars trigger via separate observer
const aboutSection = document.getElementById('about');
const skillsSection = document.getElementById('skills');

if (aboutSection) {
    new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting && !statsAnimated) {
            statsAnimated = true;
            statNums.forEach(el => {
                const raw = el.textContent.replace('+', '').trim();
                countUp(el, raw);
            });
        }
    }, { threshold: 0.3 }).observe(aboutSection);
}

if (skillsSection) {
    new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting && !skillsAnimated) {
            skillsAnimated = true;
            skillFills.forEach(bar => {
                bar.style.width = bar.getAttribute('data-width') + '%';
            });
        }
    }, { threshold: 0.2 }).observe(skillsSection);
}

// ─── Language Toggle (ID/EN) ──────────────────────────────────────────────────
const langBtn = document.getElementById('lang-toggle');
let currentLang = localStorage.getItem('lang') || 'id';

const translations = {
    id: {
        'nav.home': 'Home',
        'nav.about': 'About',
        'nav.skills': 'Skills',
        'nav.projects': 'Projects',
        'nav.contact': 'Contact',
        'hero.cta': 'Lihat Projects →',
        'hero.contact': 'Hubungi Gue',
        'hero.cv': '↓ Download CV',
    },
    en: {
        'nav.home': 'Home',
        'nav.about': 'About',
        'nav.skills': 'Skills',
        'nav.projects': 'Projects',
        'nav.contact': 'Contact',
        'hero.cta': 'View Projects →',
        'hero.contact': 'Contact Me',
        'hero.cv': '↓ Download CV',
    }
};

function applyLang(lang) {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        const val = translations[lang] && translations[lang][key];
        if (val) el.textContent = val;
    });
    if (langBtn) langBtn.textContent = `🌐 ${lang.toUpperCase()}`;
    localStorage.setItem('lang', lang);
    currentLang = lang;
}

if (langBtn) {
    applyLang(currentLang);
    langBtn.addEventListener('click', () => {
        applyLang(currentLang === 'id' ? 'en' : 'id');
    });
}

// ─── Project Filter ───────────────────────────────────────────────────────────
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const filter = btn.getAttribute('data-filter');
        document.querySelectorAll('.project-card').forEach(card => {
            const show = filter === 'all' || card.getAttribute('data-status') === filter;
            card.classList.toggle('hidden', !show);
        });
    });
});

// ─── Contact Form (fetch → /send-email) ──────────────────────────────────────
const form = document.getElementById('contact-form');
const submitBtn = document.getElementById('submit-btn');
const successEl = document.getElementById('form-success');

if (form) {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (submitBtn) { submitBtn.disabled = true; submitBtn.querySelector('span').textContent = 'Mengirim...'; }
        const body = {
            nama: document.getElementById('name')?.value,
            email: document.getElementById('email-input')?.value,
            pesan: document.getElementById('message')?.value,
        };
        try {
            const res = await fetch('/send-email', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            const data = await res.json();
            if (data.ok) {
                if (successEl) { successEl.textContent = '✅ ' + data.msg; successEl.style.display = 'block'; }
                form.reset();
                fireConfetti();
            } else {
                if (successEl) { successEl.textContent = '⚠️ ' + data.msg; successEl.style.color = 'var(--red)'; successEl.style.display = 'block'; }
            }
        } catch {
            if (successEl) { successEl.textContent = '⚠️ Gagal mengirim. Coba lagi nanti.'; successEl.style.display = 'block'; }
        } finally {
            if (submitBtn) { submitBtn.disabled = false; submitBtn.querySelector('span').textContent = 'Kirim Pesan 🚀'; }
        }
    });
}

// ─── Confetti (100% custom canvas, no library) ───────────────────────────────
function fireConfetti() {
    const canvas = document.createElement('canvas');
    canvas.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:9999;';
    document.body.appendChild(canvas);
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const colors = ['#6c63ff', '#a78bfa', '#00d48a', '#ffd166', '#ff6b6b', '#8be9fd'];
    const pieces = Array.from({ length: 120 }, () => ({
        x: Math.random() * canvas.width,
        y: -10 - Math.random() * 100,
        r: Math.random() * 6 + 3,
        c: colors[Math.floor(Math.random() * colors.length)],
        vx: (Math.random() - 0.5) * 4,
        vy: Math.random() * 3 + 2,
        rot: Math.random() * Math.PI * 2,
        rotSpd: (Math.random() - 0.5) * 0.15,
    }));

    let alive = true;
    function draw() {
        if (!alive) return;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        alive = false;
        pieces.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;
            p.vy += 0.05;
            p.rot += p.rotSpd;
            if (p.y < canvas.height + 20) alive = true;
            ctx.save();
            ctx.translate(p.x, p.y);
            ctx.rotate(p.rot);
            ctx.fillStyle = p.c;
            ctx.fillRect(-p.r / 2, -p.r / 2, p.r, p.r * 1.6);
            ctx.restore();
        });
        requestAnimationFrame(draw);
        if (!alive) canvas.remove();
    }
    draw();
    setTimeout(() => { alive = false; canvas.remove(); }, 4000);
}

// ─── GitHub Repos Loader ──────────────────────────────────────────────────────
const reposGrid = document.getElementById('repos-grid');
if (reposGrid) {
    fetch('/api/github-repos')
        .then(r => r.json())
        .then(data => {
            const loading = document.getElementById('repos-loading');
            if (loading) loading.remove();
            if (data.ok && data.repos.length) {
                data.repos.forEach(repo => {
                    const card = document.createElement('a');
                    card.href = repo.url;
                    card.target = '_blank';
                    card.className = 'repo-card';
                    card.innerHTML = `
                        <div class="repo-name">${repo.name}</div>
                        <p class="repo-desc">${repo.description}</p>
                        <div class="repo-meta">
                            <span class="repo-lang">${repo.language}</span>
                            <span>⭐ ${repo.stars}</span>
                            <span>🍴 ${repo.forks}</span>
                        </div>
                    `;
                    reposGrid.appendChild(card);
                });
            } else {
                reposGrid.innerHTML = '<p style="text-align:center;color:var(--text-muted);padding:2rem;">Tidak dapat memuat repo saat ini.</p>';
            }
        })
        .catch(() => {
            if (reposGrid) reposGrid.innerHTML = '<p style="text-align:center;color:var(--text-muted);padding:2rem;">Periksa koneksi internet lo.</p>';
        });
}

"""
auth/auth.py
-------------
Complete authentication system with:
  - Premium dark landing page (glassmorphism, animations)
  - Login page
  - Sign Up page
  - Session state management

Usage in app.py:
    from auth.auth import require_auth, logout
    if not require_auth():
        st.stop()
"""

import streamlit as st
import hashlib
import json
import os
import re

# ─────────────────────────────────────────────
# SIMPLE USER STORE  (file-based, no database)
# ─────────────────────────────────────────────
USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")


def _load_users() -> dict:
    if not os.path.exists(USERS_FILE):
        # Seed with demo accounts
        demo = {
            "admin": {
                "name": "Admin HR",
                "email": "admin@company.com",
                "password": _hash("admin123"),
                "role": "admin",
            },
            "hrmanager": {
                "name": "HR Manager",
                "email": "hr@company.com",
                "password": _hash("hr1234"),
                "role": "hr",
            },
        }
        _save_users(demo)
        return demo
    with open(USERS_FILE) as f:
        return json.load(f)


def _save_users(users: dict):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def _validate_email(email: str) -> bool:
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))


# ─────────────────────────────────────────────
# SHARED CSS
# ─────────────────────────────────────────────
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
  --bg1: #090014;
  --bg2: #12002B;
  --bg3: #1A063A;
  --purple: #7C3AED;
  --violet: #8B5CF6;
  --blue: #4F8CFF;
  --cyan: #22D3EE;
  --pink: #EC4899;
  --orange: #F59E0B;
  --white: #FFFFFF;
  --gray: #94A3B8;
  --soft-purple: #C4B5FD;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body, .stApp {
  background: var(--bg1) !important;
  font-family: 'Inter', sans-serif;
  color: var(--white);
}

/* Hide Streamlit chrome */
#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb { background: var(--purple); border-radius: 3px; }

/* Animations */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50%       { transform: translateY(-20px) rotate(5deg); }
}
@keyframes float2 {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50%       { transform: translateY(-15px) rotate(-5deg); }
}
@keyframes glow-pulse {
  0%, 100% { box-shadow: 0 0 20px rgba(124,58,237,0.4); }
  50%       { box-shadow: 0 0 40px rgba(124,58,237,0.8), 0 0 80px rgba(79,140,255,0.3); }
}
@keyframes counter {
  from { opacity: 0; transform: scale(0.5); }
  to   { opacity: 1; transform: scale(1); }
}
@keyframes slide-in-left {
  from { opacity: 0; transform: translateX(-40px); }
  to   { opacity: 1; transform: translateX(0); }
}
@keyframes spin-slow {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}
@keyframes gradient-shift {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
</style>
"""

# ─────────────────────────────────────────────
# LANDING PAGE
# ─────────────────────────────────────────────
LANDING_HTML = """
<style>
/* ── NAV ── */
.lp-nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 48px;
  background: rgba(9,0,20,0.6);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(124,58,237,0.2);
  transition: all 0.3s ease;
}
.lp-logo {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 22px; font-weight: 700;
  background: linear-gradient(135deg, #8B5CF6, #22D3EE);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  letter-spacing: -0.5px;
}
.lp-logo span { color: #EC4899; -webkit-text-fill-color: #EC4899; }
.lp-links { display: flex; gap: 32px; list-style: none; }
.lp-links a {
  color: #94A3B8; font-size: 14px; font-weight: 500;
  text-decoration: none; transition: color 0.2s;
}
.lp-links a:hover { color: #fff; }
.lp-nav-btns { display: flex; gap: 12px; }
.btn-ghost {
  background: transparent;
  border: 1px solid rgba(139,92,246,0.5);
  color: #8B5CF6; padding: 9px 20px; border-radius: 8px;
  font-size: 13px; font-weight: 600; cursor: pointer;
  transition: all 0.2s; text-decoration: none; display: inline-block;
}
.btn-ghost:hover { background: rgba(139,92,246,0.1); border-color: #8B5CF6; }
.btn-primary {
  background: linear-gradient(135deg, #7C3AED, #4F8CFF);
  border: none; color: #fff; padding: 9px 20px; border-radius: 8px;
  font-size: 13px; font-weight: 600; cursor: pointer;
  transition: all 0.3s; text-decoration: none; display: inline-block;
  animation: glow-pulse 2.5s infinite;
}
.btn-primary:hover { transform: translateY(-2px); filter: brightness(1.15); }

/* ── HERO ── */
.lp-hero {
  min-height: 100vh;
  background: radial-gradient(ellipse 80% 60% at 50% 0%, rgba(124,58,237,0.25) 0%, transparent 70%),
              radial-gradient(ellipse 60% 40% at 80% 50%, rgba(79,140,255,0.15) 0%, transparent 60%),
              radial-gradient(ellipse 40% 30% at 20% 80%, rgba(34,211,238,0.1) 0%, transparent 50%),
              linear-gradient(180deg, #090014 0%, #12002B 50%, #1A063A 100%);
  display: flex; align-items: center; justify-content: center;
  text-align: center; padding: 120px 24px 80px; position: relative; overflow: hidden;
}
.hero-blob {
  position: absolute; border-radius: 50%; filter: blur(80px); pointer-events: none;
}
.blob1 {
  width: 500px; height: 500px; top: -100px; left: -100px;
  background: radial-gradient(circle, rgba(124,58,237,0.3), transparent 70%);
  animation: float 8s ease-in-out infinite;
}
.blob2 {
  width: 400px; height: 400px; bottom: -50px; right: -80px;
  background: radial-gradient(circle, rgba(79,140,255,0.25), transparent 70%);
  animation: float2 10s ease-in-out infinite;
}
.blob3 {
  width: 300px; height: 300px; top: 40%; left: 60%;
  background: radial-gradient(circle, rgba(34,211,238,0.15), transparent 70%);
  animation: float 12s ease-in-out infinite reverse;
}
.hero-badge {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(124,58,237,0.15); border: 1px solid rgba(124,58,237,0.4);
  border-radius: 50px; padding: 6px 16px; margin-bottom: 28px;
  font-size: 12px; font-weight: 600; color: #C4B5FD;
  animation: fadeInUp 0.8s ease both;
}
.hero-badge-dot { width: 6px; height: 6px; background: #22D3EE; border-radius: 50%; animation: glow-pulse 1.5s infinite; }
.hero-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(42px, 7vw, 88px); font-weight: 800; line-height: 1.05;
  letter-spacing: -2px; margin-bottom: 24px;
  animation: fadeInUp 0.8s 0.1s ease both;
}
.hero-title .grad {
  background: linear-gradient(135deg, #8B5CF6 0%, #4F8CFF 40%, #22D3EE 80%);
  background-size: 200% 200%; animation: gradient-shift 4s ease infinite;
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub {
  font-size: 18px; color: #94A3B8; max-width: 560px; margin: 0 auto 40px;
  line-height: 1.7; animation: fadeInUp 0.8s 0.2s ease both;
}
.hero-btns {
  display: flex; gap: 16px; justify-content: center; flex-wrap: wrap;
  animation: fadeInUp 0.8s 0.3s ease both;
}
.btn-hero-primary {
  background: linear-gradient(135deg, #7C3AED, #4F8CFF);
  color: #fff; padding: 14px 36px; border-radius: 12px; border: none;
  font-size: 15px; font-weight: 700; cursor: pointer; text-decoration: none;
  display: inline-block; transition: all 0.3s;
  box-shadow: 0 0 30px rgba(124,58,237,0.5);
}
.btn-hero-primary:hover { transform: translateY(-3px); box-shadow: 0 0 50px rgba(124,58,237,0.7); }
.btn-hero-ghost {
  background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.15);
  color: #fff; padding: 14px 36px; border-radius: 12px;
  font-size: 15px; font-weight: 600; cursor: pointer; text-decoration: none;
  display: inline-block; transition: all 0.3s; backdrop-filter: blur(10px);
}
.btn-hero-ghost:hover { background: rgba(255,255,255,0.1); transform: translateY(-3px); }

/* ── TRUSTED BY ── */
.lp-trusted {
  padding: 64px 48px;
  background: rgba(18,0,43,0.8);
  border-top: 1px solid rgba(124,58,237,0.1);
  border-bottom: 1px solid rgba(124,58,237,0.1);
  text-align: center;
}
.trusted-label { font-size: 12px; font-weight: 600; color: #64748B; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 36px; }
.trusted-logos { display: flex; gap: 48px; justify-content: center; align-items: center; flex-wrap: wrap; }
.trusted-logo {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 18px; font-weight: 700; color: #334155;
  transition: color 0.3s; cursor: default;
}
.trusted-logo:hover { color: #8B5CF6; }

/* ── FEATURES ── */
.lp-features {
  padding: 100px 48px;
  background: linear-gradient(180deg, #090014, #12002B);
}
.section-label {
  text-align: center; font-size: 12px; font-weight: 700;
  color: #8B5CF6; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 16px;
}
.section-title {
  text-align: center; font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(28px, 4vw, 48px); font-weight: 700; margin-bottom: 16px;
}
.section-sub {
  text-align: center; color: #64748B; max-width: 500px;
  margin: 0 auto 64px; font-size: 16px; line-height: 1.7;
}
.features-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px; max-width: 1100px; margin: 0 auto;
}
.feature-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(124,58,237,0.2);
  border-radius: 20px; padding: 32px;
  transition: all 0.3s; position: relative; overflow: hidden;
  backdrop-filter: blur(10px);
}
.feature-card::before {
  content: ''; position: absolute; inset: 0; border-radius: 20px;
  background: linear-gradient(135deg, rgba(124,58,237,0.1), transparent);
  opacity: 0; transition: opacity 0.3s;
}
.feature-card:hover { border-color: rgba(124,58,237,0.6); transform: translateY(-6px); box-shadow: 0 20px 60px rgba(124,58,237,0.2); }
.feature-card:hover::before { opacity: 1; }
.feature-icon {
  width: 52px; height: 52px; border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  font-size: 24px; margin-bottom: 20px;
}
.feature-title { font-size: 17px; font-weight: 700; margin-bottom: 10px; }
.feature-desc { font-size: 14px; color: #64748B; line-height: 1.7; }

/* ── STATS ── */
.lp-stats {
  padding: 80px 48px;
  background: radial-gradient(ellipse 80% 60% at 50% 50%, rgba(124,58,237,0.12) 0%, transparent 70%),
              linear-gradient(180deg, #12002B, #1A063A);
  text-align: center;
}
.stats-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 32px; max-width: 900px; margin: 0 auto;
}
.stat-card {
  padding: 40px 24px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(124,58,237,0.2);
  border-radius: 20px; backdrop-filter: blur(10px);
  transition: transform 0.3s;
}
.stat-card:hover { transform: translateY(-4px); }
.stat-num {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 48px; font-weight: 800; line-height: 1;
  background: linear-gradient(135deg, #8B5CF6, #22D3EE);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  margin-bottom: 8px;
}
.stat-label { font-size: 14px; color: #64748B; font-weight: 500; }

/* ── TESTIMONIALS ── */
.lp-testimonials { padding: 100px 48px; background: linear-gradient(180deg, #1A063A, #090014); }
.testi-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px; max-width: 1000px; margin: 0 auto;
}
.testi-card {
  background: rgba(255,255,255,0.03); border: 1px solid rgba(124,58,237,0.15);
  border-radius: 20px; padding: 32px; backdrop-filter: blur(10px);
  transition: all 0.3s;
}
.testi-card:hover { border-color: rgba(124,58,237,0.4); transform: translateY(-4px); }
.testi-stars { color: #F59E0B; font-size: 14px; margin-bottom: 16px; }
.testi-text { color: #94A3B8; font-size: 14px; line-height: 1.8; margin-bottom: 24px; font-style: italic; }
.testi-author { display: flex; align-items: center; gap: 14px; }
.testi-avatar {
  width: 44px; height: 44px; border-radius: 50%;
  background: linear-gradient(135deg, #7C3AED, #22D3EE);
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 16px; flex-shrink: 0;
}
.testi-name { font-weight: 600; font-size: 14px; }
.testi-role { font-size: 12px; color: #64748B; }

/* ── PRICING ── */
.lp-pricing { padding: 100px 48px; background: linear-gradient(180deg, #090014, #12002B); }
.pricing-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px; max-width: 980px; margin: 0 auto;
}
.pricing-card {
  background: rgba(255,255,255,0.03); border: 1px solid rgba(124,58,237,0.2);
  border-radius: 24px; padding: 40px 32px; text-align: center;
  transition: all 0.3s; position: relative; overflow: hidden;
}
.pricing-card.featured {
  background: linear-gradient(145deg, rgba(124,58,237,0.2), rgba(79,140,255,0.1));
  border-color: #7C3AED;
  box-shadow: 0 0 60px rgba(124,58,237,0.3);
  transform: scale(1.04);
}
.pricing-card:hover { transform: translateY(-8px); border-color: rgba(124,58,237,0.5); }
.pricing-card.featured:hover { transform: scale(1.04) translateY(-8px); }
.pricing-badge {
  position: absolute; top: 20px; right: 20px;
  background: linear-gradient(135deg, #7C3AED, #4F8CFF);
  color: #fff; font-size: 11px; font-weight: 700;
  padding: 4px 12px; border-radius: 50px; letter-spacing: 1px;
}
.pricing-tier { font-size: 13px; font-weight: 600; color: #8B5CF6; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 12px; }
.pricing-price {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 52px; font-weight: 800; margin-bottom: 4px;
}
.pricing-price span { font-size: 20px; font-weight: 500; color: #64748B; }
.pricing-desc { font-size: 13px; color: #64748B; margin-bottom: 32px; }
.pricing-features { list-style: none; text-align: left; margin-bottom: 32px; display: flex; flex-direction: column; gap: 12px; }
.pricing-features li { font-size: 14px; color: #94A3B8; display: flex; align-items: center; gap: 10px; }
.pricing-features li::before { content: '✓'; color: #22D3EE; font-weight: 700; flex-shrink: 0; }

/* ── FAQ ── */
.lp-faq { padding: 100px 48px; background: linear-gradient(180deg, #12002B, #1A063A); }
.faq-list { max-width: 720px; margin: 0 auto; display: flex; flex-direction: column; gap: 12px; }
.faq-item {
  background: rgba(255,255,255,0.03); border: 1px solid rgba(124,58,237,0.2);
  border-radius: 16px; overflow: hidden; transition: border-color 0.3s;
}
.faq-item:hover { border-color: rgba(124,58,237,0.5); }
.faq-q {
  width: 100%; background: transparent; border: none; color: #fff;
  font-size: 15px; font-weight: 600; padding: 20px 24px;
  cursor: pointer; text-align: left; display: flex; justify-content: space-between; align-items: center;
  font-family: 'Inter', sans-serif;
}
.faq-a { padding: 0 24px 20px; color: #64748B; font-size: 14px; line-height: 1.8; display: none; }
.faq-item.open .faq-a { display: block; }
.faq-item.open .faq-chevron { transform: rotate(180deg); }
.faq-chevron { transition: transform 0.3s; font-size: 12px; color: #8B5CF6; }

/* ── CTA SECTION ── */
.lp-cta {
  padding: 100px 48px; text-align: center;
  background: radial-gradient(ellipse 80% 60% at 50% 50%, rgba(124,58,237,0.2) 0%, transparent 70%),
              linear-gradient(180deg, #1A063A, #090014);
}
.cta-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(32px, 5vw, 60px); font-weight: 800; margin-bottom: 20px;
}
.cta-sub { color: #64748B; font-size: 17px; max-width: 500px; margin: 0 auto 40px; line-height: 1.7; }
.btn-cta {
  background: linear-gradient(135deg, #7C3AED, #4F8CFF, #22D3EE);
  background-size: 200% 200%; animation: gradient-shift 3s ease infinite, glow-pulse 2s ease infinite;
  color: #fff; padding: 18px 48px; border-radius: 14px; border: none;
  font-size: 17px; font-weight: 700; cursor: pointer; text-decoration: none; display: inline-block;
  letter-spacing: 0.3px; transition: transform 0.3s;
}
.btn-cta:hover { transform: translateY(-4px) scale(1.03); }

/* ── FOOTER ── */
.lp-footer {
  padding: 60px 48px 32px;
  background: #050010;
  border-top: 1px solid rgba(124,58,237,0.15);
}
.footer-top {
  display: grid; grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 48px; margin-bottom: 48px;
}
.footer-brand p { color: #475569; font-size: 14px; line-height: 1.7; margin-top: 12px; max-width: 260px; }
.footer-col h4 { font-size: 13px; font-weight: 700; color: #8B5CF6; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 16px; }
.footer-col a { display: block; color: #475569; font-size: 14px; text-decoration: none; margin-bottom: 8px; transition: color 0.2s; }
.footer-col a:hover { color: #8B5CF6; }
.footer-socials { display: flex; gap: 12px; margin-top: 16px; }
.social-icon {
  width: 36px; height: 36px; border-radius: 8px;
  background: rgba(124,58,237,0.15); border: 1px solid rgba(124,58,237,0.3);
  display: flex; align-items: center; justify-content: center;
  font-size: 16px; text-decoration: none; transition: all 0.2s;
}
.social-icon:hover { background: rgba(124,58,237,0.3); transform: translateY(-2px); }
.footer-bottom {
  border-top: 1px solid rgba(124,58,237,0.1); padding-top: 24px;
  display: flex; justify-content: space-between; align-items: center;
  color: #334155; font-size: 13px; flex-wrap: wrap; gap: 12px;
}
</style>

<!-- NAVBAR -->
<nav class="lp-nav" id="navbar">
  <div class="lp-logo">Performa<span>AI</span></div>
  <ul class="lp-links">
    <li><a href="#features">Features</a></li>
    <li><a href="#pricing">Pricing</a></li>
    <li><a href="#testimonials">About</a></li>
    <li><a href="#faq">FAQ</a></li>
  </ul>
  <div class="lp-nav-btns">
    <a href="?page=login" class="btn-ghost">Login</a>
    <a href="?page=signup" class="btn-primary">Sign Up</a>
  </div>
</nav>

<!-- HERO -->
<section class="lp-hero">
  <div class="hero-blob blob1"></div>
  <div class="hero-blob blob2"></div>
  <div class="hero-blob blob3"></div>
  <div style="position:relative;z-index:2;">
    <div class="hero-badge">
      <div class="hero-badge-dot"></div>
      Powered by Machine Learning &amp; Random Forest AI
    </div>
    <h1 class="hero-title">
      Predict Employee<br>
      <span class="grad">Performance with AI</span>
    </h1>
    <p class="hero-sub">
      Give your HR team a superpower. Instantly predict performance ratings,
      identify at-risk employees, and make data-driven workforce decisions.
    </p>
    <div class="hero-btns">
      <a href="?page=signup" class="btn-hero-primary">🚀 Get Started Free</a>
      <a href="#features" class="btn-hero-ghost">✦ See How It Works</a>
    </div>
  </div>
</section>

<!-- TRUSTED BY -->
<section class="lp-trusted">
  <p class="trusted-label">Trusted by teams at</p>
  <div class="trusted-logos">
    <span class="trusted-logo">Microsoft</span>
    <span class="trusted-logo">Google</span>
    <span class="trusted-logo">Amazon</span>
    <span class="trusted-logo">Nvidia</span>
    <span class="trusted-logo">OpenAI</span>
    <span class="trusted-logo">Tesla</span>
  </div>
</section>

<!-- FEATURES -->
<section class="lp-features" id="features">
  <p class="section-label">Why PerformaAI</p>
  <h2 class="section-title">Everything your HR team needs</h2>
  <p class="section-sub">From real-time predictions to deep analytics — built for modern HR professionals.</p>
  <div class="features-grid">
    <div class="feature-card">
      <div class="feature-icon" style="background:rgba(124,58,237,0.15);">🤖</div>
      <div class="feature-title">AI Prediction Engine</div>
      <div class="feature-desc">Random Forest model trained on real HR data predicts performance with high accuracy across 4 rating tiers.</div>
    </div>
    <div class="feature-card">
      <div class="feature-icon" style="background:rgba(79,140,255,0.15);">📊</div>
      <div class="feature-title">Live Analytics Dashboard</div>
      <div class="feature-desc">Interactive charts — feature importance, heatmaps, department comparisons — updated in real time.</div>
    </div>
    <div class="feature-card">
      <div class="feature-icon" style="background:rgba(34,211,238,0.15);">☁️</div>
      <div class="feature-title">Cloud-Ready Deploy</div>
      <div class="feature-desc">One-click deploy to Streamlit Cloud. No servers, no DevOps. Your app is live in minutes.</div>
    </div>
    <div class="feature-card">
      <div class="feature-icon" style="background:rgba(236,72,153,0.15);">🔐</div>
      <div class="feature-title">Role-Based Security</div>
      <div class="feature-desc">HR-only access with secure login, hashed passwords, and session management baked in.</div>
    </div>
    <div class="feature-card">
      <div class="feature-icon" style="background:rgba(245,158,11,0.15);">👥</div>
      <div class="feature-title">Bulk Predictions</div>
      <div class="feature-desc">Upload a CSV of your entire department and get predictions for all employees in one click.</div>
    </div>
    <div class="feature-card">
      <div class="feature-icon" style="background:rgba(124,58,237,0.15);">🔌</div>
      <div class="feature-title">No Database Required</div>
      <div class="feature-desc">All data stored in lightweight CSV and model files. Easy to set up, easy to move, easy to audit.</div>
    </div>
  </div>
</section>

<!-- STATS -->
<section class="lp-stats">
  <p class="section-label">By the numbers</p>
  <h2 class="section-title" style="margin-bottom:48px;">Trusted. Tested. Proven.</h2>
  <div class="stats-grid">
    <div class="stat-card"><div class="stat-num">10K+</div><div class="stat-label">Users Worldwide</div></div>
    <div class="stat-card"><div class="stat-num">500+</div><div class="stat-label">Businesses Using It</div></div>
    <div class="stat-card"><div class="stat-num">99.9%</div><div class="stat-label">Uptime Guaranteed</div></div>
    <div class="stat-card"><div class="stat-num">24/7</div><div class="stat-label">Support Available</div></div>
  </div>
</section>

<!-- TESTIMONIALS -->
<section class="lp-testimonials" id="testimonials">
  <p class="section-label">Testimonials</p>
  <h2 class="section-title">What HR leaders say</h2>
  <p class="section-sub">Real feedback from real teams using PerformaAI.</p>
  <div class="testi-grid">
    <div class="testi-card">
      <div class="testi-stars">★★★★★</div>
      <p class="testi-text">"PerformaAI transformed how we approach performance reviews. We spotted three at-risk employees before their annual review — and retained all of them."</p>
      <div class="testi-author">
        <div class="testi-avatar">S</div>
        <div><div class="testi-name">Sarah Mitchell</div><div class="testi-role">Head of HR · TechVenture Co.</div></div>
      </div>
    </div>
    <div class="testi-card">
      <div class="testi-stars">★★★★★</div>
      <p class="testi-text">"The analytics dashboard alone is worth it. Our leadership team finally has a visual story behind every performance decision. No more gut-feel."</p>
      <div class="testi-author">
        <div class="testi-avatar" style="background:linear-gradient(135deg,#22D3EE,#4F8CFF);">R</div>
        <div><div class="testi-name">Raj Patel</div><div class="testi-role">VP People Operations · ScaleUp Ltd.</div></div>
      </div>
    </div>
    <div class="testi-card">
      <div class="testi-stars">★★★★★</div>
      <p class="testi-text">"Deployed in one afternoon. No database setup, no DevOps headache. The prediction accuracy surprised us — it matched our manual reviews closely."</p>
      <div class="testi-author">
        <div class="testi-avatar" style="background:linear-gradient(135deg,#EC4899,#F59E0B);">A</div>
        <div><div class="testi-name">Anika Joshi</div><div class="testi-role">HR Director · GlobalEdge Inc.</div></div>
      </div>
    </div>
  </div>
</section>

<!-- PRICING -->
<section class="lp-pricing" id="pricing">
  <p class="section-label">Pricing</p>
  <h2 class="section-title">Simple, transparent plans</h2>
  <p class="section-sub">Start free, scale as you grow. No hidden fees.</p>
  <div class="pricing-grid">
    <div class="pricing-card">
      <div class="pricing-tier">Starter</div>
      <div class="pricing-price">Free<span>/mo</span></div>
      <p class="pricing-desc">Perfect for small teams just getting started.</p>
      <ul class="pricing-features">
        <li>Up to 50 predictions/month</li>
        <li>Basic analytics dashboard</li>
        <li>2 HR user accounts</li>
        <li>CSV upload (up to 50 rows)</li>
        <li>Community support</li>
      </ul>
      <a href="?page=signup" class="btn-ghost" style="width:100%;text-align:center;display:block;">Get Started</a>
    </div>
    <div class="pricing-card featured">
      <div class="pricing-badge">MOST POPULAR</div>
      <div class="pricing-tier">Pro</div>
      <div class="pricing-price">₹2,499<span>/mo</span></div>
      <p class="pricing-desc">For growing HR teams that need more power.</p>
      <ul class="pricing-features">
        <li>Unlimited predictions</li>
        <li>Full analytics + heatmaps</li>
        <li>10 HR user accounts</li>
        <li>Bulk CSV predictions (unlimited)</li>
        <li>PDF report exports</li>
        <li>Priority support</li>
      </ul>
      <a href="?page=signup" class="btn-primary" style="width:100%;text-align:center;display:block;padding:12px;">Start Pro Trial</a>
    </div>
    <div class="pricing-card">
      <div class="pricing-tier">Enterprise</div>
      <div class="pricing-price">Custom<span></span></div>
      <p class="pricing-desc">For large organizations with custom needs.</p>
      <ul class="pricing-features">
        <li>Everything in Pro</li>
        <li>Custom ML model training</li>
        <li>Unlimited user accounts</li>
        <li>SSO &amp; LDAP integration</li>
        <li>Dedicated account manager</li>
        <li>SLA guarantee</li>
      </ul>
      <a href="?page=signup" class="btn-ghost" style="width:100%;text-align:center;display:block;">Contact Sales</a>
    </div>
  </div>
</section>

<!-- FAQ -->
<section class="lp-faq" id="faq">
  <p class="section-label">FAQ</p>
  <h2 class="section-title">Common questions</h2>
  <p class="section-sub">Everything you need to know before getting started.</p>
  <div class="faq-list">
    <div class="faq-item">
      <button class="faq-q" onclick="this.parentElement.classList.toggle('open')">
        Do I need a database to use PerformaAI? <span class="faq-chevron">▼</span>
      </button>
      <div class="faq-a">No. PerformaAI is entirely database-free. Your data lives in lightweight CSV and model files, making it easy to set up and maintain without any backend infrastructure.</div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="this.parentElement.classList.toggle('open')">
        How accurate is the performance prediction? <span class="faq-chevron">▼</span>
      </button>
      <div class="faq-a">Our Random Forest model achieves 55–70% accuracy on 4-class prediction benchmarks, which is 2–3x better than random guessing. Results improve significantly with larger real-world datasets.</div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="this.parentElement.classList.toggle('open')">
        Can I use my own company's HR data? <span class="faq-chevron">▼</span>
      </button>
      <div class="faq-a">Yes. Simply replace the included CSV with your own dataset (matching the column format) and re-run train_model.py. The model will retrain on your data automatically.</div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="this.parentElement.classList.toggle('open')">
        How do I add new HR users? <span class="faq-chevron">▼</span>
      </button>
      <div class="faq-a">New accounts can be created via the Sign Up page. All passwords are securely hashed using SHA-256 and stored in a local JSON file. You can also manually edit auth/users.json to add users.</div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="this.parentElement.classList.toggle('open')">
        Is this built for my final year project? <span class="faq-chevron">▼</span>
      </button>
      <div class="faq-a">Yes! This entire system — ML model, authentication, analytics, and this landing page — was built as a final year project showcase. All code is yours to own, modify, and present.</div>
    </div>
  </div>
</section>

<!-- CTA -->
<section class="lp-cta">
  <h2 class="cta-title">Ready to predict<br><span style="background:linear-gradient(135deg,#8B5CF6,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">performance?</span></h2>
  <p class="cta-sub">Join HR teams who use data, not guesswork, to manage and grow their workforce.</p>
  <a href="?page=signup" class="btn-cta">🚀 Start Your Free Trial</a>
</section>

<!-- FOOTER -->
<footer class="lp-footer">
  <div class="footer-top">
    <div class="footer-brand">
      <div class="lp-logo">Performa<span style="-webkit-text-fill-color:#EC4899;color:#EC4899">AI</span></div>
      <p>AI-powered HR analytics for modern teams. Predict performance, reduce attrition, and make smarter people decisions.</p>
      <div class="footer-socials">
        <a class="social-icon" href="#">🐦</a>
        <a class="social-icon" href="#">💼</a>
        <a class="social-icon" href="#">🐙</a>
        <a class="social-icon" href="#">📘</a>
      </div>
    </div>
    <div class="footer-col">
      <h4>Product</h4>
      <a href="#">Features</a>
      <a href="#">Pricing</a>
      <a href="#">Changelog</a>
      <a href="#">Roadmap</a>
    </div>
    <div class="footer-col">
      <h4>Company</h4>
      <a href="#">About</a>
      <a href="#">Blog</a>
      <a href="#">Careers</a>
      <a href="#">Contact</a>
    </div>
    <div class="footer-col">
      <h4>Legal</h4>
      <a href="#">Privacy</a>
      <a href="#">Terms</a>
      <a href="#">Security</a>
      <a href="#">Cookies</a>
    </div>
  </div>
  <div class="footer-bottom">
    <span>© 2025 PerformaAI. All rights reserved.</span>
    <span>Made with 💜 for Final Year Projects</span>
  </div>
</footer>
"""

# ─────────────────────────────────────────────
# LOGIN PAGE
# ─────────────────────────────────────────────
LOGIN_HTML_STYLE = """
<style>
.auth-wrap {
  min-height: 100vh;
  background: radial-gradient(ellipse 80% 60% at 30% 50%, rgba(124,58,237,0.2), transparent 60%),
              radial-gradient(ellipse 60% 50% at 80% 60%, rgba(79,140,255,0.15), transparent 60%),
              linear-gradient(135deg, #090014, #12002B, #1A063A);
  display: flex; align-items: center; justify-content: center;
  padding: 40px 20px; font-family: 'Inter', sans-serif;
}
.auth-card {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(124,58,237,0.3);
  border-radius: 28px; padding: 48px 44px;
  width: 100%; max-width: 440px;
  backdrop-filter: blur(30px);
  box-shadow: 0 0 80px rgba(124,58,237,0.15), 0 40px 80px rgba(0,0,0,0.5);
  animation: fadeInUp 0.6s ease both;
}
.auth-logo {
  text-align: center; margin-bottom: 8px;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 26px; font-weight: 800;
  background: linear-gradient(135deg, #8B5CF6, #22D3EE);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.auth-tagline { text-align: center; color: #475569; font-size: 13px; margin-bottom: 36px; }
.auth-title { font-size: 22px; font-weight: 700; margin-bottom: 6px; }
.auth-sub { color: #64748B; font-size: 14px; margin-bottom: 28px; }
.form-group { margin-bottom: 18px; }
.form-label { font-size: 13px; font-weight: 600; color: #94A3B8; margin-bottom: 8px; display: block; }
.form-input {
  width: 100%; background: rgba(255,255,255,0.05);
  border: 1px solid rgba(124,58,237,0.25); border-radius: 12px;
  padding: 13px 16px; color: #fff; font-size: 14px;
  font-family: 'Inter', sans-serif; transition: all 0.2s; outline: none;
  box-sizing: border-box;
}
.form-input:focus { border-color: #8B5CF6; box-shadow: 0 0 0 3px rgba(139,92,246,0.15); }
.form-input::placeholder { color: #334155; }
.form-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.form-check { display: flex; align-items: center; gap: 8px; font-size: 13px; color: #64748B; }
.form-check input { accent-color: #8B5CF6; }
.form-link { font-size: 13px; color: #8B5CF6; text-decoration: none; font-weight: 500; }
.form-link:hover { color: #A78BFA; }
.btn-submit {
  width: 100%; background: linear-gradient(135deg, #7C3AED, #4F8CFF);
  color: #fff; border: none; border-radius: 12px;
  padding: 14px; font-size: 15px; font-weight: 700;
  cursor: pointer; font-family: 'Inter', sans-serif;
  transition: all 0.3s; margin-bottom: 20px;
  box-shadow: 0 0 30px rgba(124,58,237,0.4);
}
.btn-submit:hover { transform: translateY(-2px); box-shadow: 0 0 50px rgba(124,58,237,0.6); }
.divider { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
.divider-line { flex: 1; height: 1px; background: rgba(124,58,237,0.2); }
.divider-text { font-size: 12px; color: #334155; font-weight: 500; }
.social-btns { display: flex; gap: 12px; margin-bottom: 28px; }
.btn-social {
  flex: 1; background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px; padding: 11px; font-size: 13px;
  color: #94A3B8; font-weight: 600; cursor: pointer;
  font-family: 'Inter', sans-serif; transition: all 0.2s;
}
.btn-social:hover { background: rgba(255,255,255,0.08); border-color: rgba(255,255,255,0.2); color: #fff; }
.auth-footer-text { text-align: center; font-size: 13px; color: #475569; }
.auth-back {
  display: inline-flex; align-items: center; gap: 6px;
  color: #64748B; font-size: 13px; text-decoration: none;
  margin-bottom: 28px; transition: color 0.2s; font-weight: 500;
}
.auth-back:hover { color: #8B5CF6; }
</style>
"""

# ─────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────

def _get_page() -> str:
    """Read ?page= query param from the URL."""
    params = st.query_params
    return params.get("page", "landing")


def _set_page(page: str):
    st.query_params["page"] = page


def show_landing():
    st.markdown(GLOBAL_CSS + LANDING_HTML, unsafe_allow_html=True)


def show_login():
    st.markdown(GLOBAL_CSS + LOGIN_HTML_STYLE, unsafe_allow_html=True)

    st.markdown('<div class="auth-wrap"><div class="auth-card">', unsafe_allow_html=True)
    st.markdown('<div class="auth-logo">PerformaAI</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-tagline">HR Intelligence Platform</div>', unsafe_allow_html=True)

    col_back, _ = st.columns([1, 3])
    with col_back:
        if st.button("← Back to Home", key="login_back"):
            _set_page("landing")
            st.rerun()

    st.markdown('<div class="auth-title">Welcome back 👋</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-sub">Sign in to your HR dashboard</div>', unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="Enter your username", key="login_user")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pass")

    col1, col2 = st.columns(2)
    with col1:
        remember = st.checkbox("Remember me", key="remember_me")
    with col2:
        st.markdown('<div style="text-align:right;"><a class="form-link" href="#">Forgot password?</a></div>', unsafe_allow_html=True)

    if st.button("🔐 Login", key="login_btn", use_container_width=True, type="primary"):
        if not username or not password:
            st.error("Please fill in all fields.")
        else:
            users = _load_users()
            if username in users and users[username]["password"] == _hash(password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.session_state["name"] = users[username]["name"]
                st.session_state["role"] = users[username]["role"]
                _set_page("dashboard")
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")

    st.markdown("""
    <div class="divider">
      <div class="divider-line"></div>
      <div class="divider-text">OR CONTINUE WITH</div>
      <div class="divider-line"></div>
    </div>
    <div class="social-btns">
      <button class="btn-social">🔵 Google</button>
      <button class="btn-social">⚫ GitHub</button>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        'Don\'t have an account? &nbsp;',
        unsafe_allow_html=True,
    )
    if st.button("Sign Up →", key="go_signup"):
        _set_page("signup")
        st.rerun()

    st.markdown('</div></div>', unsafe_allow_html=True)


def show_signup():
    st.markdown(GLOBAL_CSS + LOGIN_HTML_STYLE, unsafe_allow_html=True)
    st.markdown('<div class="auth-wrap"><div class="auth-card">', unsafe_allow_html=True)
    st.markdown('<div class="auth-logo">PerformaAI</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-tagline">HR Intelligence Platform</div>', unsafe_allow_html=True)

    col_back, _ = st.columns([1, 3])
    with col_back:
        if st.button("← Back", key="signup_back"):
            _set_page("landing")
            st.rerun()

    st.markdown('<div class="auth-title">Create your account ✨</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-sub">Join your HR team on PerformaAI</div>', unsafe_allow_html=True)

    full_name = st.text_input("Full Name", placeholder="e.g. Sarah Mitchell", key="su_name")
    username  = st.text_input("Username", placeholder="e.g. sarah_hr", key="su_user")
    email     = st.text_input("Email", placeholder="sarah@company.com", key="su_email")
    password  = st.text_input("Password", type="password", placeholder="Min. 6 characters", key="su_pass")
    confirm   = st.text_input("Confirm Password", type="password", placeholder="Repeat password", key="su_confirm")
    terms     = st.checkbox("I accept the Terms of Service and Privacy Policy", key="su_terms")

    if st.button("🚀 Create Account", key="signup_btn", use_container_width=True, type="primary"):
        errors = []
        if not all([full_name, username, email, password, confirm]):
            errors.append("All fields are required.")
        if password and len(password) < 6:
            errors.append("Password must be at least 6 characters.")
        if password != confirm:
            errors.append("Passwords do not match.")
        if email and not _validate_email(email):
            errors.append("Enter a valid email address.")
        if not terms:
            errors.append("You must accept the Terms of Service.")

        users = _load_users()
        if username in users:
            errors.append("Username already taken. Choose another.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            users[username] = {
                "name": full_name,
                "email": email,
                "password": _hash(password),
                "role": "hr",
            }
            _save_users(users)
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["name"] = full_name
            st.session_state["role"] = "hr"
            st.success("🎉 Account created! Redirecting to dashboard...")
            _set_page("dashboard")
            st.rerun()

    st.markdown("""
    <div class="divider" style="margin-top:16px;">
      <div class="divider-line"></div>
      <div class="divider-text">OR SIGN UP WITH</div>
      <div class="divider-line"></div>
    </div>
    <div class="social-btns">
      <button class="btn-social">🔵 Google</button>
      <button class="btn-social">⚫ GitHub</button>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("Already have an account? &nbsp;", unsafe_allow_html=True)
    if st.button("Login →", key="go_login"):
        _set_page("login")
        st.rerun()

    st.markdown('</div></div>', unsafe_allow_html=True)


def logout():
    """Call this from app.py to log the current user out."""
    for key in ["authenticated", "username", "name", "role"]:
        st.session_state.pop(key, None)
    _set_page("landing")
    st.rerun()


def require_auth() -> bool:
    """
    Main auth gate.  Call at the top of app.py:

        from auth.auth import require_auth, logout
        if not require_auth():
            st.stop()

    Returns True only when a user is logged in.
    Shows the landing / login / signup pages otherwise.
    """
    page = _get_page()

    # Already logged in → go to dashboard regardless of URL
    if st.session_state.get("authenticated"):
        return True

    if page == "login":
        show_login()
    elif page == "signup":
        show_signup()
    else:
        show_landing()

    return False

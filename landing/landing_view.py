import streamlit as st
from components.navbar import render_public_navbar
from components.footer import render_footer
from utils.session import set_page

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;600;700;800&display=swap');
* { box-sizing:border-box;margin:0;padding:0; }
body,.stApp { background:#090014 !important; font-family:'Inter',sans-serif; color:#fff; }
#MainMenu,footer,header,.stDeployButton { display:none !important; }
.block-container { padding:0 !important; max-width:100% !important; }
[data-testid="stVerticalBlock"] { gap:0 !important; }
::-webkit-scrollbar { width:6px; }
::-webkit-scrollbar-thumb { background:#7C3AED; border-radius:3px; }
@keyframes fadeInUp { from{opacity:0;transform:translateY(30px)} to{opacity:1;transform:translateY(0)} }
@keyframes float    { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-20px)} }
@keyframes float2   { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-14px)} }
@keyframes glow-pulse { 0%,100%{box-shadow:0 0 20px rgba(124,58,237,.4)} 50%{box-shadow:0 0 50px rgba(124,58,237,.8)} }
@keyframes gradient-shift { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
</style>
"""

LANDING_HTML = """
<style>
/* HERO */
.hero {
  min-height:100vh;
  background:radial-gradient(ellipse 80% 60% at 50% 0%,rgba(124,58,237,.25),transparent 70%),
             radial-gradient(ellipse 50% 40% at 80% 50%,rgba(79,140,255,.15),transparent 60%),
             radial-gradient(ellipse 40% 30% at 20% 80%,rgba(34,211,238,.1),transparent 50%),
             linear-gradient(180deg,#090014,#12002B 60%,#1A063A);
  display:flex;align-items:center;justify-content:center;
  text-align:center;padding:140px 24px 80px;position:relative;overflow:hidden;
}
.blob { position:absolute;border-radius:50%;filter:blur(80px);pointer-events:none; }
.b1 { width:500px;height:500px;top:-100px;left:-100px;background:radial-gradient(circle,rgba(124,58,237,.3),transparent 70%);animation:float 8s ease-in-out infinite; }
.b2 { width:400px;height:400px;bottom:-50px;right:-80px;background:radial-gradient(circle,rgba(79,140,255,.25),transparent 70%);animation:float2 10s ease-in-out infinite; }
.b3 { width:300px;height:300px;top:40%;left:60%;background:radial-gradient(circle,rgba(34,211,238,.15),transparent 70%);animation:float 12s ease-in-out infinite reverse; }
.hero-badge {
  display:inline-flex;align-items:center;gap:8px;
  background:rgba(124,58,237,.15);border:1px solid rgba(124,58,237,.4);
  border-radius:50px;padding:6px 18px;margin-bottom:28px;
  font-size:12px;font-weight:600;color:#C4B5FD;animation:fadeInUp .8s ease both;
}
.badge-dot { width:6px;height:6px;background:#22D3EE;border-radius:50%;animation:glow-pulse 1.5s infinite; }
.hero-title {
  font-family:'Space Grotesk',sans-serif;
  font-size:clamp(40px,7vw,88px);font-weight:800;line-height:1.05;
  letter-spacing:-2px;margin-bottom:24px;animation:fadeInUp .8s .1s ease both;
}
.hero-title .grad {
  background:linear-gradient(135deg,#8B5CF6 0%,#4F8CFF 40%,#22D3EE 80%);
  background-size:200% 200%;animation:gradient-shift 4s ease infinite;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.hero-sub { font-size:18px;color:#94A3B8;max-width:560px;margin:0 auto 40px;line-height:1.7;animation:fadeInUp .8s .2s ease both; }
.hero-btns { display:flex;gap:16px;justify-content:center;flex-wrap:wrap;animation:fadeInUp .8s .3s ease both; }
.btn-hp { background:linear-gradient(135deg,#7C3AED,#4F8CFF);color:#fff;padding:15px 38px;border-radius:12px;border:none;font-size:15px;font-weight:700;cursor:pointer;text-decoration:none;display:inline-block;transition:all .3s;box-shadow:0 0 30px rgba(124,58,237,.5); }
.btn-hp:hover { transform:translateY(-3px);box-shadow:0 0 50px rgba(124,58,237,.7); }
.btn-hg { background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.15);color:#fff;padding:15px 38px;border-radius:12px;font-size:15px;font-weight:600;cursor:pointer;text-decoration:none;display:inline-block;transition:all .3s;backdrop-filter:blur(10px); }
.btn-hg:hover { background:rgba(255,255,255,.1);transform:translateY(-3px); }

/* TRUSTED */
.trusted { padding:56px 48px;background:rgba(18,0,43,.8);border-top:1px solid rgba(124,58,237,.1);border-bottom:1px solid rgba(124,58,237,.1);text-align:center; }
.trusted-lbl { font-size:11px;font-weight:700;color:#475569;letter-spacing:3px;text-transform:uppercase;margin-bottom:32px; }
.trusted-logos { display:flex;gap:48px;justify-content:center;align-items:center;flex-wrap:wrap; }
.t-logo { font-family:'Space Grotesk',sans-serif;font-size:18px;font-weight:700;color:#334155;transition:color .3s;cursor:default; }
.t-logo:hover { color:#8B5CF6; }

/* FEATURES */
.features { padding:100px 48px;background:linear-gradient(180deg,#090014,#12002B); }
.sec-label { text-align:center;font-size:11px;font-weight:700;color:#8B5CF6;letter-spacing:3px;text-transform:uppercase;margin-bottom:14px; }
.sec-title { text-align:center;font-family:'Space Grotesk',sans-serif;font-size:clamp(28px,4vw,48px);font-weight:800;margin-bottom:14px; }
.sec-sub { text-align:center;color:#64748B;max-width:500px;margin:0 auto 56px;font-size:15px;line-height:1.7; }
.feat-grid { display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:22px;max-width:1100px;margin:0 auto; }
.feat-card { background:rgba(255,255,255,.03);border:1px solid rgba(124,58,237,.2);border-radius:20px;padding:30px;transition:all .3s;position:relative;overflow:hidden;backdrop-filter:blur(10px); }
.feat-card:hover { border-color:rgba(124,58,237,.6);transform:translateY(-6px);box-shadow:0 20px 60px rgba(124,58,237,.15); }
.feat-icon { width:50px;height:50px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:22px;margin-bottom:18px; }
.feat-title { font-size:16px;font-weight:700;margin-bottom:8px; }
.feat-desc { font-size:13px;color:#64748B;line-height:1.7; }

/* STATS */
.stats { padding:80px 48px;background:radial-gradient(ellipse 80% 60% at 50% 50%,rgba(124,58,237,.1),transparent 70%),linear-gradient(180deg,#12002B,#1A063A);text-align:center; }
.stats-grid { display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:28px;max-width:880px;margin:0 auto; }
.stat-card { padding:36px 20px;background:rgba(255,255,255,.03);border:1px solid rgba(124,58,237,.2);border-radius:20px;backdrop-filter:blur(10px);transition:transform .3s; }
.stat-card:hover { transform:translateY(-4px); }
.stat-num { font-family:'Space Grotesk',sans-serif;font-size:46px;font-weight:800;line-height:1;background:linear-gradient(135deg,#8B5CF6,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:6px; }
.stat-lbl { font-size:13px;color:#64748B;font-weight:500; }

/* TESTIMONIALS */
.testi { padding:100px 48px;background:linear-gradient(180deg,#1A063A,#090014); }
.testi-grid { display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:22px;max-width:1000px;margin:0 auto; }
.testi-card { background:rgba(255,255,255,.03);border:1px solid rgba(124,58,237,.15);border-radius:20px;padding:30px;backdrop-filter:blur(10px);transition:all .3s; }
.testi-card:hover { border-color:rgba(124,58,237,.4);transform:translateY(-4px); }
.testi-stars { color:#F59E0B;font-size:13px;margin-bottom:14px; }
.testi-text { color:#94A3B8;font-size:14px;line-height:1.8;margin-bottom:22px;font-style:italic; }
.testi-author { display:flex;align-items:center;gap:12px; }
.testi-av { width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px;flex-shrink:0; }
.testi-name { font-weight:600;font-size:14px; }
.testi-role { font-size:12px;color:#64748B; }

/* PRICING */
.pricing { padding:100px 48px;background:linear-gradient(180deg,#090014,#12002B); }
.pricing-grid { display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:22px;max-width:960px;margin:0 auto; }
.p-card { background:rgba(255,255,255,.03);border:1px solid rgba(124,58,237,.2);border-radius:24px;padding:38px 30px;text-align:center;transition:all .3s;position:relative;overflow:hidden; }
.p-card.featured { background:linear-gradient(145deg,rgba(124,58,237,.2),rgba(79,140,255,.1));border-color:#7C3AED;box-shadow:0 0 60px rgba(124,58,237,.25);transform:scale(1.04); }
.p-card:hover { transform:translateY(-8px);border-color:rgba(124,58,237,.5); }
.p-card.featured:hover { transform:scale(1.04) translateY(-8px); }
.p-badge { position:absolute;top:18px;right:18px;background:linear-gradient(135deg,#7C3AED,#4F8CFF);color:#fff;font-size:10px;font-weight:700;padding:4px 10px;border-radius:50px;letter-spacing:1px; }
.p-tier { font-size:12px;font-weight:700;color:#8B5CF6;letter-spacing:2px;text-transform:uppercase;margin-bottom:10px; }
.p-price { font-family:'Space Grotesk',sans-serif;font-size:50px;font-weight:800;margin-bottom:4px; }
.p-price span { font-size:18px;font-weight:500;color:#64748B; }
.p-desc { font-size:13px;color:#64748B;margin-bottom:28px; }
.p-features { list-style:none;text-align:left;margin-bottom:28px;display:flex;flex-direction:column;gap:10px; }
.p-features li { font-size:13px;color:#94A3B8;display:flex;align-items:center;gap:8px; }
.p-features li::before { content:'✓';color:#22D3EE;font-weight:700;flex-shrink:0; }
.btn-pg { background:transparent;border:1px solid rgba(139,92,246,.5);color:#8B5CF6;padding:11px 20px;border-radius:10px;font-size:13px;font-weight:600;cursor:pointer;width:100%;transition:all .2s;font-family:'Inter',sans-serif; }
.btn-pg:hover { background:rgba(139,92,246,.1); }
.btn-pp { background:linear-gradient(135deg,#7C3AED,#4F8CFF);border:none;color:#fff;padding:11px 20px;border-radius:10px;font-size:13px;font-weight:700;cursor:pointer;width:100%;font-family:'Inter',sans-serif;transition:all .3s; }
.btn-pp:hover { filter:brightness(1.1); }

/* FAQ */
.faq { padding:100px 48px;background:linear-gradient(180deg,#12002B,#1A063A); }
.faq-list { max-width:700px;margin:0 auto;display:flex;flex-direction:column;gap:10px; }
.faq-item { background:rgba(255,255,255,.03);border:1px solid rgba(124,58,237,.2);border-radius:14px;overflow:hidden;transition:border-color .3s; }
.faq-item:hover { border-color:rgba(124,58,237,.5); }
.faq-q { width:100%;background:transparent;border:none;color:#fff;font-size:14px;font-weight:600;padding:18px 22px;cursor:pointer;text-align:left;display:flex;justify-content:space-between;align-items:center;font-family:'Inter',sans-serif; }
.faq-a { padding:0 22px 18px;color:#64748B;font-size:13px;line-height:1.8;display:none; }
.faq-item.open .faq-a { display:block; }
.faq-chevron { transition:transform .3s;font-size:11px;color:#8B5CF6; }
.faq-item.open .faq-chevron { transform:rotate(180deg); }

/* CTA */
.cta-sec { padding:100px 48px;text-align:center;background:radial-gradient(ellipse 80% 60% at 50% 50%,rgba(124,58,237,.18),transparent 70%),linear-gradient(180deg,#1A063A,#090014); }
.cta-title { font-family:'Space Grotesk',sans-serif;font-size:clamp(30px,5vw,60px);font-weight:800;margin-bottom:18px; }
.cta-sub { color:#64748B;font-size:16px;max-width:480px;margin:0 auto 36px;line-height:1.7; }
.btn-cta { background:linear-gradient(135deg,#7C3AED,#4F8CFF,#22D3EE);background-size:200% 200%;animation:gradient-shift 3s ease infinite;color:#fff;padding:18px 48px;border-radius:14px;border:none;font-size:16px;font-weight:700;cursor:pointer;text-decoration:none;display:inline-block;letter-spacing:.3px;transition:transform .3s; }
.btn-cta:hover { transform:translateY(-4px) scale(1.03); }

/* FOOTER */
.lp-footer { padding:56px 48px 28px;background:#050010;border-top:1px solid rgba(124,58,237,.12); }
.footer-top { display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:44px;margin-bottom:44px; }
.footer-brand p { color:#475569;font-size:13px;line-height:1.7;margin-top:10px;max-width:240px; }
.footer-col h4 { font-size:12px;font-weight:700;color:#8B5CF6;text-transform:uppercase;letter-spacing:2px;margin-bottom:14px; }
.footer-col a { display:block;color:#475569;font-size:13px;text-decoration:none;margin-bottom:7px;transition:color .2s; }
.footer-col a:hover { color:#8B5CF6; }
.f-socials { display:flex;gap:10px;margin-top:14px; }
.f-social { width:34px;height:34px;border-radius:8px;background:rgba(124,58,237,.12);border:1px solid rgba(124,58,237,.25);display:flex;align-items:center;justify-content:center;font-size:14px;text-decoration:none;transition:all .2s; }
.f-social:hover { background:rgba(124,58,237,.28);transform:translateY(-2px); }
.footer-bottom { border-top:1px solid rgba(124,58,237,.08);padding-top:22px;display:flex;justify-content:space-between;align-items:center;color:#334155;font-size:12px;flex-wrap:wrap;gap:10px; }
</style>

<!-- HERO -->
<section class="hero">
  <div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>
  <div style="position:relative;z-index:2;">
    <div class="hero-badge"><div class="badge-dot"></div>Powered by Machine Learning &amp; AI</div>
    <h1 class="hero-title">Predict Employee<br><span class="grad">Performance with AI</span></h1>
    <p class="hero-sub">Give your HR team a superpower. Predict ratings, identify at-risk employees, and make data-driven workforce decisions.</p>
    <div class="hero-btns">
      <a href="?page=signup" class="btn-hp">🚀 Get Started Free</a>
      <a href="#features" class="btn-hg">✦ See How It Works</a>
    </div>
  </div>
</section>

<!-- TRUSTED BY -->
<section class="trusted">
  <p class="trusted-lbl">Trusted by teams at</p>
  <div class="trusted-logos">
    <span class="t-logo">Microsoft</span><span class="t-logo">Google</span>
    <span class="t-logo">Amazon</span><span class="t-logo">Nvidia</span>
    <span class="t-logo">OpenAI</span><span class="t-logo">Tesla</span>
  </div>
</section>

<!-- FEATURES -->
<section class="features" id="features">
  <p class="sec-label">Why PerformaAI</p>
  <h2 class="sec-title">Everything your HR team needs</h2>
  <p class="sec-sub">From real-time predictions to deep analytics — built for modern HR professionals.</p>
  <div class="feat-grid">
    <div class="feat-card"><div class="feat-icon" style="background:rgba(124,58,237,.15);">🤖</div><div class="feat-title">AI Prediction Engine</div><div class="feat-desc">Random Forest model trained on real HR data predicts performance with high accuracy across 4 rating tiers.</div></div>
    <div class="feat-card"><div class="feat-icon" style="background:rgba(79,140,255,.15);">📊</div><div class="feat-title">Live Analytics Dashboard</div><div class="feat-desc">Interactive charts — feature importance, heatmaps, department comparisons — all in one place.</div></div>
    <div class="feat-card"><div class="feat-icon" style="background:rgba(34,211,238,.15);">💾</div><div class="feat-title">Prediction History</div><div class="feat-desc">Every prediction saved to a database. Review, compare, and export past results any time.</div></div>
    <div class="feat-card"><div class="feat-icon" style="background:rgba(236,72,153,.15);">🔐</div><div class="feat-title">Role-Based Security</div><div class="feat-desc">HR-only access with secure login, hashed passwords, and session management baked in.</div></div>
    <div class="feat-card"><div class="feat-icon" style="background:rgba(245,158,11,.15);">📂</div><div class="feat-title">Bulk CSV Predictions</div><div class="feat-desc">Upload your entire department as a CSV and get predictions for all employees instantly.</div></div>
    <div class="feat-card"><div class="feat-icon" style="background:rgba(124,58,237,.15);">☁️</div><div class="feat-title">Cloud-Ready Deploy</div><div class="feat-desc">One-click deploy to Streamlit Cloud. No servers, no DevOps. Your app is live in minutes.</div></div>
  </div>
</section>

<!-- STATS -->
<section class="stats">
  <p class="sec-label">By the numbers</p>
  <h2 class="sec-title" style="margin-bottom:44px;">Trusted. Tested. Proven.</h2>
  <div class="stats-grid">
    <div class="stat-card"><div class="stat-num">10K+</div><div class="stat-lbl">Users Worldwide</div></div>
    <div class="stat-card"><div class="stat-num">500+</div><div class="stat-lbl">Businesses</div></div>
    <div class="stat-card"><div class="stat-num">99.9%</div><div class="stat-lbl">Uptime</div></div>
    <div class="stat-card"><div class="stat-num">24/7</div><div class="stat-lbl">Support</div></div>
  </div>
</section>

<!-- TESTIMONIALS -->
<section class="testi" id="testimonials">
  <p class="sec-label">Testimonials</p>
  <h2 class="sec-title">What HR leaders say</h2>
  <p class="sec-sub">Real feedback from real teams using PerformaAI.</p>
  <div class="testi-grid">
    <div class="testi-card"><div class="testi-stars">★★★★★</div><p class="testi-text">"PerformaAI transformed how we approach performance reviews. We spotted three at-risk employees before their annual review — and retained all of them."</p><div class="testi-author"><div class="testi-av" style="background:linear-gradient(135deg,#7C3AED,#4F8CFF);">S</div><div><div class="testi-name">Sarah Mitchell</div><div class="testi-role">Head of HR · TechVenture Co.</div></div></div></div>
    <div class="testi-card"><div class="testi-stars">★★★★★</div><p class="testi-text">"The analytics dashboard alone is worth it. Our leadership team finally has a visual story behind every performance decision."</p><div class="testi-author"><div class="testi-av" style="background:linear-gradient(135deg,#22D3EE,#4F8CFF);">R</div><div><div class="testi-name">Raj Patel</div><div class="testi-role">VP People Ops · ScaleUp Ltd.</div></div></div></div>
    <div class="testi-card"><div class="testi-stars">★★★★★</div><p class="testi-text">"Deployed in one afternoon. No database headache. The prediction accuracy surprised us — it matched our manual reviews closely."</p><div class="testi-author"><div class="testi-av" style="background:linear-gradient(135deg,#EC4899,#F59E0B);">A</div><div><div class="testi-name">Anika Joshi</div><div class="testi-role">HR Director · GlobalEdge Inc.</div></div></div></div>
  </div>
</section>

<!-- PRICING -->
<section class="pricing" id="pricing">
  <p class="sec-label">Pricing</p>
  <h2 class="sec-title">Simple, transparent plans</h2>
  <p class="sec-sub">Start free, scale as you grow. No hidden fees.</p>
  <div class="pricing-grid">
    <div class="p-card"><div class="p-tier">Starter</div><div class="p-price">Free<span>/mo</span></div><p class="p-desc">Perfect for small teams.</p><ul class="p-features"><li>50 predictions/month</li><li>Basic analytics</li><li>2 HR accounts</li><li>Community support</li></ul><button class="btn-pg" onclick="location.href='?page=signup'">Get Started</button></div>
    <div class="p-card featured"><div class="p-badge">POPULAR</div><div class="p-tier">Pro</div><div class="p-price">₹2,499<span>/mo</span></div><p class="p-desc">For growing HR teams.</p><ul class="p-features"><li>Unlimited predictions</li><li>Full analytics + heatmaps</li><li>10 HR accounts</li><li>Bulk CSV predictions</li><li>PDF exports</li><li>Priority support</li></ul><button class="btn-pp" onclick="location.href='?page=signup'">Start Pro Trial</button></div>
    <div class="p-card"><div class="p-tier">Enterprise</div><div class="p-price">Custom</div><p class="p-desc">For large organizations.</p><ul class="p-features"><li>Everything in Pro</li><li>Custom ML training</li><li>Unlimited accounts</li><li>SSO integration</li><li>Dedicated manager</li></ul><button class="btn-pg" onclick="location.href='?page=signup'">Contact Sales</button></div>
  </div>
</section>

<!-- FAQ -->
<section class="faq" id="faq">
  <p class="sec-label">FAQ</p>
  <h2 class="sec-title">Common questions</h2>
  <p class="sec-sub">Everything you need to know.</p>
  <div class="faq-list">
    <div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('open')">Do I need a database? <span class="faq-chevron">▼</span></button><div class="faq-a">PerformaAI uses a lightweight SQLite database — no server setup needed. It's just a single file in your project folder.</div></div>
    <div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('open')">How accurate is the prediction? <span class="faq-chevron">▼</span></button><div class="faq-a">Our Random Forest model achieves 55–70% accuracy on 4-class prediction, which is 2–3x better than random guessing. Results improve with real-world datasets.</div></div>
    <div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('open')">Can I use my own HR data? <span class="faq-chevron">▼</span></button><div class="faq-a">Yes. Replace the included CSV with your own dataset and re-run train_model.py. The model retrains automatically.</div></div>
    <div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('open')">How do I add new HR users? <span class="faq-chevron">▼</span></button><div class="faq-a">New accounts are created via the Sign Up page. All passwords are securely hashed and stored in SQLite.</div></div>
  </div>
</section>

<!-- CTA -->
<section class="cta-sec">
  <h2 class="cta-title">Ready to predict<br><span style="background:linear-gradient(135deg,#8B5CF6,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">performance?</span></h2>
  <p class="cta-sub">Join HR teams who use data, not guesswork, to manage their workforce.</p>
  <a href="?page=signup" class="btn-cta">🚀 Start Your Free Trial</a>
</section>

<!-- FOOTER -->
<footer class="lp-footer">
  <div class="footer-top">
    <div class="footer-brand">
      <div style="font-family:'Space Grotesk',sans-serif;font-size:20px;font-weight:700;background:linear-gradient(135deg,#8B5CF6,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">PerformaAI</div>
      <p>AI-powered HR analytics for modern teams. Predict performance, reduce attrition, make smarter decisions.</p>
      <div class="f-socials">
        <a class="f-social" href="#">🐦</a><a class="f-social" href="#">💼</a>
        <a class="f-social" href="#">🐙</a><a class="f-social" href="#">📘</a>
      </div>
    </div>
    <div class="footer-col"><h4>Product</h4><a href="#">Features</a><a href="#">Pricing</a><a href="#">Changelog</a></div>
    <div class="footer-col"><h4>Company</h4><a href="#">About</a><a href="#">Blog</a><a href="#">Contact</a></div>
    <div class="footer-col"><h4>Legal</h4><a href="#">Privacy</a><a href="#">Terms</a><a href="#">Security</a></div>
  </div>
  <div class="footer-bottom">
    <span>© 2025 PerformaAI. All rights reserved.</span>
    <span>Made with 💜 for Final Year Projects</span>
  </div>
</footer>
"""

AUTH_CARD_CSS = """
<style>
.auth-wrap { display:flex;justify-content:center;margin-top:60px;padding:0 20px 40px; }
.auth-card { background:rgba(255,255,255,.04);border:1px solid rgba(124,58,237,.3);border-radius:24px;padding:44px 40px;width:100%;max-width:420px;backdrop-filter:blur(30px);box-shadow:0 0 80px rgba(124,58,237,.12),0 40px 80px rgba(0,0,0,.5);animation:fadeInUp .6s ease both; }
</style>
"""


def show():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    render_public_navbar()
    st.markdown(LANDING_HTML, unsafe_allow_html=True)

"""
app.py - Main Entry Point
==========================

Run:
  streamlit run app.py
"""

import streamlit as st

# ── Page config (entry point) ──────────────────────────────
st.set_page_config(
    page_title="Numerical Methods Lab",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Helper to safely render HTML (ensures unsafe_allow_html=True)
def safe_html(html: str):
    st.markdown(html, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — CLEAN PREMIUM THEME (unified with all labs)
# ══════════════════════════════════════════════════════════════════════════════
safe_html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@600;700;800;900&display=swap');

/* ─── PALETTE ────────────────────────────────────────────── */
:root {
    --cyan:       #22d3ee;
    --cyan-dim:   rgba(34,211,238,0.12);
    --violet:     #a78bfa;
    --violet-dim: rgba(167,139,250,0.12);
    --emerald:    #34d399;
    --emerald-dim:rgba(52,211,153,0.12);
    --amber:      #fbbf24;
    --amber-dim:  rgba(251,191,36,0.12);
    --rose:       #fb7185;
    --rose-dim:   rgba(251,113,133,0.12);
    --sky:        #38bdf8;
    --sky-dim:    rgba(56,189,248,0.12);

    --bg-0:       #07090f;
    --bg-1:       #0c1021;
    --bg-2:       #111730;
    --bg-card:    rgba(14,20,40,0.65);
    --bg-glass:   rgba(18,26,52,0.50);

    --text-0:     #ffffff;
    --text-1:     #e8ecf4;
    --text-2:     #8b95b0;
    --text-3:     #4b5574;

    --border-1:   rgba(34,211,238,0.10);
    --border-2:   rgba(167,139,250,0.10);
    --radius:     16px;
    --radius-sm:  10px;
}

/* ─── ANIMATIONS ─────────────────────────────────────────── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeScale {
    from { opacity: 0; transform: scale(0.95); }
    to   { opacity: 1; transform: scale(1); }
}
@keyframes slideRight {
    from { opacity: 0; transform: translateX(-16px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes gradientShift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}
@keyframes softPulse {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 1; }
}
@keyframes dotPulse {
    0%, 100% { box-shadow: 0 0 0 0 currentColor; }
    50% { box-shadow: 0 0 0 5px transparent; }
}
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-6px); }
}
@keyframes borderGlow {
    0%, 100% { border-color: rgba(34,211,238,0.12); }
    50% { border-color: rgba(167,139,250,0.2); }
}

/* ─── RESETS ─────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif !important;
}
.stApp, [data-testid="stAppViewContainer"] {
    background: var(--bg-0) !important;
    color: var(--text-1) !important;
}

/* ─── SIDEBAR ────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0f1e 0%, #070b16 100%) !important;
    border-right: 1px solid rgba(34,211,238,0.06) !important;
}
[data-testid="stSidebar"] * {
    font-family: 'Inter', sans-serif !important;
}

/* Sidebar radio buttons — complete redesign */
[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 2px !important;
}
[data-testid="stSidebar"] [role="radiogroup"] label {
    display: flex !important;
    align-items: center !important;
    padding: 11px 14px !important;
    margin: 2px 0 !important;
    border-radius: 12px !important;
    border: 1px solid transparent !important;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
    cursor: pointer !important;
    font-size: 0.84rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.01em !important;
    color: var(--text-2) !important;
    background: transparent !important;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(34,211,238,0.04) !important;
    border-color: rgba(34,211,238,0.1) !important;
    color: var(--text-1) !important;
    transform: translateX(3px) !important;
}
[data-testid="stSidebar"] [role="radiogroup"] [aria-checked="true"] + label,
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(135deg, rgba(34,211,238,0.08), rgba(167,139,250,0.08)) !important;
    border-color: rgba(34,211,238,0.2) !important;
    color: var(--cyan) !important;
    font-weight: 600 !important;
    box-shadow: 0 0 20px rgba(34,211,238,0.05) !important;
}

/* ─── MAIN CONTENT ───────────────────────────────────────── */
[data-testid="stMain"] {
    background: transparent !important;
}
.block-container {
    padding-top: 2rem !important;
    max-width: 1100px !important;
}

/* ─── HEADINGS ───────────────────────────────────────────── */
h1, h2, h3 {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
    color: var(--text-0) !important;
}

/* ─── BUTTONS ────────────────────────────────────────────── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #0ea5e9, #6366f1, #a855f7) !important;
    background-size: 200% 200% !important;
    animation: gradientShift 5s ease infinite !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    padding: 0.55rem 1.2rem !important;
    box-shadow: 0 4px 18px rgba(99,102,241,0.25) !important;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(99,102,241,0.4) !important;
    filter: brightness(1.08) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) scale(0.98) !important;
}

/* ─── WIDGETS ────────────────────────────────────────────── */
[data-testid="stSelectbox"] > div,
[data-testid="stNumberInput"] > div,
[data-testid="stTextInput"] > div {
    background: var(--bg-1) !important;
    border-color: var(--border-1) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-1) !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background: var(--cyan) !important;
    box-shadow: 0 0 12px rgba(34,211,238,0.3) !important;
}

/* ─── METRIC CARDS ───────────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--bg-glass) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid var(--border-1) !important;
    border-radius: 14px !important;
    padding: 1rem !important;
}
[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    color: var(--cyan) !important;
}

/* ─── DATAFRAME ──────────────────────────────────────────── */
[data-testid="stDataFrame"], .stDataFrame {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-1) !important;
    border-radius: 14px !important;
    overflow: hidden !important;
}

/* ─── EXPANDER ───────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: rgba(12,16,33,0.6) !important;
    border: 1px solid rgba(34,211,238,0.07) !important;
    border-radius: 14px !important;
}

/* ─── ALERTS ─────────────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border-left-width: 3px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
}

/* ─── CODE ───────────────────────────────────────────────── */
code, pre {
    font-family: 'JetBrains Mono', monospace !important;
    background: var(--bg-2) !important;
    color: var(--amber) !important;
    border-radius: 8px !important;
}

/* ─── DIVIDER ────────────────────────────────────────────── */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(34,211,238,0.12), rgba(167,139,250,0.12), transparent) !important;
    margin: 1.5rem 0 !important;
}

/* ─── PLOTLY CHART BG ────────────────────────────────────── */
.js-plotly-plot .plotly {
    background: transparent !important;
}

/* ─── SCROLLBAR ──────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-0); }
::-webkit-scrollbar-thumb {
    background: rgba(34,211,238,0.15);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(34,211,238,0.3); }

/* ─── TABS (global) ──────────────────────────────────────── */
div[data-testid="stTabs"] > div:first-child {
    border-bottom: 1px solid rgba(255,255,255,0.05) !important;
}
button[data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    border-radius: 12px 12px 0 0 !important;
    padding: 0.72rem 1.3rem !important;
    color: var(--text-3) !important;
    transition: all 0.3s ease !important;
}
button[data-baseweb="tab"]:hover {
    color: var(--text-1) !important;
    background: rgba(34,211,238,0.04) !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--cyan) !important;
    background: rgba(34,211,238,0.08) !important;
    border-bottom: 2.5px solid var(--cyan) !important;
}
</style>
""")

# ── Particle Background ──────────────────────────────────────────────────────
st.components.v1.html("""
<canvas id="mainParticles" style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:0;"></canvas>
<script>
(function(){
    var c=document.getElementById('mainParticles');if(!c)return;
    var ctx=c.getContext('2d'),w,h,pts=[];
    function rs(){w=c.width=window.innerWidth;h=c.height=window.innerHeight;}
    rs();window.addEventListener('resize',rs);
    var cols=['#22d3ee','#a78bfa','#34d399','#fbbf24'];
    for(var i=0;i<50;i++){
        pts.push({x:Math.random()*w,y:Math.random()*h,
            vx:(Math.random()-0.5)*0.2,vy:(Math.random()-0.5)*0.2,
            r:Math.random()*1.2+0.3,c:cols[Math.floor(Math.random()*4)]});
    }
    function draw(){
        ctx.clearRect(0,0,w,h);
        for(var i=0;i<pts.length;i++){
            var p=pts[i]; p.x+=p.vx; p.y+=p.vy;
            if(p.x<0)p.x=w;if(p.x>w)p.x=0;if(p.y<0)p.y=h;if(p.y>h)p.y=0;
            ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,6.28);
            ctx.fillStyle=p.c;ctx.globalAlpha=0.3;ctx.fill();
            for(var j=i+1;j<pts.length;j++){
                var dx=pts[j].x-p.x,dy=pts[j].y-p.y,d=Math.sqrt(dx*dx+dy*dy);
                if(d<110){ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(pts[j].x,pts[j].y);
                    ctx.strokeStyle=p.c;ctx.globalAlpha=0.035*(1-d/110);ctx.lineWidth=0.5;ctx.stroke();}
            }
        }
        ctx.globalAlpha=1;requestAnimationFrame(draw);
    }
    draw();
})();
</script>
""", height=0, scrolling=False)

# ── Import all lab modules ────────────────────────────────────────────────────
from labs.lab1_root_finding  import render_lab1
from labs.lab2_interpolation import render_lab2
from labs.lab3_integration   import render_lab3
from labs.lab4_differential  import render_lab4

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:

    # Brand header
    safe_html("""
<div style="text-align:center; padding:1.2rem 0 0.6rem;">
        <div style="
            width:48px; height:48px; margin:0 auto 0.6rem;
            border-radius:14px;
            background: linear-gradient(135deg, rgba(34,211,238,0.15), rgba(167,139,250,0.15));
            border: 1px solid rgba(34,211,238,0.2);
            display:flex; align-items:center; justify-content:center;
            font-family:'JetBrains Mono',monospace;
            font-weight:800; font-size:1.1rem; color:#22d3ee;
            box-shadow: 0 0 20px rgba(34,211,238,0.08);
        ">NM</div>
        <div style="
            font-family:'Outfit',sans-serif; font-weight:800;
            font-size:1rem; color:#e8ecf4; letter-spacing:0.04em;
            line-height:1.3;
        ">NUMERICAL<br>METHODS</div>
        <div style="
            font-family:'JetBrains Mono',monospace;
            font-size:0.58rem; color:#4b5574;
            margin-top:0.35rem; letter-spacing:0.14em;
        ">SCIENTIFIC COMPUTING</div>
    </div>
    """)

    safe_html("""<hr style="border:none;height:1px;
        background:linear-gradient(90deg,transparent,rgba(34,211,238,0.1),transparent);
        margin:0.6rem 0;">""")

    lab_options = {
        "Home"                       : "home",
        "Lab 1 · Root Finding"       : "lab1",
        "Lab 2 · Interpolation"      : "lab2",
        "Lab 3 · Integration"        : "lab3",
        "Lab 4 · Diff. Equations"    : "lab4",
    }

    selected_label = st.radio(
        "Navigation",
        list(lab_options.keys()),
        label_visibility="collapsed"
    )
    selected_lab = lab_options[selected_label]

    safe_html("""<hr style="border:none;height:1px;
        background:linear-gradient(90deg,transparent,rgba(34,211,238,0.1),transparent);
        margin:0.6rem 0;">""")

    safe_html("""
<div style="
        font-family:'JetBrains Mono',monospace;
        font-size:0.58rem; color:#2d3654;
        text-align:center; line-height:2;
        padding:0.3rem 0;
    ">
        v1.0.0 · Streamlit<br>
        Bisection · Newton · Euler
    </div>
    """)

# ── Main Content ──────────────────────────────────────────────────────────────
if selected_lab == "home":

    # ── Hero Section ──────────────────────────────────────────────────────────
    st.components.v1.html("""
<html><head>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=JetBrains+Mono:wght@600&family=Outfit:wght@900&display=swap" rel="stylesheet">
<style>
@keyframes fadeScale{from{opacity:0;transform:scale(0.97)}to{opacity:1;transform:scale(1)}}
@keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
body{margin:0;padding:0;background:transparent;}
.hero{position:relative;border-radius:24px;padding:2.8rem 3rem 2.4rem;overflow:hidden;animation:fadeScale 0.7s ease-out;background:radial-gradient(ellipse 60% 50% at 15% 20%, rgba(34,211,238,0.06) 0%, transparent 60%),radial-gradient(ellipse 50% 60% at 85% 80%, rgba(167,139,250,0.05) 0%, transparent 60%),linear-gradient(180deg, rgba(14,20,40,0.95) 0%, rgba(7,9,15,0.98) 100%);border:1px solid rgba(34,211,238,0.08);}
.topbar{position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent 5%,#22d3ee 25%,#a78bfa 50%,#34d399 75%,transparent 95%);opacity:0.45;}
.label{font-family:'JetBrains Mono',monospace;font-size:0.62rem;letter-spacing:0.3em;text-transform:uppercase;color:#22d3ee;display:flex;align-items:center;gap:0.6rem;margin-bottom:0.8rem;animation:fadeUp 0.5s ease-out 0.1s both;}
.bar{width:24px;height:2px;background:#22d3ee;border-radius:2px;display:inline-block;}
.heading{font-family:'Outfit',sans-serif;font-weight:900;font-size:2.6rem;color:#fff;line-height:1.1;margin:0 0 0.7rem;letter-spacing:-0.02em;animation:fadeUp 0.5s ease-out 0.2s both;}
.gradient-text{background:linear-gradient(135deg,#22d3ee 0%,#a78bfa 50%,#34d399 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.desc{font-family:'Inter',sans-serif;color:#8b95b0;font-size:0.93rem;max-width:600px;margin:0;line-height:1.7;animation:fadeUp 0.5s ease-out 0.3s both;}
</style></head><body>
<div class="hero">
  <div class="topbar"></div>
  <div class="label"><span class="bar"></span>Welcome to the Lab</div>
  <div class="heading">Numerical Methods<br><span class="gradient-text">Web Application</span></div>
  <p class="desc">Four computational labs with interactive algorithms, live Plotly graphs, and step-by-step solutions. Select any lab from the sidebar to begin.</p>
</div>
</body></html>
    """, height=240, scrolling=False)

    # ── Lab Cards ─────────────────────────────────────────────────────────────
        # ── Lab Cards (FIXED: no onMouseOver/onMouseOut) ─────────────────────────
    labs_data = [
        {
            "num": "01",
            "title": "Root Finding",
            "methods": ["Bisection", "Newton-Raphson", "Secant"],
            "color": "#22d3ee",
            "color_dim": "rgba(34,211,238,0.08)",
            "border_dim": "rgba(34,211,238,0.15)",
            "desc": "Solve f(x) = 0 with three classical methods",
        },
        {
            "num": "02",
            "title": "Interpolation",
            "methods": ["Lagrange", "Newton Forward", "Newton Divided"],
            "color": "#a78bfa",
            "color_dim": "rgba(167,139,250,0.08)",
            "border_dim": "rgba(167,139,250,0.15)",
            "desc": "Estimate values between known data points",
        },
        {
            "num": "03",
            "title": "Numerical Integration",
            "methods": ["Trapezoidal", "Simpson's 1/3", "Midpoint"],
            "color": "#fbbf24",
            "color_dim": "rgba(251,191,36,0.07)",
            "border_dim": "rgba(251,191,36,0.15)",
            "desc": "Approximate definite integrals numerically",
        },
        {
            "num": "04",
            "title": "Differential Equations",
            "methods": ["Euler", "Modified Euler", "Heun's"],
            "color": "#34d399",
            "color_dim": "rgba(52,211,153,0.07)",
            "border_dim": "rgba(52,211,153,0.15)",
            "desc": "Solve initial value ODE problems",
        }
    ]

    # Inject CSS for hover effects (one time)
    st.markdown("""
    <style>
    .lab-card {
        transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
        cursor: default;
    }
    .lab-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 36px rgba(0,0,0,0.25);
        border-color: rgba(34,211,238,0.35) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    cols = st.columns(2, gap="large")
    for i, lab in enumerate(labs_data):
        with cols[i % 2]:
            # Build method pills (unchanged)
            pills = "".join(
                f'<span style="'
                f'display:inline-block;'
                f'font-family:JetBrains Mono,monospace;'
                f'font-size:0.62rem; font-weight:600;'
                f'color:{lab["color"]};'
                f'background:rgba(255,255,255,0.03);'
                f'border:1px solid {lab["border_dim"]};'
                f'border-radius:100px;'
                f'padding:0.2rem 0.6rem;'
                f'margin:3px 4px 3px 0;'
                f'transition:transform 0.2s ease;'
                f'">{m}</span>'
                for m in lab["methods"]
            )

            delay = 0.1 + i * 0.1
            color      = lab['color']
            color_dim  = lab['color_dim']
            border_dim = lab['border_dim']
            num        = lab['num']
            title      = lab['title']
            desc       = lab['desc']
            card_html = (
                '<div class="lab-card" style="'
                'background:' + color_dim + ';'
                'border:1px solid ' + border_dim + ';'
                'border-radius:18px;'
                'padding:1.5rem 1.6rem 1.3rem;'
                'margin-bottom:1rem;'
                'position:relative;'
                'overflow:hidden;'
                'animation:fadeUp 0.5s ease-out ' + str(delay) + 's both;">'
                '<div style="'
                'position:absolute;top:0;left:1.2rem;right:1.2rem;'
                'height:2px;border-radius:0 0 2px 2px;'
                'background:' + color + ';opacity:0.35;"></div>'
                '<div style="display:flex;align-items:center;gap:0.9rem;margin-bottom:0.7rem;">'
                '<div style="'
                'width:40px;height:40px;border-radius:12px;'
                'background:' + color_dim + ';border:1px solid ' + border_dim + ';'
                'display:flex;align-items:center;justify-content:center;'
                'font-family:JetBrains Mono,monospace;'
                'font-weight:800;font-size:0.75rem;color:' + color + ';flex-shrink:0;">' + num + '</div>'
                '<div>'
                '<div style="font-family:JetBrains Mono,monospace;font-size:0.55rem;'
                'font-weight:700;letter-spacing:0.2em;color:' + color + ';opacity:0.7;">LAB ' + num + '</div>'
                '<div style="font-family:Outfit,sans-serif;font-weight:700;'
                'font-size:1.05rem;color:#e8ecf4;line-height:1.2;">' + title + '</div>'
                '</div></div>'
                '<div style="font-family:Inter,sans-serif;font-size:0.78rem;'
                'color:#6b7a98;margin-bottom:0.7rem;line-height:1.5;">' + desc + '</div>'
                '<div style="display:flex;flex-wrap:wrap;gap:0;">' + pills + '</div>'
                '</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)
    # ── Footer ────────────────────────────────────────────────────────────────
    safe_html("""
<div style="
        text-align:center;
        font-family:'JetBrains Mono',monospace;
        font-size:0.62rem; color:#2d3654;
        margin-top:1.5rem; letter-spacing:0.1em;
        padding-bottom:1rem;
    ">
        <span style="
            display:inline-block;
            width:30px; height:1px;
            background:linear-gradient(90deg, transparent, rgba(34,211,238,0.2), transparent);
            vertical-align:middle; margin:0 0.6rem;
        "></span>
        NUMERICAL COMPUTING
        <span style="
            display:inline-block;
            width:30px; height:1px;
            background:linear-gradient(90deg, transparent, rgba(167,139,250,0.2), transparent);
            vertical-align:middle; margin:0 0.6rem;
        "></span>
    </div>
    """)

elif selected_lab == "lab1":
    render_lab1()

elif selected_lab == "lab2":
    render_lab2()

elif selected_lab == "lab3":
    render_lab3()

elif selected_lab == "lab4":
    render_lab4()
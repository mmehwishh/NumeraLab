"""
lab3_integration.py - Lab 3: Numerical Integration
====================================================
Implements:
  1. Trapezoidal Rule   -> trapezoidal_rule()
  2. Simpson's Rule     -> simpsons_rule()
  3. Midpoint Rule      -> midpoint_rule()
  4. render_lab3()      -> Streamlit UI with area visualizations

UI v4.0 — CLEAN PREMIUM REDESIGN (matching Lab 1)
──────────────────────────────────────────────────
• No emojis — clean SVG/CSS indicators only
• Algorithm cards: clean, readable, no visual noise
• Plotly interactive graphs (zoom, hover, pan)
• Smooth CSS animations (tasteful, not overdone)
• ALL LOGIC 100% UNTOUCHED
"""

import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.helpers import parse_function, show_function_guide


# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — CLEAN PREMIUM THEME (matching Lab 1)
# ══════════════════════════════════════════════════════════════════════════════
LAB3_CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@600;700;800;900&display=swap');

:root {
    --cyan:     #22d3ee;
    --cyan-dim: rgba(34,211,238,0.12);
    --violet:   #a78bfa;
    --violet-dim: rgba(167,139,250,0.12);
    --emerald:  #34d399;
    --emerald-dim: rgba(52,211,153,0.12);
    --amber:    #fbbf24;
    --amber-dim: rgba(251,191,36,0.12);
    --rose:     #fb7185;
    --rose-dim: rgba(251,113,133,0.12);
    --sky:      #38bdf8;
    --sky-dim:  rgba(56,189,248,0.12);

    --bg-0:     #07090f;
    --bg-1:     #0c1021;
    --bg-2:     #111730;
    --bg-card:  rgba(14,20,40,0.65);
    --bg-glass: rgba(18,26,52,0.50);

    --text-0:   #ffffff;
    --text-1:   #e8ecf4;
    --text-2:   #8b95b0;
    --text-3:   #4b5574;

    --border-1: rgba(34,211,238,0.10);
    --border-2: rgba(167,139,250,0.10);
    --radius:   16px;
    --radius-sm: 10px;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(18px); }
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
    0%, 100% { opacity: 0.6; }
    50% { opacity: 1; }
}
@keyframes dotPulse {
    0%, 100% { box-shadow: 0 0 0 0 currentColor; }
    50% { box-shadow: 0 0 0 5px transparent; }
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif !important;
}
.stApp {
    background: var(--bg-0) !important;
}

/* ─── HERO ───────────────────────────────────────────────── */
.hero-section {
    position: relative;
    padding: 2.6rem 2.8rem 2.2rem;
    margin-bottom: 2rem;
    border-radius: 24px;
    overflow: hidden;
    animation: fadeScale 0.7s ease-out;
    background:
        radial-gradient(ellipse 60% 50% at 10% 20%, rgba(167,139,250,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 50% 60% at 90% 80%, rgba(52,211,153,0.05) 0%, transparent 60%),
        linear-gradient(180deg, rgba(14,20,40,0.8) 0%, rgba(7,9,15,0.9) 100%);
    border: 1px solid rgba(167,139,250,0.08);
}
.hero-section::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent 5%, var(--amber) 30%, var(--violet) 70%, transparent 95%);
    opacity: 0.5;
}
.hero-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--amber);
    display: flex; align-items: center; gap: 0.6rem;
    margin-bottom: 0.75rem;
    animation: fadeUp 0.5s ease-out 0.1s both;
}
.hero-label-bar {
    width: 24px; height: 2px;
    background: var(--amber);
    border-radius: 2px;
    display: inline-block;
}
.hero-heading {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    font-size: 2.4rem;
    line-height: 1.12;
    margin: 0 0 0.65rem;
    color: var(--text-0);
    letter-spacing: -0.02em;
    animation: fadeUp 0.5s ease-out 0.2s both;
}
.hero-heading span {
    background: linear-gradient(135deg, var(--amber) 0%, var(--violet) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-desc {
    color: var(--text-2);
    font-size: 0.92rem;
    line-height: 1.7;
    margin: 0 0 1.3rem;
    max-width: 620px;
    animation: fadeUp 0.5s ease-out 0.3s both;
}
.hero-desc code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: var(--amber);
    background: var(--amber-dim);
    padding: 0.12rem 0.45rem;
    border-radius: 5px;
}
.hero-tags {
    display: flex; gap: 0.55rem; flex-wrap: wrap;
    animation: fadeUp 0.5s ease-out 0.4s both;
}
.htag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.64rem;
    padding: 0.28rem 0.8rem;
    border-radius: 100px;
    font-weight: 600;
    letter-spacing: 0.03em;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.htag:hover { transform: translateY(-2px); }
.htag-a { background: var(--amber-dim);   color: var(--amber);   border: 1px solid rgba(251,191,36,0.2); }
.htag-v { background: var(--violet-dim);  color: var(--violet);  border: 1px solid rgba(167,139,250,0.2); }
.htag-e { background: var(--emerald-dim); color: var(--emerald); border: 1px solid rgba(52,211,153,0.2); }
.htag-a:hover { box-shadow: 0 4px 16px rgba(251,191,36,0.15); }
.htag-v:hover { box-shadow: 0 4px 16px rgba(167,139,250,0.15); }
.htag-e:hover { box-shadow: 0 4px 16px rgba(52,211,153,0.15); }

/* ─── SETTINGS CARD ──────────────────────────────────────── */
.settings-card {
    background: var(--bg-card);
    backdrop-filter: blur(20px) saturate(1.3);
    border-radius: var(--radius);
    padding: 1.5rem 1.6rem;
    border: 1px solid var(--border-1);
    animation: fadeScale 0.6s ease-out;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
    position: relative;
    overflow: hidden;
    margin-bottom: 1.2rem;
}
.settings-card:hover {
    border-color: rgba(34,211,238,0.2);
    box-shadow: 0 0 24px rgba(34,211,238,0.04);
}
.settings-card-bar {
    position: absolute;
    top: 0; left: 1.2rem; right: 1.2rem;
    height: 2px;
    border-radius: 0 0 2px 2px;
    background: linear-gradient(90deg, var(--cyan), var(--violet));
    opacity: 0.4;
}
.settings-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--cyan);
    margin-bottom: 0.8rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.settings-label::before {
    content: '';
    width: 5px; height: 5px;
    border-radius: 50%;
    background: var(--cyan);
    display: inline-block;
    animation: dotPulse 2s ease-in-out infinite;
    color: var(--cyan);
}

/* ─── ALGORITHM CARD ─────────────────────────────────────── */
.algo-box {
    background: var(--bg-card);
    backdrop-filter: blur(20px) saturate(1.3);
    border-radius: var(--radius);
    padding: 1.6rem 1.5rem;
    height: 100%;
    border: 1px solid var(--border-1);
    animation: fadeScale 0.6s ease-out 0.2s both;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
    position: relative;
    overflow: hidden;
}
.algo-box:hover {
    border-color: var(--accent, var(--cyan));
    box-shadow: 0 0 30px rgba(34,211,238,0.05);
}
.algo-box-bar {
    position: absolute;
    top: 0; left: 1.2rem; right: 1.2rem;
    height: 2px;
    border-radius: 0 0 2px 2px;
    opacity: 0.5;
}
.algo-box-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    margin-bottom: 1rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.algo-box-label::before {
    content: '';
    width: 5px; height: 5px;
    border-radius: 50%;
    display: inline-block;
    animation: dotPulse 2s ease-in-out infinite;
}
.algo-steps {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.73rem;
    color: var(--text-2);
    line-height: 2.2;
    margin-bottom: 1rem;
}
.algo-steps .sn { color: var(--text-3); font-size: 0.65rem; margin-right: 0.3rem; }
.algo-steps .sh { color: var(--text-1); font-weight: 600; }
.algo-props { display: flex; flex-direction: column; gap: 0.4rem; }
.algo-prop {
    display: flex; align-items: center; gap: 0.5rem;
    font-family: 'Inter', sans-serif;
    font-size: 0.68rem;
    font-weight: 500;
    padding: 0.3rem 0.6rem;
    border-radius: 6px;
    transition: transform 0.2s ease;
}
.algo-prop:hover { transform: translateX(4px); }
.prop-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.prop-amber  { background: var(--amber-dim);  color: var(--amber); }
.prop-green  { background: var(--emerald-dim); color: var(--emerald); }
.prop-violet { background: var(--violet-dim);  color: var(--violet); }
.prop-amber  .prop-dot { background: var(--amber); }
.prop-green  .prop-dot { background: var(--emerald); }
.prop-violet .prop-dot { background: var(--violet); }

/* ─── RUN BUTTON ─────────────────────────────────────────── */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #0ea5e9, #6366f1, #a855f7) !important;
    background-size: 200% 200% !important;
    animation: gradientShift 5s ease infinite !important;
    border: none !important;
    border-radius: 14px !important;
    color: #fff !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.8rem 1.5rem !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.3) !important;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(99,102,241,0.45) !important;
    filter: brightness(1.08) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:active {
    transform: translateY(0) scale(0.98) !important;
}

/* ─── INPUTS ─────────────────────────────────────────────── */
div[data-testid="stTextInput"] > div > div > input,
div[data-testid="stNumberInput"] input {
    background: var(--bg-1) !important;
    border: 1.5px solid rgba(34,211,238,0.1) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-1) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stTextInput"] > div > div > input:focus,
div[data-testid="stNumberInput"] input:focus {
    border-color: rgba(34,211,238,0.4) !important;
    box-shadow: 0 0 0 3px rgba(34,211,238,0.06) !important;
}

/* ─── TABS ───────────────────────────────────────────────── */
div[data-testid="stTabs"] > div:first-child {
    border-bottom: 1px solid rgba(255,255,255,0.05) !important;
    gap: 0.15rem;
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

/* ─── METRIC CARDS ───────────────────────────────────────── */
.m-card {
    background: var(--bg-glass);
    backdrop-filter: blur(16px);
    border: 1px solid var(--border-1);
    border-radius: var(--radius);
    padding: 1.2rem 1.3rem;
    text-align: center;
    animation: fadeUp 0.5s ease-out both;
    transition: all 0.35s ease;
    position: relative;
}
.m-card:hover {
    transform: translateY(-4px);
    border-color: var(--m-accent, var(--cyan));
    box-shadow: 0 8px 28px rgba(0,0,0,0.25);
}
.m-card-bar {
    position: absolute;
    top: 0; left: 20%; right: 20%;
    height: 2px;
    border-radius: 0 0 4px 4px;
    opacity: 0.4;
}
.m-card-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 0.6rem;
    font-size: 0.8rem;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
}
.m-card-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-0);
    margin-bottom: 0.25rem;
    letter-spacing: -0.01em;
}
.m-card-lbl {
    font-family: 'Inter', sans-serif;
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-3);
}

/* ─── RESULT BANNERS ─────────────────────────────────────── */
.res-banner {
    border-radius: 14px;
    padding: 1rem 1.4rem;
    display: flex;
    align-items: center;
    gap: 0.9rem;
    margin: 1rem 0;
    animation: fadeUp 0.4s ease-out;
    backdrop-filter: blur(12px);
}
.res-ok {
    background: linear-gradient(135deg, rgba(52,211,153,0.08), rgba(52,211,153,0.02));
    border: 1px solid rgba(52,211,153,0.25);
}
.res-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
    animation: softPulse 2s ease-in-out infinite;
    background: var(--emerald);
    box-shadow: 0 0 10px var(--emerald);
}
.res-msg {
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--text-1);
}

/* ─── CHART WRAPPER ──────────────────────────────────────── */
.chart-wrap {
    border-radius: var(--radius);
    overflow: hidden;
    border: 1px solid var(--border-1);
    background: var(--bg-card);
    padding: 0.3rem;
    animation: fadeScale 0.5s ease-out;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}
.chart-wrap:hover {
    border-color: rgba(34,211,238,0.2);
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
}

/* ─── SECTION TITLE ──────────────────────────────────────── */
.sec-title {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 0.75rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-3);
    margin: 1.5rem 0 0.8rem;
    display: flex; align-items: center; gap: 0.6rem;
    animation: fadeUp 0.4s ease-out;
}
.sec-title-bar {
    width: 16px; height: 3px;
    border-radius: 3px;
    background: linear-gradient(90deg, var(--cyan), var(--violet));
    display: inline-block;
}

/* ─── METHOD SUBTITLE ────────────────────────────────────── */
.method-sub {
    font-size: 0.88rem;
    color: var(--text-2);
    font-weight: 400;
    margin-bottom: 1.3rem;
    padding-left: 0.9rem;
    border-left: 2.5px solid var(--accent, var(--cyan));
    line-height: 1.65;
    animation: slideRight 0.4s ease-out;
}

/* ─── STATUS ROW ─────────────────────────────────────────── */
.status-row {
    display: flex; align-items: center; gap: 0.5rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-3);
    margin: 0.5rem 0;
    animation: fadeUp 0.35s ease-out;
}
.s-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--emerald);
    box-shadow: 0 0 6px var(--emerald);
    animation: softPulse 2s ease-in-out infinite;
}

/* ─── MISC ───────────────────────────────────────────────── */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(34,211,238,0.12), rgba(167,139,250,0.12), transparent) !important;
    margin: 1.8rem 0 !important;
}
div[data-testid="stExpander"] > details {
    background: rgba(12,16,33,0.6) !important;
    border: 1px solid rgba(34,211,238,0.07) !important;
    border-radius: 14px !important;
    backdrop-filter: blur(10px);
}
div[data-testid="stExpander"] summary {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    color: var(--text-2) !important;
}
div[data-testid="stExpander"] summary:hover {
    color: var(--text-1) !important;
}
div[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid rgba(34,211,238,0.07) !important;
}
div[data-testid="stSlider"] > div { color: var(--text-2) !important; }
</style>
"""

PARTICLE_HTML = """
<canvas id="pCanvas3" style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:0;"></canvas>
<script>
(function(){
    var c=document.getElementById('pCanvas3');if(!c)return;
    var ctx=c.getContext('2d'),w,h,pts=[];
    function rs(){w=c.width=window.innerWidth;h=c.height=window.innerHeight;}
    rs();window.addEventListener('resize',rs);
    var cols=['#a78bfa','#34d399','#fbbf24','#22d3ee'];
    for(var i=0;i<40;i++){
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
                if(d<100){ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(pts[j].x,pts[j].y);
                    ctx.strokeStyle=p.c;ctx.globalAlpha=0.035*(1-d/100);ctx.lineWidth=0.5;ctx.stroke();}
            }
        }
        ctx.globalAlpha=1;requestAnimationFrame(draw);
    }
    draw();
})();
</script>
"""


# ─────────────────────────────────────────────
# METHOD 1: TRAPEZOIDAL RULE (LOGIC UNTOUCHED)
# ─────────────────────────────────────────────
def trapezoidal_rule(func, a: float, b: float, n: int):
    h      = (b - a) / n
    x_vals = np.linspace(a, b, n + 1)
    y_vals = np.vectorize(func)(x_vals)
    result = (h / 2) * (y_vals[0] + 2 * np.sum(y_vals[1:-1]) + y_vals[-1])
    return result, x_vals, y_vals


# ─────────────────────────────────────────────
# METHOD 2: SIMPSON'S RULE (LOGIC UNTOUCHED)
# ─────────────────────────────────────────────
def simpsons_rule(func, a: float, b: float, n: int):
    if n % 2 != 0:
        n += 1
    h      = (b - a) / n
    x_vals = np.linspace(a, b, n + 1)
    y_vals = np.vectorize(func)(x_vals)
    coeffs       = np.ones(n + 1)
    coeffs[1:-1] = np.where(np.arange(1, n) % 2 == 1, 4, 2)
    result = (h / 3) * np.dot(coeffs, y_vals)
    return result, x_vals, y_vals


# ─────────────────────────────────────────────
# METHOD 3: MIDPOINT RULE (LOGIC UNTOUCHED)
# ─────────────────────────────────────────────
def midpoint_rule(func, a: float, b: float, n: int):
    h          = (b - a) / n
    mid_points = np.array([a + (i + 0.5) * h for i in range(n)])
    y_vals     = np.vectorize(func)(mid_points)
    result     = h * np.sum(y_vals)
    return result, mid_points, y_vals


# ══════════════════════════════════════════════════════════════════════════════
# PLOTLY INTERACTIVE VISUALIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

def _plotly_layout():
    """Shared Plotly axis & layout styling."""
    return dict(
        gridcolor='rgba(30,41,59,0.5)', gridwidth=0.5,
        zerolinecolor='#1e293b', zerolinewidth=1,
        linecolor='#1e293b', linewidth=0.6,
        tickfont=dict(size=10, color='#4b5574', family='JetBrains Mono'),
        title_font=dict(size=11, color='#64748b', family='Inter'),
    )


def plot_integration_interactive(func, a, b, x_vals, y_vals, method_name, result, accent='#22d3ee'):
    """
    Two-panel interactive Plotly chart:
      Left  — function curve with shaded area + method-specific overlays
      Right — subinterval contribution bar chart with cumulative line
    """
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(
            f'<b>{method_name}</b>  ·  Result = {result:.8f}',
            '<b>Subinterval Contributions</b>'
        ),
        horizontal_spacing=0.1,
        column_widths=[0.55, 0.45],
        specs=[[{"secondary_y": False}, {"secondary_y": True}]]
    )

    ax = _plotly_layout()

    # ── LEFT: function curve + area ───────────────────────────────────────────
    margin = abs(b - a) * 0.25
    x_fine = np.linspace(a - margin, b + margin, 800)
    try:
        y_fine = np.vectorize(func)(x_fine)
    except Exception:
        y_fine = np.zeros_like(x_fine)

    # Shaded integration region
    x_shade = np.linspace(a, b, 600)
    try:
        y_shade = np.vectorize(func)(x_shade)
    except Exception:
        y_shade = np.zeros_like(x_shade)

    fig.add_trace(go.Scatter(
        x=x_shade, y=y_shade,
        fill='tozeroy', fillcolor='rgba(167,139,250,0.12)',
        line=dict(width=0), name='Integration Area',
        hoverinfo='skip'
    ), row=1, col=1)

    # Glow line
    fig.add_trace(go.Scatter(
        x=x_fine, y=y_fine, mode='lines',
        line=dict(color=accent, width=6), opacity=0.1,
        showlegend=False, hoverinfo='skip'
    ), row=1, col=1)

    # Sharp curve
    fig.add_trace(go.Scatter(
        x=x_fine, y=y_fine, mode='lines', name='f(x)',
        line=dict(color=accent, width=2.5, shape='spline'),
        hovertemplate='<b>x</b> = %{x:.4f}<br><b>f(x)</b> = %{y:.6f}<extra></extra>'
    ), row=1, col=1)

    # Method-specific overlays
    if 'Trapezoidal' in method_name:
        for i in range(len(x_vals) - 1):
            xs = [x_vals[i], x_vals[i], x_vals[i+1], x_vals[i+1], x_vals[i]]
            ys_trap = [0, y_vals[i], y_vals[i+1], 0, 0]
            fig.add_trace(go.Scatter(
                x=xs, y=ys_trap, fill='toself',
                fillcolor='rgba(251,191,36,0.1)',
                line=dict(color='rgba(251,191,36,0.4)', width=1),
                showlegend=(i == 0), name='Trapezoids' if i == 0 else None,
                hoverinfo='skip'
            ), row=1, col=1)
        # Node points
        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals, mode='markers',
            name='Nodes',
            marker=dict(size=7, color='#fbbf24', line=dict(width=1.5, color='#fef3c7')),
            hovertemplate='<b>Node %{pointNumber}</b><br>x=%{x:.4f}<br>f(x)=%{y:.6f}<extra></extra>'
        ), row=1, col=1)

    elif 'Simpson' in method_name:
        for i in range(len(x_vals) - 1):
            xs = [x_vals[i], x_vals[i], x_vals[i+1], x_vals[i+1], x_vals[i]]
            ys_s = [0, y_vals[i], y_vals[i+1], 0, 0]
            fig.add_trace(go.Scatter(
                x=xs, y=ys_s, fill='toself',
                fillcolor='rgba(167,139,250,0.1)',
                line=dict(color='rgba(167,139,250,0.35)', width=1),
                showlegend=(i == 0), name='Parabolic Segments' if i == 0 else None,
                hoverinfo='skip'
            ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals, mode='markers',
            name='Nodes',
            marker=dict(size=7, color='#a78bfa', line=dict(width=1.5, color='#ddd6fe')),
            hovertemplate='<b>Node %{pointNumber}</b><br>x=%{x:.4f}<br>f(x)=%{y:.6f}<extra></extra>'
        ), row=1, col=1)

    elif 'Midpoint' in method_name:
        n = len(x_vals)
        h = (b - a) / n
        for i in range(n):
            rx = x_vals[i] - h / 2
            fig.add_shape(
                type='rect', x0=rx, x1=rx + h, y0=0, y1=y_vals[i],
                fillcolor='rgba(52,211,153,0.1)',
                line=dict(color='rgba(52,211,153,0.35)', width=1),
                row=1, col=1
            )
        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals, mode='markers',
            name='Midpoints',
            marker=dict(size=8, color='#fbbf24', symbol='diamond',
                       line=dict(width=1.5, color='#fef3c7')),
            hovertemplate='<b>Mid %{pointNumber}</b><br>x=%{x:.4f}<br>f(x)=%{y:.6f}<extra></extra>'
        ), row=1, col=1)

    fig.add_hline(y=0, line=dict(color='#1e293b', width=1.2), row=1, col=1)

    # ── RIGHT: bar chart + cumulative ─────────────────────────────────────────
    if 'Midpoint' in method_name:
        n_bars = len(x_vals)
        h_val = (b - a) / n_bars
        contribs = np.abs(y_vals) * h_val
        bar_colors = [accent if v >= 0 else '#fb7185' for v in y_vals]
        bar_labels = [f'Mid {i+1}' for i in range(n_bars)]
    else:
        n_bars = len(x_vals) - 1
        contribs = []
        bar_colors = []
        bar_labels = []
        for i in range(n_bars):
            seg = abs(y_vals[i] + y_vals[i+1]) / 2 * abs(x_vals[i+1] - x_vals[i])
            contribs.append(seg)
            bar_colors.append(accent if y_vals[i] >= 0 else '#fb7185')
            bar_labels.append(f'Seg {i+1}')
        contribs = np.array(contribs)

    bar_x = list(range(len(contribs)))

    # Highlight max
    max_idx = int(np.argmax(contribs)) if len(contribs) > 0 else 0
    border_colors = ['rgba(251,191,36,0.8)' if i == max_idx else 'rgba(30,41,59,0.4)' for i in range(len(contribs))]
    border_widths = [2.5 if i == max_idx else 0.8 for i in range(len(contribs))]

    fig.add_trace(go.Bar(
        x=bar_x, y=contribs,
        name='|Contribution|',
        marker=dict(color=bar_colors, line=dict(color=border_colors, width=border_widths),
                    opacity=0.8),
        hovertemplate='<b>%{text}</b><br>Contribution: %{y:.6f}<extra></extra>',
        text=bar_labels,
    ), row=1, col=2, secondary_y=False)

    # Cumulative line
    cumsum = np.cumsum(contribs)
    fig.add_trace(go.Scatter(
        x=bar_x, y=cumsum,
        mode='lines+markers', name='Cumulative',
        line=dict(color='#22d3ee', width=2.5, shape='spline'),
        marker=dict(size=5, color='#22d3ee', line=dict(width=1, color='#a5f3fc')),
        hovertemplate='<b>Cumulative</b><br>Sum: %{y:.6f}<extra></extra>',
    ), row=1, col=2, secondary_y=True)

    # Layout
    fig.update_layout(
        height=480, plot_bgcolor='#0c1021', paper_bgcolor='#07090f',
        font=dict(family='Inter', color='#8b95b0', size=12),
        legend=dict(
            bgcolor='rgba(12,16,33,0.9)', bordercolor='rgba(34,211,238,0.1)', borderwidth=1,
            font=dict(size=10, color='#e8ecf4', family='Inter'),
            orientation='h', yanchor='bottom', y=-0.25, xanchor='center', x=0.5,
        ),
        margin=dict(l=55, r=45, t=55, b=75),
        hoverlabel=dict(
            bgcolor='rgba(12,16,33,0.95)', bordercolor='rgba(34,211,238,0.2)',
            font=dict(family='JetBrains Mono', size=12, color='#e8ecf4')
        ),
        bargap=0.15,
    )

    fig.update_xaxes(title_text='x', **ax, row=1, col=1)
    fig.update_yaxes(title_text='f(x)', **ax, row=1, col=1)
    fig.update_xaxes(title_text='Subinterval Index', **ax, row=1, col=2)
    fig.update_yaxes(title_text='|Contribution|', **ax, row=1, col=2, secondary_y=False)
    fig.update_yaxes(title_text='Cumulative Sum', color='#22d3ee',
                     tickfont=dict(color='#22d3ee', size=9, family='JetBrains Mono'),
                     title_font=dict(color='#22d3ee', size=10, family='Inter'),
                     gridcolor='rgba(34,211,238,0.05)',
                     row=1, col=2, secondary_y=True)

    for ann in fig.layout.annotations:
        ann.font = dict(size=12, color='#e8ecf4', family='Inter')

    return fig


def plot_comparison_interactive(func, a, b, n_max=50):
    """Interactive convergence comparison of all three methods."""
    n_vals = list(range(2, n_max + 1, 2))
    trap_v, simp_v, mid_v = [], [], []

    for n in n_vals:
        try:
            trap_v.append(trapezoidal_rule(func, a, b, n)[0])
            simp_v.append(simpsons_rule(func, a, b, n)[0])
            mid_v.append(midpoint_rule(func, a, b, n)[0])
        except Exception:
            trap_v.append(np.nan)
            simp_v.append(np.nan)
            mid_v.append(np.nan)

    fig = go.Figure()
    ax = _plotly_layout()

    for vals, name, color, symbol in [
        (trap_v, 'Trapezoidal', '#fbbf24', 'circle'),
        (simp_v, "Simpson's 1/3", '#a78bfa', 'square'),
        (mid_v,  'Midpoint',     '#34d399', 'diamond'),
    ]:
        # Glow
        fig.add_trace(go.Scatter(
            x=n_vals, y=vals, mode='lines',
            line=dict(color=color, width=6), opacity=0.08,
            showlegend=False, hoverinfo='skip'
        ))
        # Sharp
        fig.add_trace(go.Scatter(
            x=n_vals, y=vals, mode='lines+markers',
            name=name,
            line=dict(color=color, width=2.5, shape='spline'),
            marker=dict(size=6, color=color, symbol=symbol,
                       line=dict(width=1, color='#fff')),
            hovertemplate=f'<b>{name}</b><br>n=%{{x}}<br>Value=%{{y:.8f}}<extra></extra>'
        ))

    fig.update_layout(
        height=420, plot_bgcolor='#0c1021', paper_bgcolor='#07090f',
        title=dict(text='<b>Convergence Comparison</b>  ·  All Methods vs n',
                   font=dict(size=13, color='#e8ecf4', family='Inter'), x=0.5),
        font=dict(family='Inter', color='#8b95b0', size=12),
        legend=dict(
            bgcolor='rgba(12,16,33,0.9)', bordercolor='rgba(34,211,238,0.1)', borderwidth=1,
            font=dict(size=10.5, color='#e8ecf4', family='Inter'),
            orientation='h', yanchor='bottom', y=-0.22, xanchor='center', x=0.5,
        ),
        margin=dict(l=60, r=30, t=60, b=75),
        hoverlabel=dict(
            bgcolor='rgba(12,16,33,0.95)', bordercolor='rgba(34,211,238,0.2)',
            font=dict(family='JetBrains Mono', size=12, color='#e8ecf4')
        ),
        xaxis=dict(title='Number of Subintervals (n)', **ax),
        yaxis=dict(title='Approximate Integral Value', **ax),
    )

    return fig


# ══════════════════════════════════════════════════════════════════════════════
# RESULTS DISPLAY
# ══════════════════════════════════════════════════════════════════════════════

def _show_integration_result(func, a, b, n, x_vals, y_vals, result, method_name, accent='#22d3ee'):
    """Premium results display: banner + metrics + interactive chart + table."""

    h_val = (b - a) / n

    # Success banner
    st.markdown(f"""
    <div class="res-banner res-ok">
        <span class="res-dot"></span>
        <span class="res-msg">Integration complete — {method_name} with n={n} subintervals</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # Metric cards
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="m-card" style="animation-delay:.1s;">
            <div class="m-card-bar" style="background:var(--amber);"></div>
            <div class="m-card-icon" style="color:var(--amber);background:var(--amber-dim);">S</div>
            <div class="m-card-val">{result:.8f}</div>
            <div class="m-card-lbl">Integral Result</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="m-card" style="animation-delay:.2s;">
            <div class="m-card-bar" style="background:var(--cyan);"></div>
            <div class="m-card-icon" style="color:var(--cyan);background:var(--cyan-dim);">n</div>
            <div class="m-card-val">{n}</div>
            <div class="m-card-lbl">Subintervals</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="m-card" style="animation-delay:.3s;">
            <div class="m-card-bar" style="background:var(--violet);"></div>
            <div class="m-card-icon" style="color:var(--violet);background:var(--violet-dim);">h</div>
            <div class="m-card-val">{h_val:.6f}</div>
            <div class="m-card-lbl">Step Size</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)

    # Interactive chart
    st.markdown('<div class="sec-title"><span class="sec-title-bar"></span>Interactive Visualization</div>',
                unsafe_allow_html=True)

    fig = plot_integration_interactive(func, a, b, x_vals, y_vals, method_name, result, accent)
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': True, 'displaylogo': False,
        'toImageButtonOptions': {'format': 'png', 'filename': f'{method_name}_result', 'scale': 2}
    })
    st.markdown('</div>', unsafe_allow_html=True)

    # Status
    st.markdown(f"""
    <div class="status-row">
        <span class="s-dot"></span>
        Complete · {method_name} · {n} subintervals · h = {h_val:.6f} · hover chart to explore
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN RENDERER
# ══════════════════════════════════════════════════════════════════════════════

def render_lab3():
    st.markdown(LAB3_CSS, unsafe_allow_html=True)
    st.components.v1.html(PARTICLE_HTML, height=0, scrolling=False)

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-section">
        <div class="hero-label"><span class="hero-label-bar"></span>Lab 03 · Numerical Methods</div>
        <div class="hero-heading">Numerical <span>Integration</span></div>
        <p class="hero-desc">
            Approximate definite integrals <code>&#8747; f(x) dx</code> using three classical
            quadrature methods. Fully interactive graphs — hover, zoom, pan to explore
            every subinterval contribution.
        </p>
        <div class="hero-tags">
            <span class="htag htag-a">Trapezoidal · O(h²)</span>
            <span class="htag htag-v">Simpson's 1/3 · O(h⁴)</span>
            <span class="htag htag-e">Midpoint · O(h²)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Common Settings ───────────────────────────────────────────────────────
    st.markdown("""
    <div class="settings-card">
        <div class="settings-card-bar"></div>
        <div class="settings-label">Common Settings</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    func_str = col1.text_input("f(x) =", value="x**2", key="int_func",
                                help="e.g. sin(x), 2/(x-4), ln(x), e^x, sqrt(x), x^2+3x")
    a_val = col2.number_input("Lower limit a", value=0.0, key="int_a")
    b_val = col3.number_input("Upper limit b", value=1.0, key="int_b")
    n_val = col4.number_input("Subintervals n", value=10, min_value=2, step=2, key="int_n")

    with st.expander("Function syntax guide", expanded=False):
        show_function_guide()

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "Trapezoidal", "Simpson's 1/3", "Midpoint", "Comparison"
    ])

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 1 — TRAPEZOIDAL
    # ══════════════════════════════════════════════════════════════════════════
    with tab1:
        st.markdown("""
        <p class="method-sub" style="--accent: var(--amber);">
            Connects adjacent points with straight lines forming trapezoids.
            Simple, robust, and works for any continuous function.
        </p>
        """, unsafe_allow_html=True)

        ci, ca = st.columns([1.3, 1], gap="large")
        with ci:
            st.markdown("""
            <div class="method-sub" style="--accent:var(--amber); font-size:0.82rem; color:var(--text-2); margin-bottom:0;">
                Uses linear interpolation between each pair of adjacent nodes to form
                trapezoidal panels. The sum of all panel areas approximates the integral.
                Error decreases quadratically as n increases.
            </div>
            """, unsafe_allow_html=True)

        with ca:
            st.markdown("""
            <div class="algo-box" style="--accent: var(--amber);">
                <div class="algo-box-bar" style="background: var(--amber);"></div>
                <div class="algo-box-label" style="color: var(--amber);">Trapezoidal Rule</div>
                <div class="algo-steps">
                    <span class="sn">01</span> <span class="sh">h = (b − a) / n</span><br>
                    <span class="sn">02</span> I = (h/2) · [f(x₀) + 2f(x₁) + ... + f(xₙ)]<br>
                </div>
                <div class="algo-props">
                    <div class="algo-prop prop-amber"><span class="prop-dot"></span>Error Order: O(h²)</div>
                    <div class="algo-prop prop-green"><span class="prop-dot"></span>Works for any continuous f</div>
                    <div class="algo-prop prop-violet"><span class="prop-dot"></span>Linear interpolation</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
        if st.button("Run Trapezoidal", key="run_trap", use_container_width=True, type="primary"):
            func, err = parse_function(func_str)
            if err:
                st.error(f"Parse error: {err}")
            elif a_val >= b_val:
                st.error("Upper limit b must be greater than lower limit a.")
            else:
                with st.spinner("Computing..."):
                    result, x_vals, y_vals = trapezoidal_rule(func, a_val, b_val, int(n_val))
                _show_integration_result(func, a_val, b_val, int(n_val), x_vals, y_vals,
                                          result, "Trapezoidal Rule", '#fbbf24')

                with st.expander("Node values table", expanded=False):
                    import pandas as pd
                    df = pd.DataFrame({'x': x_vals, 'f(x)': y_vals})
                    df.index += 1
                    st.dataframe(df.style.format({'x': '{:.6f}', 'f(x)': '{:.6f}'}),
                                 use_container_width=True)

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 2 — SIMPSON'S
    # ══════════════════════════════════════════════════════════════════════════
    with tab2:
        st.markdown("""
        <p class="method-sub" style="--accent: var(--violet);">
            Fits parabolic arcs through groups of three adjacent points for
            higher-order accuracy. Requires an even number of subintervals.
        </p>
        """, unsafe_allow_html=True)

        ci, ca = st.columns([1.3, 1], gap="large")
        with ci:
            st.markdown("""
            <div class="method-sub" style="--accent:var(--violet); font-size:0.82rem; color:var(--text-2); margin-bottom:0;">
                Uses quadratic (parabolic) interpolation over pairs of subintervals.
                Achieves O(h⁴) accuracy — far more precise than trapezoidal for smooth functions.
                If n is odd, it is automatically corrected to even.
            </div>
            """, unsafe_allow_html=True)

        with ca:
            st.markdown("""
            <div class="algo-box" style="--accent: var(--violet);">
                <div class="algo-box-bar" style="background: var(--violet);"></div>
                <div class="algo-box-label" style="color: var(--violet);">Simpson's 1/3 Rule</div>
                <div class="algo-steps">
                    <span class="sn">01</span> <span class="sh">h = (b − a) / n</span> &nbsp;(n must be even)<br>
                    <span class="sn">02</span> I = (h/3)·[f(x₀)+4f(x₁)+2f(x₂)+...+f(xₙ)]<br>
                </div>
                <div class="algo-props">
                    <div class="algo-prop prop-amber"><span class="prop-dot"></span>Error Order: O(h⁴) — very accurate</div>
                    <div class="algo-prop prop-green"><span class="prop-dot"></span>Parabolic interpolation</div>
                    <div class="algo-prop prop-violet"><span class="prop-dot"></span>Requires even n</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
        if st.button("Run Simpson's", key="run_simp", use_container_width=True, type="primary"):
            func, err = parse_function(func_str)
            if err:
                st.error(f"Parse error: {err}")
            elif a_val >= b_val:
                st.error("Upper limit b must be greater than lower limit a.")
            else:
                n_use = int(n_val) if int(n_val) % 2 == 0 else int(n_val) + 1
                if n_use != int(n_val):
                    st.markdown(f"""
                    <div class="status-row">
                        <span class="s-dot" style="background:var(--amber);box-shadow:0 0 6px var(--amber);"></span>
                        n={int(n_val)} was odd — auto-corrected to n={n_use}
                    </div>
                    """, unsafe_allow_html=True)

                with st.spinner("Computing..."):
                    result, x_vals, y_vals = simpsons_rule(func, a_val, b_val, n_use)
                _show_integration_result(func, a_val, b_val, n_use, x_vals, y_vals,
                                          result, "Simpson's 1/3 Rule", '#a78bfa')

                with st.expander("Node values with coefficients", expanded=False):
                    import pandas as pd
                    coeffs = np.ones(n_use + 1)
                    coeffs[1:-1] = np.where(np.arange(1, n_use) % 2 == 1, 4, 2)
                    df = pd.DataFrame({'x': x_vals, 'f(x)': y_vals, 'Coeff': coeffs.astype(int)})
                    df.index += 1
                    st.dataframe(df.style.format({'x': '{:.6f}', 'f(x)': '{:.6f}'}),
                                 use_container_width=True)

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 3 — MIDPOINT
    # ══════════════════════════════════════════════════════════════════════════
    with tab3:
        st.markdown("""
        <p class="method-sub" style="--accent: var(--emerald);">
            Evaluates f(x) at the midpoint of each subinterval and forms rectangles.
            Simpler than trapezoidal, yet often more accurate for smooth functions.
        </p>
        """, unsafe_allow_html=True)

        ci, ca = st.columns([1.3, 1], gap="large")
        with ci:
            st.markdown("""
            <div class="method-sub" style="--accent:var(--emerald); font-size:0.82rem; color:var(--text-2); margin-bottom:0;">
                Instead of sampling at the endpoints, the midpoint rule evaluates f at the
                center of each panel. This often cancels errors better than endpoint methods,
                yielding surprisingly good results for smooth functions.
            </div>
            """, unsafe_allow_html=True)

        with ca:
            st.markdown("""
            <div class="algo-box" style="--accent: var(--emerald);">
                <div class="algo-box-bar" style="background: var(--emerald);"></div>
                <div class="algo-box-label" style="color: var(--emerald);">Midpoint Rule</div>
                <div class="algo-steps">
                    <span class="sn">01</span> <span class="sh">mᵢ = a + (i + ½) · h</span><br>
                    <span class="sn">02</span> <span class="sh">I = h · &#931; f(mᵢ)</span><br>
                </div>
                <div class="algo-props">
                    <div class="algo-prop prop-amber"><span class="prop-dot"></span>Error Order: O(h²)</div>
                    <div class="algo-prop prop-green"><span class="prop-dot"></span>Often beats trapezoidal in practice</div>
                    <div class="algo-prop prop-violet"><span class="prop-dot"></span>Center-point sampling</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
        if st.button("Run Midpoint", key="run_mid", use_container_width=True, type="primary"):
            func, err = parse_function(func_str)
            if err:
                st.error(f"Parse error: {err}")
            elif a_val >= b_val:
                st.error("Upper limit b must be greater than lower limit a.")
            else:
                with st.spinner("Computing..."):
                    result, mid_pts, y_vals = midpoint_rule(func, a_val, b_val, int(n_val))
                _show_integration_result(func, a_val, b_val, int(n_val), mid_pts, y_vals,
                                          result, "Midpoint Rule", '#34d399')

                with st.expander("Midpoint values table", expanded=False):
                    import pandas as pd
                    df = pd.DataFrame({'Midpoint x': mid_pts, 'f(midpoint)': y_vals})
                    df.index += 1
                    st.dataframe(df.style.format('{:.8f}'), use_container_width=True)

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 4 — COMPARISON
    # ══════════════════════════════════════════════════════════════════════════
    with tab4:
        st.markdown("""
        <p class="method-sub" style="--accent: var(--cyan);">
            Compare all three methods side-by-side as the number of subintervals increases.
            Watch how each method converges to the true integral value.
        </p>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        n_max_cmp = c1.slider("Max n for comparison", 4, 100, 40, step=2, key="cmp_nmax")

        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
        if st.button("Run Comparison", key="run_cmp", use_container_width=True, type="primary"):
            func, err = parse_function(func_str)
            if err:
                st.error(f"Parse error: {err}")
            elif a_val >= b_val:
                st.error("Upper limit b must be greater than lower limit a.")
            else:
                with st.spinner("Computing all methods..."):
                    r_trap, _, _ = trapezoidal_rule(func, a_val, b_val, int(n_val))
                    n_even = int(n_val) if int(n_val) % 2 == 0 else int(n_val) + 1
                    r_simp, _, _ = simpsons_rule(func, a_val, b_val, n_even)
                    r_mid, _, _ = midpoint_rule(func, a_val, b_val, int(n_val))

                # Results at current n
                st.markdown(f"""
                <div class="res-banner res-ok">
                    <span class="res-dot"></span>
                    <span class="res-msg">Comparison complete — results at n={int(n_val)}</span>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(f"""
                    <div class="m-card" style="animation-delay:.1s;">
                        <div class="m-card-bar" style="background:var(--amber);"></div>
                        <div class="m-card-icon" style="color:var(--amber);background:var(--amber-dim);">T</div>
                        <div class="m-card-val">{r_trap:.8f}</div>
                        <div class="m-card-lbl">Trapezoidal</div>
                    </div>
                    """, unsafe_allow_html=True)

                with c2:
                    st.markdown(f"""
                    <div class="m-card" style="animation-delay:.2s;">
                        <div class="m-card-bar" style="background:var(--violet);"></div>
                        <div class="m-card-icon" style="color:var(--violet);background:var(--violet-dim);">S</div>
                        <div class="m-card-val">{r_simp:.8f}</div>
                        <div class="m-card-lbl">Simpson's</div>
                    </div>
                    """, unsafe_allow_html=True)

                with c3:
                    st.markdown(f"""
                    <div class="m-card" style="animation-delay:.3s;">
                        <div class="m-card-bar" style="background:var(--emerald);"></div>
                        <div class="m-card-icon" style="color:var(--emerald);background:var(--emerald-dim);">M</div>
                        <div class="m-card-val">{r_mid:.8f}</div>
                        <div class="m-card-lbl">Midpoint</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)

                # Convergence chart
                st.markdown('<div class="sec-title"><span class="sec-title-bar"></span>Convergence as n Increases</div>',
                            unsafe_allow_html=True)

                fig = plot_comparison_interactive(func, a_val, b_val, n_max=n_max_cmp)
                st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True, config={
                    'displayModeBar': True, 'displaylogo': False,
                    'toImageButtonOptions': {'format': 'png', 'filename': 'comparison', 'scale': 2}
                })
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("""
                <div class="status-row">
                    <span class="s-dot"></span>
                    All three methods computed · hover graph to see exact values at each n
                </div>
                """, unsafe_allow_html=True)

                # Value table
                with st.expander("Value table (first 10 even n)", expanded=False):
                    import pandas as pd
                    n_list = list(range(2, min(n_max_cmp, 20) + 1, 2))
                    rows = []
                    for nn in n_list:
                        t, _, _ = trapezoidal_rule(func, a_val, b_val, nn)
                        nn_e = nn if nn % 2 == 0 else nn + 1
                        s, _, _ = simpsons_rule(func, a_val, b_val, nn_e)
                        m, _, _ = midpoint_rule(func, a_val, b_val, nn)
                        rows.append({'n': nn, 'Trapezoidal': t, "Simpson's": s, 'Midpoint': m})
                    df = pd.DataFrame(rows).set_index('n')
                    st.dataframe(df.style.format('{:.8f}'), use_container_width=True)
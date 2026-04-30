"""
lab1_root_finding.py - Lab 1: Root Finding Methods
====================================================
Implements:
  1. Bisection Method       -> bisection()
  2. Newton-Raphson Method  -> newton_raphson()
  3. Secant Method          -> secant()
  4. render_lab1()          -> Streamlit UI

UI v4.0 — CLEAN PREMIUM REDESIGN
─────────────────────────────────
• No emojis — clean SVG/CSS indicators only
• Algorithm cards: clean, readable, no visual noise
• Brighter, more energetic palette
• Plotly interactive graphs
• Smooth CSS animations (tasteful, not overdone)
• ALL LOGIC 100% UNTOUCHED
"""

import numpy as np
import sympy as sp
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.helpers import parse_function, display_iteration_table, show_function_guide


# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — CLEAN PREMIUM THEME
# ══════════════════════════════════════════════════════════════════════════════
GLOBAL_CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@600;700;800;900&display=swap');

/* ─── ROOT PALETTE ────────────────────────────────────────── */
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

/* ─── ANIMATIONS ─────────────────────────────────────────── */
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
@keyframes barGrow {
    from { width: 0; }
    to   { width: 100%; }
}
@keyframes dotPulse {
    0%, 100% { box-shadow: 0 0 0 0 currentColor; }
    50% { box-shadow: 0 0 0 5px transparent; }
}

/* ─── RESETS ─────────────────────────────────────────────── */
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
        radial-gradient(ellipse 60% 50% at 10% 20%, rgba(34,211,238,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 50% 60% at 90% 80%, rgba(167,139,250,0.05) 0%, transparent 60%),
        linear-gradient(180deg, rgba(14,20,40,0.8) 0%, rgba(7,9,15,0.9) 100%);
    border: 1px solid rgba(34,211,238,0.08);
}
/* decorative line across top */
.hero-section::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent 5%, var(--cyan) 30%, var(--violet) 70%, transparent 95%);
    opacity: 0.5;
}

.hero-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--cyan);
    display: flex; align-items: center; gap: 0.6rem;
    margin-bottom: 0.75rem;
    animation: fadeUp 0.5s ease-out 0.1s both;
}
.hero-label-bar {
    width: 24px; height: 2px;
    background: var(--cyan);
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
    background: linear-gradient(135deg, var(--cyan) 0%, var(--violet) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-desc {
    color: var(--text-2);
    font-size: 0.92rem;
    line-height: 1.7;
    margin: 0 0 1.3rem;
    max-width: 600px;
    animation: fadeUp 0.5s ease-out 0.3s both;
}
.hero-desc code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: var(--cyan);
    background: var(--cyan-dim);
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
.htag-c { background: var(--cyan-dim);    color: var(--cyan);    border: 1px solid rgba(34,211,238,0.2); }
.htag-v { background: var(--violet-dim);  color: var(--violet);  border: 1px solid rgba(167,139,250,0.2); }
.htag-e { background: var(--emerald-dim); color: var(--emerald); border: 1px solid rgba(52,211,153,0.2); }
.htag-c:hover { box-shadow: 0 4px 16px rgba(34,211,238,0.15); }
.htag-v:hover { box-shadow: 0 4px 16px rgba(167,139,250,0.15); }
.htag-e:hover { box-shadow: 0 4px 16px rgba(52,211,153,0.15); }

/* ─── ALGORITHM CARD — COMPLETELY CLEAN ─────────────────── */
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
/* clean top accent bar */
.algo-box-bar {
    position: absolute;
    top: 0; left: 1.2rem; right: 1.2rem;
    height: 2px;
    border-radius: 0 0 2px 2px;
    background: var(--accent, var(--cyan));
    opacity: 0.5;
}
.algo-box-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--accent, var(--cyan));
    margin-bottom: 1rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.algo-box-label::before {
    content: '';
    width: 5px; height: 5px;
    border-radius: 50%;
    background: var(--accent, var(--cyan));
    display: inline-block;
    animation: dotPulse 2s ease-in-out infinite;
    color: var(--accent, var(--cyan));
}
.algo-steps {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.73rem;
    color: var(--text-2);
    line-height: 2.2;
    margin-bottom: 1rem;
}
.algo-steps .step-num {
    color: var(--text-3);
    font-size: 0.65rem;
    margin-right: 0.3rem;
}
.algo-steps .step-hl {
    color: var(--text-1);
    font-weight: 600;
}
.algo-props {
    display: flex; flex-direction: column; gap: 0.4rem;
}
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
.prop-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    flex-shrink: 0;
}
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

/* ─── SECONDARY BUTTONS ──────────────────────────────────── */
div[data-testid="stButton"] > button[kind="secondary"] {
    background: var(--bg-2) !important;
    border: 1px solid rgba(34,211,238,0.12) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-2) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
    padding: 0.32rem 0.6rem !important;
    transition: all 0.25s ease !important;
}
div[data-testid="stButton"] > button[kind="secondary"]:hover {
    background: var(--cyan-dim) !important;
    border-color: rgba(34,211,238,0.35) !important;
    color: var(--cyan) !important;
    transform: translateY(-1px) !important;
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

/* ─── METRIC CARDS — CLEAN GLASS ─────────────────────────── */
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
    background: var(--m-accent, var(--cyan));
    opacity: 0.4;
}
.m-card-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 0.6rem;
    font-size: 0.85rem;
    font-weight: 800;
    color: var(--m-accent, var(--cyan));
    background: var(--m-bg, var(--cyan-dim));
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
.res-fail {
    background: linear-gradient(135deg, rgba(251,113,133,0.08), rgba(251,113,133,0.02));
    border: 1px solid rgba(251,113,133,0.25);
}
.res-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
    animation: softPulse 2s ease-in-out infinite;
}
.res-ok .res-dot  { background: var(--emerald); box-shadow: 0 0 10px var(--emerald); }
.res-fail .res-dot { background: var(--rose); box-shadow: 0 0 10px var(--rose); }
.res-msg {
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--text-1);
}

/* ─── GRAPH WRAPPER ──────────────────────────────────────── */
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

/* ─── MISC ───────────────────────────────────────────────── */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(34,211,238,0.12), rgba(167,139,250,0.12), transparent) !important;
    margin: 1.8rem 0 !important;
}
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
.ex-lbl {
    font-family: 'Inter', sans-serif;
    font-size: 0.68rem;
    color: var(--text-3);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 0.35rem;
    margin-top: 0.2rem;
}
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
</style>
"""


# ── Particle Background ──────────────────────────────────────────────────────
PARTICLE_HTML = """
<canvas id="pCanvas" style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:0;"></canvas>
<script>
(function(){
    var c=document.getElementById('pCanvas');if(!c)return;
    var ctx=c.getContext('2d'),w,h,pts=[];
    function rs(){w=c.width=window.innerWidth;h=c.height=window.innerHeight;}
    rs();window.addEventListener('resize',rs);
    var cols=['#22d3ee','#a78bfa','#34d399','#fbbf24'];
    for(var i=0;i<45;i++){
        pts.push({x:Math.random()*w,y:Math.random()*h,
            vx:(Math.random()-0.5)*0.25,vy:(Math.random()-0.5)*0.25,
            r:Math.random()*1.2+0.4,c:cols[Math.floor(Math.random()*4)]});
    }
    function draw(){
        ctx.clearRect(0,0,w,h);
        for(var i=0;i<pts.length;i++){
            var p=pts[i]; p.x+=p.vx; p.y+=p.vy;
            if(p.x<0)p.x=w;if(p.x>w)p.x=0;if(p.y<0)p.y=h;if(p.y>h)p.y=0;
            ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,6.28);
            ctx.fillStyle=p.c;ctx.globalAlpha=0.35;ctx.fill();
            for(var j=i+1;j<pts.length;j++){
                var dx=pts[j].x-p.x,dy=pts[j].y-p.y,d=Math.sqrt(dx*dx+dy*dy);
                if(d<110){ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(pts[j].x,pts[j].y);
                    ctx.strokeStyle=p.c;ctx.globalAlpha=0.04*(1-d/110);ctx.lineWidth=0.5;ctx.stroke();}
            }
        }
        ctx.globalAlpha=1;requestAnimationFrame(draw);
    }
    draw();
})();
</script>
"""


# ══════════════════════════════════════════════════════════════════════════════
# PLOTLY INTERACTIVE CHARTS
# ══════════════════════════════════════════════════════════════════════════════

def plot_root_interactive(func, root, a, b, method_name, iterations, accent='#22d3ee'):
    """Interactive dual-panel Plotly chart: function curve + convergence."""

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(
            f'<b style="font-family:Inter">{method_name}</b>  ·  Function Curve',
            '<b style="font-family:Inter">Convergence</b>  ·  Error Trace'
        ),
        horizontal_spacing=0.1,
        column_widths=[0.55, 0.45]
    )

    # ── LEFT: function curve ──────────────────────────────────────────────────
    margin = max(abs(b - a) * 0.45, 0.5)
    x_min, x_max = min(a, b) - margin, max(a, b) + margin
    x_range = np.linspace(x_min, x_max, 800)

    try:
        y_range = np.vectorize(func)(x_range)
        y_fin = y_range[np.isfinite(y_range)]
        if len(y_fin) > 0:
            clip = np.nanmedian(np.abs(y_fin)) * 8 or 10
            y_range = np.clip(y_range, -clip, clip)
    except Exception:
        y_range = np.zeros_like(x_range)

    # Positive / negative fills
    fig.add_trace(go.Scatter(
        x=x_range, y=np.where(y_range >= 0, y_range, 0),
        fill='tozeroy', fillcolor='rgba(34,211,238,0.05)',
        line=dict(width=0), showlegend=False, hoverinfo='skip'
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=x_range, y=np.where(y_range < 0, y_range, 0),
        fill='tozeroy', fillcolor='rgba(167,139,250,0.05)',
        line=dict(width=0), showlegend=False, hoverinfo='skip'
    ), row=1, col=1)

    # Glow line
    fig.add_trace(go.Scatter(
        x=x_range, y=y_range, mode='lines',
        line=dict(color=accent, width=6), opacity=0.12,
        showlegend=False, hoverinfo='skip'
    ), row=1, col=1)

    # Sharp line
    fig.add_trace(go.Scatter(
        x=x_range, y=y_range, mode='lines', name='f(x)',
        line=dict(color=accent, width=2.5, shape='spline'),
        hovertemplate='<b>x</b> = %{x:.4f}<br><b>f(x)</b> = %{y:.6f}<extra></extra>'
    ), row=1, col=1)

    # Interval band
    fig.add_vrect(
        x0=min(a, b), x1=max(a, b),
        fillcolor='rgba(167,139,250,0.04)',
        line=dict(color='rgba(167,139,250,0.2)', width=1, dash='dot'),
        layer='below', row=1, col=1
    )

    # Interval labels
    for pt, lbl, clr in [(min(a, b), 'a', '#a78bfa'), (max(a, b), 'b', '#c4b5fd')]:
        fig.add_vline(x=pt, line=dict(color=clr, width=1, dash='dot'), row=1, col=1)
        fig.add_annotation(
            x=pt, y=0, text=f'<b>{lbl}</b>', showarrow=False,
            font=dict(color=clr, size=13, family='Inter'), yshift=-22, row=1, col=1
        )

    fig.add_hline(y=0, line=dict(color='#1e293b', width=1.2), row=1, col=1)

    # Root marker
    if root is not None:
        try:
            yr = func(root)
            for sz, op in [(30, 0.08), (20, 0.18)]:
                fig.add_trace(go.Scatter(
                    x=[root], y=[yr], mode='markers',
                    marker=dict(size=sz, color=f'rgba(251,191,36,{op})'),
                    showlegend=False, hoverinfo='skip'
                ), row=1, col=1)
            fig.add_trace(go.Scatter(
                x=[root], y=[yr], mode='markers+text',
                name=f'Root = {root:.6f}',
                marker=dict(size=11, color='#fbbf24', symbol='diamond',
                           line=dict(width=2, color='#fef3c7')),
                text=[f'  {root:.6f}'], textposition='top right',
                textfont=dict(color='#fde68a', size=11, family='JetBrains Mono'),
                hovertemplate=f'<b>Root</b><br>x = {root:.8f}<br>f(x) = {yr:.2e}<extra></extra>'
            ), row=1, col=1)
            fig.add_vline(x=root, line=dict(color='#fbbf24', width=1.3, dash='dash'), opacity=0.4, row=1, col=1)
        except Exception:
            pass

    # ── RIGHT: convergence ────────────────────────────────────────────────────
    if iterations:
        errors = [max(it['Error'], 1e-16) for it in iterations]
        idxs = list(range(1, len(iterations) + 1))

        fig.add_trace(go.Scatter(
            x=idxs, y=errors, fill='tozeroy', fillcolor='rgba(167,139,250,0.06)',
            line=dict(width=0), showlegend=False, hoverinfo='skip'
        ), row=1, col=2)
        fig.add_trace(go.Scatter(
            x=idxs, y=errors, mode='lines',
            line=dict(color='#a78bfa', width=5), opacity=0.12,
            showlegend=False, hoverinfo='skip'
        ), row=1, col=2)
        fig.add_trace(go.Scatter(
            x=idxs, y=errors, mode='lines+markers', name='Error',
            line=dict(color='#c4b5fd', width=2.5, shape='spline'),
            marker=dict(size=7, color='#fbbf24', line=dict(width=1.2, color='#fef3c7')),
            hovertemplate='<b>Iteration %{x}</b><br>Error: %{y:.3e}<extra></extra>'
        ), row=1, col=2)

        # Converged point
        fig.add_trace(go.Scatter(
            x=[idxs[-1]], y=[errors[-1]], mode='markers',
            marker=dict(size=24, color='rgba(52,211,153,0.12)'),
            showlegend=False, hoverinfo='skip'
        ), row=1, col=2)
        fig.add_trace(go.Scatter(
            x=[idxs[-1]], y=[errors[-1]], mode='markers',
            name=f'Final: {errors[-1]:.2e}',
            marker=dict(size=10, color='#34d399', symbol='star',
                       line=dict(width=1.5, color='#a7f3d0')),
            hovertemplate=f'<b>Converged</b><br>Error: {errors[-1]:.2e}<extra></extra>'
        ), row=1, col=2)

        fig.add_hline(
            y=errors[-1], line=dict(color='#34d399', width=1, dash='dash'),
            annotation_text=f'final {errors[-1]:.1e}',
            annotation_font=dict(color='#34d399', size=10, family='JetBrains Mono'),
            annotation_position='top left', row=1, col=2
        )
        fig.update_yaxes(type='log', row=1, col=2)

    # ── Layout ────────────────────────────────────────────────────────────────
    ax = dict(
        gridcolor='rgba(30,41,59,0.5)', gridwidth=0.5,
        zerolinecolor='#1e293b', zerolinewidth=1,
        linecolor='#1e293b', linewidth=0.6,
        tickfont=dict(size=10, color='#4b5574', family='JetBrains Mono'),
        title_font=dict(size=11, color='#64748b', family='Inter'),
    )

    fig.update_layout(
        height=500, plot_bgcolor='#0c1021', paper_bgcolor='#07090f',
        font=dict(family='Inter', color='#8b95b0', size=12),
        legend=dict(
            bgcolor='rgba(12,16,33,0.9)', bordercolor='rgba(34,211,238,0.1)', borderwidth=1,
            font=dict(size=10.5, color='#e8ecf4', family='Inter'),
            orientation='h', yanchor='bottom', y=-0.22, xanchor='center', x=0.5,
        ),
        margin=dict(l=55, r=25, t=55, b=75),
        hoverlabel=dict(
            bgcolor='rgba(12,16,33,0.95)', bordercolor='rgba(34,211,238,0.2)',
            font=dict(family='JetBrains Mono', size=12, color='#e8ecf4')
        ),
    )

    fig.update_xaxes(title_text='x', **ax, row=1, col=1)
    fig.update_yaxes(title_text='f(x)', **ax, row=1, col=1)
    fig.update_xaxes(title_text='Iteration', **ax, row=1, col=2)
    fig.update_yaxes(title_text='Error (log)', **ax, row=1, col=2)

    for ann in fig.layout.annotations:
        ann.font = dict(size=12, color='#e8ecf4', family='Inter')

    return fig


# ─────────────────────────────────────────────
# METHOD 1: BISECTION (UNTOUCHED)
# ─────────────────────────────────────────────
def bisection(func, a: float, b: float, tol: float = 1e-6, max_iter: int = 100):
    f_a = func(a)
    f_b = func(b)
    if f_a * f_b >= 0:
        return None, [], (
            "f(a) and f(b) must have opposite signs (Bolzano's Theorem). "
            f"f({a}) = {f_a:.4f}, f({b}) = {f_b:.4f} — both have same sign."
        )
    iterations = []
    message = "Maximum iterations reached without convergence."
    c = a
    for i in range(max_iter):
        c = (a + b) / 2
        f_c = func(c)
        error = abs(b - a) / 2
        iterations.append({
            'a': round(a, 8), 'b': round(b, 8),
            'c (midpoint)': round(c, 8), 'f(c)': round(f_c, 8), 'Error': round(error, 8),
        })
        if abs(f_c) < tol or error < tol:
            message = f"Root found — converged in {i+1} iterations."
            break
        if f_a * f_c < 0:
            b = c; f_b = f_c
        else:
            a = c; f_a = f_c
    return c, iterations, message


# ─────────────────────────────────────────────
# METHOD 2: NEWTON-RAPHSON (UNTOUCHED)
# ─────────────────────────────────────────────
def newton_raphson(func, func_derivative, x0: float, tol: float = 1e-6, max_iter: int = 100):
    iterations = []
    message = "Maximum iterations reached without convergence."
    x1 = x0
    for i in range(max_iter):
        f_val = func(x0)
        f_prime = func_derivative(x0)
        if abs(f_prime) < 1e-14:
            return None, iterations, "Derivative became zero — division by zero. Change initial guess."
        x1 = x0 - f_val / f_prime
        error = abs(x1 - x0)
        iterations.append({
            'x₀': round(x0, 8), 'f(x₀)': round(f_val, 8),
            "f'(x₀)": round(f_prime, 8), 'x₁': round(x1, 8), 'Error': round(error, 8),
        })
        if error < tol:
            message = f"Root found — converged in {i+1} iterations."
            break
        x0 = x1
    return x1, iterations, message


# ─────────────────────────────────────────────
# METHOD 3: SECANT (UNTOUCHED)
# ─────────────────────────────────────────────
def secant(func, x0: float, x1: float, tol: float = 1e-6, max_iter: int = 100):
    iterations = []
    message = "Maximum iterations reached without convergence."
    x2 = x1
    f0 = func(x0)
    f1 = func(x1)
    for i in range(max_iter):
        denom = f1 - f0
        if abs(denom) < 1e-14:
            return None, iterations, "f(x1) - f(x0) = 0, division by zero. Change initial guesses."
        x2 = x1 - f1 * (x1 - x0) / denom
        error = abs(x2 - x1)
        f2 = func(x2)
        iterations.append({
            'x₀': round(x0, 8), 'x₁': round(x1, 8),
            'x₂': round(x2, 8), 'f(x₂)': round(f2, 8), 'Error': round(error, 8),
        })
        if error < tol:
            message = f"Root found — converged in {i+1} iterations."
            break
        x0, x1 = x1, x2
        f0, f1 = f1, f2
    return x2, iterations, message


# ─────────────────────────────────────────────
# RESULTS DISPLAY
# ─────────────────────────────────────────────
def _show_results(root, iters, msg, func, a_plot, b_plot, method_name, accent='#22d3ee'):
    """Premium results: banner + metric cards + interactive chart + table."""

    is_ok = root is not None

    # Banner
    cls = 'res-ok' if is_ok else 'res-fail'
    st.markdown(f"""
    <div class="res-banner {cls}">
        <span class="res-dot"></span>
        <span class="res-msg">{msg}</span>
    </div>
    """, unsafe_allow_html=True)

    if not is_ok:
        return

    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

    # Metric cards
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="m-card" style="--m-accent: var(--amber); animation-delay:.1s;">
            <div class="m-card-bar" style="background:var(--amber);"></div>
            <div class="m-card-icon" style="--m-accent:var(--amber); --m-bg:var(--amber-dim);">x*</div>
            <div class="m-card-val">{root:.8f}</div>
            <div class="m-card-lbl">Root Found</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="m-card" style="--m-accent: var(--cyan); animation-delay:.2s;">
            <div class="m-card-bar" style="background:var(--cyan);"></div>
            <div class="m-card-icon" style="--m-accent:var(--cyan); --m-bg:var(--cyan-dim);">n</div>
            <div class="m-card-val">{len(iters)}</div>
            <div class="m-card-lbl">Iterations</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        fe = f"{iters[-1]['Error']:.2e}" if iters else "N/A"
        st.markdown(f"""
        <div class="m-card" style="--m-accent: var(--emerald); animation-delay:.3s;">
            <div class="m-card-bar" style="background:var(--emerald);"></div>
            <div class="m-card-icon" style="--m-accent:var(--emerald); --m-bg:var(--emerald-dim);">e</div>
            <div class="m-card-val">{fe}</div>
            <div class="m-card-lbl">Final Error</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        try:
            fv = f"{abs(func(root)):.2e}"
        except:
            fv = "N/A"
        st.markdown(f"""
        <div class="m-card" style="--m-accent: var(--violet); animation-delay:.4s;">
            <div class="m-card-bar" style="background:var(--violet);"></div>
            <div class="m-card-icon" style="--m-accent:var(--violet); --m-bg:var(--violet-dim);">|f|</div>
            <div class="m-card-val">{fv}</div>
            <div class="m-card-lbl">|f(root)|</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

    # Chart
    st.markdown("""<div class="sec-title"><span class="sec-title-bar"></span>Interactive Visualization</div>""",
                unsafe_allow_html=True)

    fig = plot_root_interactive(func, root, a_plot, b_plot, method_name, iters, accent)
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
        Complete · {method_name} · {len(iters)} iterations · hover chart to explore data
    </div>
    """, unsafe_allow_html=True)

    # Table
    with st.expander("Iteration Table — click to expand", expanded=False):
        display_iteration_table(iters)


# ─────────────────────────────────────────────
# MAIN RENDERER
# ─────────────────────────────────────────────
def render_lab1():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.components.v1.html(PARTICLE_HTML, height=0, scrolling=False)

    # Hero
    st.markdown("""
    <div class="hero-section">
        <div class="hero-label"><span class="hero-label-bar"></span>Lab 01 · Numerical Methods</div>
        <div class="hero-heading">Root Finding <span>Methods</span></div>
        <p class="hero-desc">
            Solve nonlinear equations <code>f(x) = 0</code> with three classical numerical
            methods. Fully interactive graphs — hover, zoom, pan to explore every iteration.
        </p>
        <div class="hero-tags">
            <span class="htag htag-c">Bisection · O(1/2ⁿ)</span>
            <span class="htag htag-v">Newton-Raphson · Quadratic</span>
            <span class="htag htag-e">Secant · ~1.618</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    show_function_guide()
    st.markdown("<hr>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Bisection", "Newton-Raphson", "Secant"])

    # ── TAB 1: BISECTION ─────────────────────────────────────────────────────
    with tab1:
        st.markdown("""
        <p class="method-sub" style="--accent: var(--cyan);">
            Interval halving — guaranteed convergence when a sign change exists in [a, b].
            The most robust root-finding method.
        </p>
        """, unsafe_allow_html=True)

        ci, ca = st.columns([1.35, 1], gap="large")

        with ci:
            func_str_b = st.text_input("f(x) =", value="x**3 - x - 2", key="b_func",
                placeholder="e.g. 3x - e^x  or  sin(x) - 0.5")
            st.markdown("<div class='ex-lbl'>Quick examples</div>", unsafe_allow_html=True)
            ec = st.columns(4)
            for i, (c, e) in enumerate(zip(ec, ["x**3 - x - 2", "3*x - exp(x)", "sin(x) - 0.5", "x*exp(x) - 1"])):
                if c.button(e, key=f"be{i}", use_container_width=True):
                    st.session_state["b_func"] = e; st.rerun()
            st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
            r1, r2 = st.columns(2)
            a_b = r1.number_input("Left bound  a", value=1.0, step=0.5, key="b_a")
            b_b = r2.number_input("Right bound  b", value=2.0, step=0.5, key="b_b")
            r3, r4 = st.columns(2)
            tol_b = r3.number_input("Tolerance", value=1e-6, format="%.2e", key="b_tol")
            mi_b = r4.number_input("Max Iterations", value=50, min_value=1, max_value=500, key="b_mi")

        with ca:
            st.markdown("""
            <div class="algo-box" style="--accent: var(--cyan);">
                <div class="algo-box-bar" style="background: var(--cyan);"></div>
                <div class="algo-box-label">Bisection Algorithm</div>
                <div class="algo-steps">
                    <span class="step-num">01</span> <span class="step-hl">c = (a + b) / 2</span><br>
                    <span class="step-num">02</span> if f(a) · f(c) &lt; 0 then <span class="step-hl">b = c</span><br>
                    <span class="step-num">03</span> else <span class="step-hl">a = c</span><br>
                    <span class="step-num">04</span> repeat until <span class="step-hl">|b − a| &lt; tol</span>
                </div>
                <div class="algo-props">
                    <div class="algo-prop prop-amber"><span class="prop-dot"></span>Linear convergence O(1/2ⁿ)</div>
                    <div class="algo-prop prop-green"><span class="prop-dot"></span>Always converges if sign change exists</div>
                    <div class="algo-prop prop-violet"><span class="prop-dot"></span>Requires: f(a)·f(b) &lt; 0</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
        if st.button("Run Bisection", key="run_b", use_container_width=True, type="primary"):
            func, err = parse_function(func_str_b)
            if not err:
                with st.spinner("Computing..."):
                    root, iters, msg = bisection(func, a_b, b_b, tol_b, int(mi_b))
                _show_results(root, iters, msg, func, a_b, b_b, "Bisection", '#22d3ee')

    # ── TAB 2: NEWTON-RAPHSON ─────────────────────────────────────────────────
    with tab2:
        st.markdown("""
        <p class="method-sub" style="--accent: var(--violet);">
            Tangent-line method with quadratic convergence. Derivative is auto-computed
            via SymPy symbolic differentiation.
        </p>
        """, unsafe_allow_html=True)

        ci, ca = st.columns([1.35, 1], gap="large")

        with ci:
            func_str_n = st.text_input("f(x) =", value="x**3 - x - 2", key="n_func",
                placeholder="e.g. cos(x) - x  or  exp(x) - 3*x")
            st.markdown("<div class='ex-lbl'>Quick examples</div>", unsafe_allow_html=True)
            ec = st.columns(4)
            for i, (c, e) in enumerate(zip(ec, ["x**3 - x - 2", "cos(x) - x", "exp(x) - 3*x", "x**2 - 2"])):
                if c.button(e, key=f"ne{i}", use_container_width=True):
                    st.session_state["n_func"] = e; st.rerun()
            st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
            x0_n = st.number_input("Initial guess  x₀", value=1.5, step=0.5, key="n_x0")
            r3, r4 = st.columns(2)
            tol_n = r3.number_input("Tolerance", value=1e-6, format="%.2e", key="n_tol")
            mi_n = r4.number_input("Max Iterations", value=50, min_value=1, key="n_mi")

        with ca:
            st.markdown("""
            <div class="algo-box" style="--accent: var(--violet);">
                <div class="algo-box-bar" style="background: var(--violet);"></div>
                <div class="algo-box-label" style="color: var(--violet);">Newton-Raphson Algorithm</div>
                <div class="algo-steps">
                    <span class="step-num">01</span> <span class="step-hl">x₁ = x₀ − f(x₀) / f'(x₀)</span><br>
                    <span class="step-num">02</span> repeat until <span class="step-hl">|x₁ − x₀| &lt; tol</span>
                </div>
                <div class="algo-props">
                    <div class="algo-prop prop-amber"><span class="prop-dot"></span>Quadratic convergence — very fast</div>
                    <div class="algo-prop prop-green"><span class="prop-dot"></span>Typically 4-7 iterations</div>
                    <div class="algo-prop prop-violet"><span class="prop-dot"></span>f'(x) auto-derived via SymPy</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
        if st.button("Run Newton-Raphson", key="run_n", use_container_width=True, type="primary"):
            func, err = parse_function(func_str_n)
            if not err:
                try:
                    x_sym = sp.Symbol('x')
                    from sympy.parsing.sympy_parser import (
                        parse_expr, standard_transformations,
                        implicit_multiplication_application, convert_xor
                    )
                    transformations = (standard_transformations +
                                       (implicit_multiplication_application, convert_xor))
                    expr = parse_expr(func_str_n,
                                      local_dict={'x': x_sym, 'e': sp.E, 'pi': sp.pi},
                                      transformations=transformations)
                    deriv = sp.diff(expr, x_sym)
                    func_d = sp.lambdify(x_sym, deriv, modules=['numpy'])
                    st.markdown(f"""
                    <div class="status-row">
                        <span class="s-dot" style="background:var(--violet);box-shadow:0 0 6px var(--violet);"></span>
                        Auto-derived:&nbsp; <code style="color:var(--violet);background:var(--violet-dim);
                        padding:.12rem .45rem;border-radius:5px;font-family:'JetBrains Mono',monospace;
                        font-size:.78rem;">f'(x) = {sp.simplify(deriv)}</code>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as ex:
                    st.error(f"Could not compute derivative: {ex}")
                    st.stop()
                with st.spinner("Computing..."):
                    root, iters, msg = newton_raphson(func, func_d, x0_n, tol_n, int(mi_n))
                _show_results(root, iters, msg, func, x0_n - 3, x0_n + 3, "Newton-Raphson", '#a78bfa')

    # ── TAB 3: SECANT ─────────────────────────────────────────────────────────
    with tab3:
        st.markdown("""
        <p class="method-sub" style="--accent: var(--emerald);">
            Derivative-free method with superlinear convergence (~1.618). Uses secant-line
            approximation instead of tangent — no f'(x) needed.
        </p>
        """, unsafe_allow_html=True)

        ci, ca = st.columns([1.35, 1], gap="large")

        with ci:
            func_str_s = st.text_input("f(x) =", value="x**3 - x - 2", key="s_func",
                placeholder="e.g. x*log(x) - 1  or  exp(x) - 2")
            st.markdown("<div class='ex-lbl'>Quick examples</div>", unsafe_allow_html=True)
            ec = st.columns(4)
            for i, (c, e) in enumerate(zip(ec, ["x**3 - x - 2", "x*log(x) - 1", "exp(x) - 2", "sin(x) - x/2"])):
                if c.button(e, key=f"se{i}", use_container_width=True):
                    st.session_state["s_func"] = e; st.rerun()
            st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
            r1, r2 = st.columns(2)
            x0_s = r1.number_input("First guess  x₀", value=1.0, step=0.5, key="s_x0")
            x1_s = r2.number_input("Second guess  x₁", value=2.0, step=0.5, key="s_x1")
            r3, r4 = st.columns(2)
            tol_s = r3.number_input("Tolerance", value=1e-6, format="%.2e", key="s_tol")
            mi_s = r4.number_input("Max Iterations", value=50, min_value=1, key="s_mi")

        with ca:
            st.markdown("""
            <div class="algo-box" style="--accent: var(--emerald);">
                <div class="algo-box-bar" style="background: var(--emerald);"></div>
                <div class="algo-box-label" style="color: var(--emerald);">Secant Algorithm</div>
                <div class="algo-steps">
                    <span class="step-num">01</span> <span class="step-hl">x₂ = x₁ − f(x₁)·(x₁ − x₀) / (f(x₁) − f(x₀))</span><br>
                    <span class="step-num">02</span> repeat until <span class="step-hl">|x₂ − x₁| &lt; tol</span>
                </div>
                <div class="algo-props">
                    <div class="algo-prop prop-amber"><span class="prop-dot"></span>Superlinear convergence ~1.618</div>
                    <div class="algo-prop prop-green"><span class="prop-dot"></span>No derivative computation needed</div>
                    <div class="algo-prop prop-violet"><span class="prop-dot"></span>Requires two initial guesses</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
        if st.button("Run Secant", key="run_s", use_container_width=True, type="primary"):
            func, err = parse_function(func_str_s)
            if not err:
                if abs(x0_s - x1_s) < 1e-14:
                    st.error("Initial guesses x₀ and x₁ must be different!")
                else:
                    with st.spinner("Computing..."):
                        root, iters, msg = secant(func, x0_s, x1_s, tol_s, int(mi_s))
                    _show_results(root, iters, msg, func, min(x0_s, x1_s) - 1.5,
                                  max(x0_s, x1_s) + 1.5, "Secant", '#34d399')


if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    f = lambda x: x**3 - x - 2
    root, logs, msg = bisection(f, 1, 2)
    print(msg, "| Root:", root)
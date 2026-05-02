"""
lab2_interpolation.py - Lab 2: Interpolation Methods
======================================================
Methods:
  1. Lagrange Interpolation         -> lagrange_interpolation()
  2. Newton Forward Difference       -> newton_forward_difference()
  3. Newton Divided Difference       -> newton_divided_difference()

Main UI function:
  render_lab2()

UI v4.0 — PREMIUM REDESIGN (matches Lab 1 style)
─────────────────────────────────────────────────
• Hero section with animated tags
• Algo cards per method with step-by-step breakdown
• Metric result cards (same as Lab 1)
• Full step-by-step working shown after calculation
• Premium styled tables (difference tables, Li tables)
• Plotly interactive interpolation graph
• Particle background + full CSS theme
• ALL LOGIC VERIFIED AND CORRECT
"""

import numpy as np
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — MATCHES LAB 1 PREMIUM THEME EXACTLY
# ══════════════════════════════════════════════════════════════════════════════
LAB2_CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@600;700;800;900&display=swap');

/* ─── ROOT PALETTE ─────────────────────────────────────────── */
:root {
    --cyan:        #22d3ee;
    --cyan-dim:    rgba(34,211,238,0.12);
    --violet:      #a78bfa;
    --violet-dim:  rgba(167,139,250,0.12);
    --emerald:     #34d399;
    --emerald-dim: rgba(52,211,153,0.12);
    --amber:       #fbbf24;
    --amber-dim:   rgba(251,191,36,0.12);
    --rose:        #fb7185;
    --rose-dim:    rgba(251,113,133,0.12);
    --sky:         #38bdf8;

    --bg-0:     #07090f;
    --bg-1:     #0c1021;
    --bg-2:     #111730;
    --bg-card:  rgba(14,20,40,0.65);
    --bg-glass: rgba(18,26,52,0.50);

    --text-0: #ffffff;
    --text-1: #e8ecf4;
    --text-2: #8b95b0;
    --text-3: #4b5574;

    --border-1: rgba(34,211,238,0.10);
    --border-2: rgba(167,139,250,0.10);
    --radius:    16px;
    --radius-sm: 10px;
}

/* ─── ANIMATIONS ──────────────────────────────────────────── */
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
    50%       { background-position: 100% 50%; }
}
@keyframes softPulse {
    0%, 100% { opacity: 0.6; }
    50%       { opacity: 1; }
}
@keyframes dotPulse {
    0%, 100% { box-shadow: 0 0 0 0 currentColor; }
    50%       { box-shadow: 0 0 0 5px transparent; }
}

/* ─── RESETS ──────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif !important;
}
.stApp { background: var(--bg-0) !important; }

/* ─── HERO ────────────────────────────────────────────────── */
.hero-section {
    position: relative;
    padding: 2.6rem 2.8rem 2.2rem;
    margin-bottom: 2rem;
    border-radius: 24px;
    overflow: hidden;
    animation: fadeScale 0.7s ease-out;
    background:
        radial-gradient(ellipse 60% 50% at 10% 20%, rgba(167,139,250,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 50% 60% at 90% 80%, rgba(34,211,238,0.05) 0%, transparent 60%),
        linear-gradient(180deg, rgba(14,20,40,0.8) 0%, rgba(7,9,15,0.9) 100%);
    border: 1px solid rgba(167,139,250,0.08);
}
.hero-section::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent 5%, var(--violet) 30%, var(--cyan) 70%, transparent 95%);
    opacity: 0.5;
}
.hero-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--violet);
    display: flex; align-items: center; gap: 0.6rem;
    margin-bottom: 0.75rem;
    animation: fadeUp 0.5s ease-out 0.1s both;
}
.hero-label-bar {
    width: 24px; height: 2px;
    background: var(--violet);
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
    background: linear-gradient(135deg, var(--violet) 0%, var(--cyan) 100%);
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
    color: var(--violet);
    background: var(--violet-dim);
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

/* ─── ALGO CARD ───────────────────────────────────────────── */
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
    border-color: var(--accent, var(--violet));
    box-shadow: 0 0 30px rgba(167,139,250,0.05);
}
.algo-box-bar {
    position: absolute;
    top: 0; left: 1.2rem; right: 1.2rem;
    height: 2px;
    border-radius: 0 0 2px 2px;
    background: var(--accent, var(--violet));
    opacity: 0.5;
}
.algo-box-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--accent, var(--violet));
    margin-bottom: 1rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.algo-box-label::before {
    content: '';
    width: 5px; height: 5px;
    border-radius: 50%;
    background: var(--accent, var(--violet));
    display: inline-block;
    animation: dotPulse 2s ease-in-out infinite;
    color: var(--accent, var(--violet));
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
.prop-amber  { background: var(--amber-dim);   color: var(--amber); }
.prop-green  { background: var(--emerald-dim); color: var(--emerald); }
.prop-violet { background: var(--violet-dim);  color: var(--violet); }
.prop-amber  .prop-dot { background: var(--amber); }
.prop-green  .prop-dot { background: var(--emerald); }
.prop-violet .prop-dot { background: var(--violet); }

/* ─── STEP CARD (step-by-step working) ───────────────────── */
.step-card {
    background: var(--bg-glass);
    border: 1px solid rgba(167,139,250,0.10);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.7rem;
    animation: fadeUp 0.4s ease-out both;
    position: relative;
    overflow: hidden;
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 10%; bottom: 10%;
    width: 2.5px;
    border-radius: 2px;
    background: var(--step-accent, var(--violet));
    opacity: 0.7;
}
.step-card-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--step-accent, var(--violet));
    margin-bottom: 0.45rem;
}
.step-card-body {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: var(--text-1);
    line-height: 1.85;
}
.step-card-body .hl { color: var(--amber); font-weight: 600; }
.step-card-body .dim { color: var(--text-3); }

/* ─── METRIC CARDS ────────────────────────────────────────── */
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
    border-color: var(--m-accent, var(--violet));
    box-shadow: 0 8px 28px rgba(0,0,0,0.25);
}
.m-card-bar {
    position: absolute;
    top: 0; left: 20%; right: 20%;
    height: 2px;
    border-radius: 0 0 4px 4px;
    background: var(--m-accent, var(--violet));
    opacity: 0.4;
}
.m-card-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    display: inline-flex;
    align-items: center; justify-content: center;
    margin-bottom: 0.6rem;
    font-size: 0.85rem;
    font-weight: 800;
    color: var(--m-accent, var(--violet));
    background: var(--m-bg, var(--violet-dim));
}
.m-card-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text-0);
    margin-bottom: 0.25rem;
    letter-spacing: -0.01em;
    word-break: break-all;
}
.m-card-lbl {
    font-family: 'Inter', sans-serif;
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-3);
}

/* ─── RESULT BANNER ───────────────────────────────────────── */
.res-banner {
    border-radius: 14px;
    padding: 1rem 1.4rem;
    display: flex; align-items: center; gap: 0.9rem;
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
    border-radius: 50%; flex-shrink: 0;
    animation: softPulse 2s ease-in-out infinite;
}
.res-ok   .res-dot { background: var(--emerald); box-shadow: 0 0 10px var(--emerald); }
.res-fail .res-dot { background: var(--rose);    box-shadow: 0 0 10px var(--rose); }
.res-msg {
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem; font-weight: 500;
    color: var(--text-1);
}

/* ─── CHART WRAPPER ───────────────────────────────────────── */
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
    border-color: rgba(167,139,250,0.2);
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
}

/* ─── SECTION TITLE ───────────────────────────────────────── */
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
    background: linear-gradient(90deg, var(--violet), var(--cyan));
    display: inline-block;
}

/* ─── METHOD SUBTITLE ─────────────────────────────────────── */
.method-sub {
    font-size: 0.88rem;
    color: var(--text-2);
    font-weight: 400;
    margin-bottom: 1.3rem;
    padding-left: 0.9rem;
    border-left: 2.5px solid var(--accent, var(--violet));
    line-height: 1.65;
    animation: slideRight 0.4s ease-out;
}

/* ─── STATUS ROW ──────────────────────────────────────────── */
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

/* ─── RUN BUTTON ──────────────────────────────────────────── */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1, #a855f7, #22d3ee) !important;
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
    box-shadow: 0 4px 20px rgba(168,85,247,0.3) !important;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(168,85,247,0.45) !important;
    filter: brightness(1.08) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:active {
    transform: translateY(0) scale(0.98) !important;
}

/* ─── INPUTS ──────────────────────────────────────────────── */
div[data-testid="stTextInput"] > div > div > input,
div[data-testid="stNumberInput"] input {
    background: var(--bg-1) !important;
    border: 1.5px solid rgba(167,139,250,0.1) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-1) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stTextInput"] > div > div > input:focus,
div[data-testid="stNumberInput"] input:focus {
    border-color: rgba(167,139,250,0.4) !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.06) !important;
}

/* ─── SELECT BOX ──────────────────────────────────────────── */
div[data-testid="stSelectbox"] > div > div {
    background: var(--bg-1) !important;
    border: 1.5px solid rgba(167,139,250,0.1) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-1) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
}

/* ─── TABS ────────────────────────────────────────────────── */
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
    background: rgba(167,139,250,0.04) !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--violet) !important;
    background: rgba(167,139,250,0.08) !important;
    border-bottom: 2.5px solid var(--violet) !important;
}

/* ─── EXPANDER ────────────────────────────────────────────── */
div[data-testid="stExpander"] > details {
    background: rgba(12,16,33,0.6) !important;
    border: 1px solid rgba(167,139,250,0.07) !important;
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
    border: 1px solid rgba(167,139,250,0.07) !important;
}

/* ─── MISC ────────────────────────────────────────────────── */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(167,139,250,0.12), rgba(34,211,238,0.12), transparent) !important;
    margin: 1.8rem 0 !important;
}
</style>
"""

# ── Particle Background (same as Lab 1) ──────────────────────────────────────
PARTICLE_HTML = """
<canvas id="pCanvas2" style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:0;"></canvas>
<script>
(function(){
    var c=document.getElementById('pCanvas2');if(!c)return;
    var ctx=c.getContext('2d'),w,h,pts=[];
    function rs(){w=c.width=window.innerWidth;h=c.height=window.innerHeight;}
    rs();window.addEventListener('resize',rs);
    var cols=['#a78bfa','#22d3ee','#34d399','#fbbf24'];
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
# METHOD 1: LAGRANGE INTERPOLATION
# ══════════════════════════════════════════════════════════════════════════════
def lagrange_interpolation(x_points: list, y_points: list, x_query: float):
    """
    Lagrange Interpolation Formula:
        P(x) = sum_{i=0}^{n-1} y_i * L_i(x)
    where:
        L_i(x) = product_{j != i} (x - x_j) / (x_i - x_j)

    Returns:
        result  : float — interpolated value P(x_query)
        Li_list : list  — list of basis polynomial values L_i(x_query)
    """
    n = len(x_points)
    Li_list = []
    result = 0.0
    for i in range(n):
        Li = 1.0
        for j in range(n):
            if j != i:
                Li *= (x_query - x_points[j]) / (x_points[i] - x_points[j])
        Li_list.append(Li)
        result += y_points[i] * Li
    return result, Li_list


# ══════════════════════════════════════════════════════════════════════════════
# METHOD 2: NEWTON FORWARD DIFFERENCE
# ══════════════════════════════════════════════════════════════════════════════
def newton_forward_difference(x_points: list, y_points: list, x_query: float):
    """
    Newton Forward Difference Interpolation.
    Requires equally-spaced x points with step h.

    Formula:
        s = (x - x_0) / h
        P(x) = y_0 + s*Δy_0 + s(s-1)/2! * Δ²y_0 + ...

    Returns:
        result     : float       — interpolated value
        diff_table : list[list]  — full forward difference table
    """
    n = len(x_points)
    h = x_points[1] - x_points[0]

    # Validate equal spacing
    for k in range(1, n - 1):
        if abs((x_points[k + 1] - x_points[k]) - h) > 1e-9:
            raise ValueError(
                "Newton Forward Difference requires equally spaced x points. "
                f"Found unequal gap between x[{k}]={x_points[k]} and x[{k+1}]={x_points[k+1]}."
            )

    s = (x_query - x_points[0]) / h

    # Build forward difference table: diff_table[i][j] = j-th order difference starting at index i
    diff_table = [[0.0] * n for _ in range(n)]
    for i in range(n):
        diff_table[i][0] = y_points[i]
    for j in range(1, n):
        for i in range(n - j):
            diff_table[i][j] = diff_table[i + 1][j - 1] - diff_table[i][j - 1]

    # Apply Newton forward formula
    result = diff_table[0][0]
    s_term = 1.0
    for k in range(1, n):
        s_term *= (s - (k - 1)) / k
        result += s_term * diff_table[0][k]

    return result, diff_table, s, h


# ══════════════════════════════════════════════════════════════════════════════
# METHOD 3: NEWTON DIVIDED DIFFERENCE
# ══════════════════════════════════════════════════════════════════════════════
def newton_divided_difference(x_points: list, y_points: list, x_query: float):
    """
    Newton Divided Difference Interpolation.
    Works for both equally and unequally spaced x points.

    Formula:
        P(x) = f[x_0] + (x-x_0)*f[x_0,x_1] + (x-x_0)(x-x_1)*f[x_0,x_1,x_2] + ...

    Returns:
        result    : float       — interpolated value
        div_table : list[list]  — full divided difference table
    """
    n = len(x_points)
    div_table = [[0.0] * n for _ in range(n)]
    for i in range(n):
        div_table[i][0] = y_points[i]
    for j in range(1, n):
        for i in range(n - j):
            div_table[i][j] = (
                (div_table[i + 1][j - 1] - div_table[i][j - 1]) /
                (x_points[i + j] - x_points[i])
            )

    # Evaluate polynomial using Horner-like expansion
    result = div_table[0][0]
    prod = 1.0
    for k in range(1, n):
        prod *= (x_query - x_points[k - 1])
        result += div_table[0][k] * prod

    return result, div_table


# ══════════════════════════════════════════════════════════════════════════════
# PLOTTING
# ══════════════════════════════════════════════════════════════════════════════
def plot_interpolation(x_points, y_points, x_query, y_result, method_name):
    """Interactive Plotly interpolation curve — matches Lab 1 chart style."""
    x_min = min(x_points) - abs(max(x_points) - min(x_points)) * 0.3
    x_max = max(x_points) + abs(max(x_points) - min(x_points)) * 0.3
    x_fine = np.linspace(x_min, x_max, 400)

    # Always evaluate curve using Lagrange (exact for polynomial interpolation)
    y_fine = []
    for xv in x_fine:
        val, _ = lagrange_interpolation(list(x_points), list(y_points), float(xv))
        y_fine.append(val)

    fig = go.Figure()

    # Interpolation curve
    fig.add_trace(go.Scatter(
        x=x_fine, y=y_fine, mode='lines', name='P(x) — Interpolating Polynomial',
        line=dict(color='#a78bfa', width=2.5, shape='spline'),
        hovertemplate='x=%{x:.4f}<br>P(x)=%{y:.6f}<extra></extra>'
    ))

    # Data points
    fig.add_trace(go.Scatter(
        x=list(x_points), y=list(y_points), mode='markers',
        name='Known Data Points',
        marker=dict(size=11, color='#22d3ee', line=dict(width=2, color='#a5f3fc')),
        hovertemplate='x=%{x}<br>y=%{y}<extra></extra>'
    ))

    # Vertical dashed line at query point
    fig.add_vline(
        x=x_query,
        line=dict(color='rgba(251,191,36,0.3)', width=1.5, dash='dot'),
    )

    # Query result point
    fig.add_trace(go.Scatter(
        x=[x_query], y=[y_result], mode='markers+text',
        name=f'P({x_query:.4f}) = {y_result:.6f}',
        marker=dict(size=14, color='#fbbf24', symbol='diamond',
                    line=dict(width=2, color='#fef3c7')),
        text=[f'  P({x_query:.3f}) = {y_result:.4f}'],
        textposition='top right',
        textfont=dict(color='#fde68a', size=11, family='JetBrains Mono'),
        hovertemplate=f'Query Point<br>x={x_query:.6f}<br>P(x)={y_result:.8f}<extra></extra>'
    ))

    ax = dict(
        gridcolor='rgba(30,41,59,0.5)', gridwidth=0.5,
        zerolinecolor='#1e293b', zerolinewidth=1,
        linecolor='#1e293b', linewidth=0.6,
        tickfont=dict(size=10, color='#4b5574', family='JetBrains Mono'),
        title_font=dict(size=11, color='#64748b', family='Inter'),
    )

    fig.update_layout(
        title=dict(
            text=f'<b style="font-family:Inter">{method_name}</b>  ·  Interpolation Curve',
            font=dict(size=14, color='#e8ecf4', family='Inter'),
            x=0.02, xanchor='left'
        ),
        height=480,
        plot_bgcolor='#0c1021', paper_bgcolor='#07090f',
        font=dict(family='Inter', color='#8b95b0', size=12),
        legend=dict(
            bgcolor='rgba(12,16,33,0.9)', bordercolor='rgba(167,139,250,0.1)', borderwidth=1,
            font=dict(size=10.5, color='#e8ecf4', family='Inter'),
            orientation='h', yanchor='bottom', y=-0.22, xanchor='center', x=0.5,
        ),
        margin=dict(l=55, r=25, t=55, b=75),
        hoverlabel=dict(
            bgcolor='rgba(12,16,33,0.95)', bordercolor='rgba(167,139,250,0.2)',
            font=dict(family='JetBrains Mono', size=12, color='#e8ecf4')
        ),
    )
    fig.update_xaxes(title_text='x', **ax)
    fig.update_yaxes(title_text='P(x)', **ax)
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# STEP-BY-STEP DISPLAY HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def _step_card(header: str, body: str, accent: str = 'var(--violet)', delay_idx: int = 0):
    """Render a single step card with left accent bar."""
    st.markdown(f"""
    <div class="step-card" style="--step-accent: {accent}; animation-delay:{delay_idx * 0.07}s;">
        <div class="step-card-header">{header}</div>
        <div class="step-card-body">{body}</div>
    </div>
    """, unsafe_allow_html=True)


def _show_lagrange_steps(x_pts, y_pts, x_query, result, Li_list):
    """Show full Lagrange working step-by-step."""
    n = len(x_pts)

    st.markdown("""<div class="sec-title"><span class="sec-title-bar"></span>Step-by-Step Working</div>""",
                unsafe_allow_html=True)

    # Step 0: Given data
    data_str = "  ".join([f"({x_pts[i]}, {y_pts[i]})" for i in range(n)])
    _step_card("Step 0 — Given Data", f"n = {n} points &nbsp;|&nbsp; x_query = {x_query}<br>"
               + "  ".join([f'<span class="hl">(x_{i}, y_{i})</span> = ({x_pts[i]}, {y_pts[i]})' for i in range(n)]),
               accent='var(--cyan)', delay_idx=0)

    # Step 1: Formula reminder
    formula = "P(x) = "
    terms = " + ".join([f"y_{i} · L_{i}(x)" for i in range(n)])
    _step_card("Step 1 — Lagrange Formula",
               f"P(x) = Σ yᵢ · Lᵢ(x) &nbsp;where&nbsp; Lᵢ(x) = ∏ (x − xⱼ) / (xᵢ − xⱼ) &nbsp;[j ≠ i]",
               accent='var(--violet)', delay_idx=1)

    # Step 2+: Each L_i
    for i in range(n):
        numer_parts = []
        denom_parts = []
        for j in range(n):
            if j != i:
                numer_parts.append(f"({x_query} - {x_pts[j]})")
                denom_parts.append(f"({x_pts[i]} - {x_pts[j]})")

        numer_vals = []
        denom_vals = []
        for j in range(n):
            if j != i:
                numer_vals.append(round(x_query - x_pts[j], 8))
                denom_vals.append(round(x_pts[i] - x_pts[j], 8))

        numer_prod = 1.0
        denom_prod = 1.0
        for v in numer_vals:
            numer_prod *= v
        for v in denom_vals:
            denom_prod *= v

        body = (
            f'L_{i}(x) = [{" × ".join([str(v) for v in numer_parts])}] / '
            f'[{" × ".join([str(v) for v in denom_parts])}]<br>'
            f'<span class="dim">     = {round(numer_prod, 8)} / {round(denom_prod, 8)}</span><br>'
            f'<span class="hl">     = {round(Li_list[i], 8)}</span>'
        )
        _step_card(f"Step {i + 2} — Compute L_{i}(x)", body,
                   accent='var(--emerald)', delay_idx=i + 2)

    # Step final: Summation
    contrib_lines = "<br>".join([
        f'y_{i} · L_{i}(x) = {y_pts[i]} × {round(Li_list[i], 8)} = <span class="hl">{round(y_pts[i] * Li_list[i], 8)}</span>'
        for i in range(n)
    ])
    _step_card(
        f"Step {n + 2} — Compute P(x_query)",
        contrib_lines + f'<br><span class="dim">Sum = </span><span class="hl">{round(result, 8)}</span>',
        accent='var(--amber)', delay_idx=n + 2
    )


def _show_newton_forward_steps(x_pts, y_pts, x_query, result, diff_table, s, h):
    """Show full Newton Forward working step-by-step."""
    n = len(x_pts)

    st.markdown("""<div class="sec-title"><span class="sec-title-bar"></span>Step-by-Step Working</div>""",
                unsafe_allow_html=True)

    # Step 0: Given
    _step_card("Step 0 — Given Data",
               f'h = {round(h, 8)} &nbsp;|&nbsp; x_query = {x_query} &nbsp;|&nbsp; x_0 = {x_pts[0]}<br>'
               + "  ".join([f'<span class="hl">({x_pts[i]}, {y_pts[i]})</span>' for i in range(n)]),
               accent='var(--cyan)', delay_idx=0)

    # Step 1: Compute s
    _step_card("Step 1 — Compute s",
               f's = (x_query − x_0) / h<br>'
               f's = ({x_query} − {x_pts[0]}) / {round(h, 8)}<br>'
               f'<span class="hl">s = {round(s, 8)}</span>',
               accent='var(--violet)', delay_idx=1)

    # Step 2: Forward difference table shown in expander (done separately)
    _step_card("Step 2 — Build Forward Difference Table",
               f'Δ⁰y = y values as given<br>'
               f'Δᵏyᵢ = Δᵏ⁻¹yᵢ₊₁ − Δᵏ⁻¹yᵢ &nbsp; (subtract consecutive values each round)<br>'
               f'<span class="dim">See full table below.</span>',
               accent='var(--emerald)', delay_idx=2)

    # Step 3: Formula terms
    term_lines = []
    s_term = 1.0
    cumulative = diff_table[0][0]
    term_lines.append(
        f'Term 0: Δ⁰y₀ = <span class="hl">{round(diff_table[0][0], 8)}</span>'
    )
    for k in range(1, n):
        s_term_prev = s_term
        s_term *= (s - (k - 1)) / k
        term_val = s_term * diff_table[0][k]
        cumulative += term_val

        coeff_expr = " × ".join([f"(s − {j})" for j in range(k)]) + f" / {k}!"
        term_lines.append(
            f'Term {k}: [{coeff_expr}] × Δ^{k}y₀ '
            f'= {round(s_term, 8)} × {round(diff_table[0][k], 8)} '
            f'= <span class="hl">{round(term_val, 8)}</span>'
        )

    _step_card("Step 3 — Apply Newton Forward Formula",
               "P(x) = y₀ + s·Δy₀ + [s(s−1)/2!]·Δ²y₀ + ...<br><br>"
               + "<br>".join(term_lines),
               accent='var(--amber)', delay_idx=3)

    _step_card("Step 4 — Final Answer",
               f'P({x_query}) = Sum of all terms = <span class="hl">{round(result, 8)}</span>',
               accent='var(--cyan)', delay_idx=4)


def _show_newton_divided_steps(x_pts, y_pts, x_query, result, div_table):
    """Show full Newton Divided Difference working step-by-step."""
    n = len(x_pts)

    st.markdown("""<div class="sec-title"><span class="sec-title-bar"></span>Step-by-Step Working</div>""",
                unsafe_allow_html=True)

    # Step 0: Given
    _step_card("Step 0 — Given Data",
               "  ".join([f'<span class="hl">({x_pts[i]}, {y_pts[i]})</span>' for i in range(n)]),
               accent='var(--cyan)', delay_idx=0)

    # Step 1: Divided difference table explanation
    _step_card("Step 1 — Build Divided Difference Table",
               "f[xᵢ] = yᵢ &nbsp;(0th order = y values)<br>"
               "f[xᵢ, xⱼ] = (f[xⱼ] − f[xᵢ]) / (xⱼ − xᵢ) &nbsp;(1st order)<br>"
               "f[xᵢ,..,xₖ] = (f[xᵢ₊₁,..,xₖ] − f[xᵢ,..,xₖ₋₁]) / (xₖ − xᵢ) &nbsp;(higher orders)<br>"
               '<span class="dim">See full table below.</span>',
               accent='var(--violet)', delay_idx=1)

    # Step 2: Show coefficients extracted from top row
    coeffs = [div_table[0][k] for k in range(n)]
    coeff_lines = "<br>".join([
        f'c_{k} = f[x_0..x_{k}] = <span class="hl">{round(coeffs[k], 8)}</span>'
        for k in range(n)
    ])
    _step_card("Step 2 — Extract Polynomial Coefficients (top row of table)", coeff_lines,
               accent='var(--emerald)', delay_idx=2)

    # Step 3: Evaluate terms
    term_lines = []
    cumulative = coeffs[0]
    term_lines.append(f'Term 0: c_0 = <span class="hl">{round(coeffs[0], 8)}</span>')
    prod = 1.0
    for k in range(1, n):
        prod *= (x_query - x_pts[k - 1])
        term_val = coeffs[k] * prod
        cumulative += term_val
        prod_factors = " × ".join([f"({x_query} − {x_pts[j]})" for j in range(k)])
        term_lines.append(
            f'Term {k}: c_{k} × [{prod_factors}] '
            f'= {round(coeffs[k], 8)} × {round(prod, 8)} '
            f'= <span class="hl">{round(term_val, 8)}</span>'
        )
    _step_card("Step 3 — Evaluate P(x_query) Term by Term",
               "P(x) = c₀ + c₁(x−x₀) + c₂(x−x₀)(x−x₁) + ...<br><br>"
               + "<br>".join(term_lines),
               accent='var(--amber)', delay_idx=3)

    _step_card("Step 4 — Final Answer",
               f'P({x_query}) = Sum of all terms = <span class="hl">{round(result, 8)}</span>',
               accent='var(--cyan)', delay_idx=4)


# ══════════════════════════════════════════════════════════════════════════════
# SHARED RESULTS DISPLAY (metric cards + chart + table)
# ══════════════════════════════════════════════════════════════════════════════
def _show_results(x_pts, y_pts, x_query, result, method_name, extra_table_fn=None):
    """
    Render metric cards, result banner, chart, and optional table.
    extra_table_fn: callable that renders the method-specific difference table.
    """
    # Result banner
    st.markdown(f"""
    <div class="res-banner res-ok">
        <span class="res-dot"></span>
        <span class="res-msg">
            P({x_query}) computed successfully using {method_name}.
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # Metric cards
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="m-card" style="--m-accent: var(--amber); animation-delay:.1s;">
            <div class="m-card-bar" style="background:var(--amber);"></div>
            <div class="m-card-icon" style="--m-accent:var(--amber); --m-bg:var(--amber-dim);">P(x)</div>
            <div class="m-card-val">{result:.8f}</div>
            <div class="m-card-lbl">Interpolated Value</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="m-card" style="--m-accent: var(--cyan); animation-delay:.2s;">
            <div class="m-card-bar" style="background:var(--cyan);"></div>
            <div class="m-card-icon" style="--m-accent:var(--cyan); --m-bg:var(--cyan-dim);">x</div>
            <div class="m-card-val">{x_query}</div>
            <div class="m-card-lbl">Query Point</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="m-card" style="--m-accent: var(--violet); animation-delay:.3s;">
            <div class="m-card-bar" style="background:var(--violet);"></div>
            <div class="m-card-icon" style="--m-accent:var(--violet); --m-bg:var(--violet-dim);">n</div>
            <div class="m-card-val">{len(x_pts)}</div>
            <div class="m-card-lbl">Data Points</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

    # Interactive chart
    st.markdown("""<div class="sec-title"><span class="sec-title-bar"></span>Interactive Visualization</div>""",
                unsafe_allow_html=True)
    fig = plot_interpolation(x_pts, y_pts, x_query, result, method_name)
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': True, 'displaylogo': False,
        'toImageButtonOptions': {'format': 'png', 'filename': f'{method_name}_result', 'scale': 2}
    })
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="status-row">
        <span class="s-dot"></span>
        Complete &nbsp;·&nbsp; {method_name} &nbsp;·&nbsp; hover chart to explore &nbsp;·&nbsp; P({x_query}) = {result:.6f}
    </div>
    """, unsafe_allow_html=True)

    # Difference / basis table inside expander
    if extra_table_fn is not None:
        with st.expander("Full Computation Table — click to expand", expanded=True):
            extra_table_fn()


# ══════════════════════════════════════════════════════════════════════════════
# STREAMLIT UI
# ══════════════════════════════════════════════════════════════════════════════
def render_lab2():
    st.markdown(LAB2_CSS, unsafe_allow_html=True)
    st.components.v1.html(PARTICLE_HTML, height=0, scrolling=False)

    # ── Hero ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-section">
        <div class="hero-label"><span class="hero-label-bar"></span>Lab 02 · Numerical Methods</div>
        <div class="hero-heading">Interpolation <span>Methods</span></div>
        <p class="hero-desc">
            Estimate unknown values from a set of known data points using polynomial
            interpolation. All three methods are mathematically equivalent for the same
            data — choose based on spacing and convenience.
        </p>
        <div class="hero-tags">
            <span class="htag htag-v">Lagrange · Basis Polynomials</span>
            <span class="htag htag-c">Newton Forward · Equal Spacing</span>
            <span class="htag htag-e">Newton Divided · Any Spacing</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "Lagrange Interpolation",
        "Newton Forward Difference",
        "Newton Divided Difference",
    ])

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 1: LAGRANGE
    # ═════════════════════════════════════════════════════════════════════════
    with tab1:
        st.markdown("""
        <p class="method-sub" style="--accent: var(--violet);">
            Constructs the unique interpolating polynomial using weighted basis polynomials L_i(x).
            Works for any spacing — no equal-step requirement. Each L_i equals 1 at x_i and 0 at all other nodes.
        </p>
        """, unsafe_allow_html=True)

        ci, ca = st.columns([1.35, 1], gap="large")

        with ci:
            lx = st.text_input("x values (comma separated)", value="1, 2, 3, 4", key="lag_x")
            ly = st.text_input("y values (comma separated)", value="1, 4, 9, 16", key="lag_y")
            lq = st.number_input("Query point x", value=2.5, step=0.5, key="lag_q")

        with ca:
            st.markdown("""
            <div class="algo-box" style="--accent: var(--violet);">
                <div class="algo-box-bar" style="background: var(--violet);"></div>
                <div class="algo-box-label" style="color: var(--violet);">Lagrange Algorithm</div>
                <div class="algo-steps">
                    <span class="step-num">01</span> For each i, compute <span class="step-hl">L_i(x) = ∏(x−x_j)/(x_i−x_j)</span> [j≠i]<br>
                    <span class="step-num">02</span> Multiply: <span class="step-hl">term_i = y_i × L_i(x)</span><br>
                    <span class="step-num">03</span> Sum all terms: <span class="step-hl">P(x) = Σ term_i</span><br>
                    <span class="step-num">04</span> Property: <span class="step-hl">Σ L_i(x) = 1</span> always
                </div>
                <div class="algo-props">
                    <div class="algo-prop prop-amber"><span class="prop-dot"></span>Works for unequal spacing</div>
                    <div class="algo-prop prop-green"><span class="prop-dot"></span>Unique polynomial of degree ≤ n−1</div>
                    <div class="algo-prop prop-violet"><span class="prop-dot"></span>O(n²) per evaluation</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

        if st.button("Calculate — Lagrange", key="run_lag", use_container_width=True, type="primary"):
            try:
                x_pts = [float(v.strip()) for v in lx.split(",")]
                y_pts = [float(v.strip()) for v in ly.split(",")]
            except ValueError:
                st.error("Invalid input. Enter comma-separated numbers.")
                return
            if len(x_pts) != len(y_pts):
                st.error("x and y must have the same number of values.")
                return
            if len(x_pts) < 2:
                st.error("At least 2 data points are required.")
                return
            if len(set(x_pts)) != len(x_pts):
                st.error("x values must be distinct (no duplicates).")
                return

            with st.spinner("Computing Lagrange interpolation..."):
                result, Li_list = lagrange_interpolation(x_pts, y_pts, lq)

            _show_results(x_pts, y_pts, lq, result, "Lagrange",
                extra_table_fn=lambda: _render_lagrange_table(x_pts, y_pts, Li_list))

            _show_lagrange_steps(x_pts, y_pts, lq, result, Li_list)


    # ═════════════════════════════════════════════════════════════════════════
    # TAB 2: NEWTON FORWARD DIFFERENCE
    # ═════════════════════════════════════════════════════════════════════════
    with tab2:
        st.markdown("""
        <p class="method-sub" style="--accent: var(--cyan);">
            Uses finite forward differences on <strong>equally spaced</strong> x values.
            Efficient when data is tabulated at uniform intervals.
            Requires the query point to lie near the start of the table.
        </p>
        """, unsafe_allow_html=True)

        ci, ca = st.columns([1.35, 1], gap="large")

        with ci:
            nx = st.text_input("x values (equally spaced, comma separated)", value="0, 1, 2, 3", key="nf_x")
            ny = st.text_input("y values (comma separated)", value="1, 2, 5, 11", key="nf_y")
            nq = st.number_input("Query point x", value=0.5, step=0.5, key="nf_q")

        with ca:
            st.markdown("""
            <div class="algo-box" style="--accent: var(--cyan);">
                <div class="algo-box-bar" style="background: var(--cyan);"></div>
                <div class="algo-box-label" style="color: var(--cyan);">Newton Forward Algorithm</div>
                <div class="algo-steps">
                    <span class="step-num">01</span> Compute step: <span class="step-hl">h = x₁ − x₀</span><br>
                    <span class="step-num">02</span> Compute: <span class="step-hl">s = (x − x₀) / h</span><br>
                    <span class="step-num">03</span> Build forward difference table: <span class="step-hl">Δᵏyᵢ = Δᵏ⁻¹yᵢ₊₁ − Δᵏ⁻¹yᵢ</span><br>
                    <span class="step-num">04</span> <span class="step-hl">P(x) = y₀ + sΔy₀ + [s(s−1)/2!]Δ²y₀ + ...</span>
                </div>
                <div class="algo-props">
                    <div class="algo-prop prop-amber"><span class="prop-dot"></span>Requires equally spaced x</div>
                    <div class="algo-prop prop-green"><span class="prop-dot"></span>Best when x is near x₀</div>
                    <div class="algo-prop prop-violet"><span class="prop-dot"></span>Differences decrease for smooth data</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

        if st.button("Calculate — Newton Forward", key="run_nf", use_container_width=True, type="primary"):
            try:
                x_pts = [float(v.strip()) for v in nx.split(",")]
                y_pts = [float(v.strip()) for v in ny.split(",")]
            except ValueError:
                st.error("Invalid input. Enter comma-separated numbers.")
                return
            if len(x_pts) != len(y_pts):
                st.error("x and y must have the same number of values.")
                return
            if len(x_pts) < 2:
                st.error("At least 2 data points are required.")
                return

            with st.spinner("Computing Newton Forward Difference interpolation..."):
                try:
                    result, diff_table, s, h = newton_forward_difference(x_pts, y_pts, nq)
                except ValueError as e:
                    st.error(str(e))
                    return

            _show_results(x_pts, y_pts, nq, result, "Newton Forward Difference",
                extra_table_fn=lambda: _render_forward_table(x_pts, y_pts, diff_table))

            _show_newton_forward_steps(x_pts, y_pts, nq, result, diff_table, s, h)


    # ═════════════════════════════════════════════════════════════════════════
    # TAB 3: NEWTON DIVIDED DIFFERENCE
    # ═════════════════════════════════════════════════════════════════════════
    with tab3:
        st.markdown("""
        <p class="method-sub" style="--accent: var(--emerald);">
            Generalized Newton interpolation that works for <strong>any spacing</strong>.
            Builds a triangular divided difference table and evaluates the polynomial
            using Newton's nested form. Most versatile of the three methods.
        </p>
        """, unsafe_allow_html=True)

        ci, ca = st.columns([1.35, 1], gap="large")

        with ci:
            dx = st.text_input("x values (any spacing, comma separated)", value="1, 2, 4, 7", key="nd_x")
            dy = st.text_input("y values (comma separated)", value="3, 6, 10, 15", key="nd_y")
            dq = st.number_input("Query point x", value=3.0, step=0.5, key="nd_q")

        with ca:
            st.markdown("""
            <div class="algo-box" style="--accent: var(--emerald);">
                <div class="algo-box-bar" style="background: var(--emerald);"></div>
                <div class="algo-box-label" style="color: var(--emerald);">Newton Divided Difference Algorithm</div>
                <div class="algo-steps">
                    <span class="step-num">01</span> Set <span class="step-hl">f[xᵢ] = yᵢ</span><br>
                    <span class="step-num">02</span> <span class="step-hl">f[xᵢ,..,xₖ] = (f[xᵢ₊₁,..,xₖ]−f[xᵢ,..,xₖ₋₁]) / (xₖ−xᵢ)</span><br>
                    <span class="step-num">03</span> Coefficients = top row of table<br>
                    <span class="step-num">04</span> <span class="step-hl">P(x) = c₀ + c₁(x−x₀) + c₂(x−x₀)(x−x₁) + ...</span>
                </div>
                <div class="algo-props">
                    <div class="algo-prop prop-amber"><span class="prop-dot"></span>Works for unequal spacing</div>
                    <div class="algo-prop prop-green"><span class="prop-dot"></span>Adding a new point is easy</div>
                    <div class="algo-prop prop-violet"><span class="prop-dot"></span>Reduces to forward diff for equal h</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

        if st.button("Calculate — Newton Divided Difference", key="run_nd", use_container_width=True, type="primary"):
            try:
                x_pts = [float(v.strip()) for v in dx.split(",")]
                y_pts = [float(v.strip()) for v in dy.split(",")]
            except ValueError:
                st.error("Invalid input. Enter comma-separated numbers.")
                return
            if len(x_pts) != len(y_pts):
                st.error("x and y must have the same number of values.")
                return
            if len(x_pts) < 2:
                st.error("At least 2 data points are required.")
                return
            if len(set(x_pts)) != len(x_pts):
                st.error("x values must be distinct (no duplicates).")
                return

            with st.spinner("Computing Newton Divided Difference interpolation..."):
                result, div_table = newton_divided_difference(x_pts, y_pts, dq)

            _show_results(x_pts, y_pts, dq, result, "Newton Divided Difference",
                extra_table_fn=lambda: _render_divided_table(x_pts, y_pts, div_table))

            _show_newton_divided_steps(x_pts, y_pts, dq, result, div_table)


# ══════════════════════════════════════════════════════════════════════════════
# TABLE RENDERERS — called inside expanders
# ══════════════════════════════════════════════════════════════════════════════

def _render_lagrange_table(x_pts, y_pts, Li_list):
    """Render styled Lagrange basis polynomial table."""
    n = len(x_pts)
    rows = []
    for i in range(n):
        rows.append({
            'i':        i,
            'xᵢ':      x_pts[i],
            'yᵢ':      y_pts[i],
            'Lᵢ(x)':   round(Li_list[i], 8),
            'yᵢ · Lᵢ': round(y_pts[i] * Li_list[i], 8),
        })
    df = pd.DataFrame(rows)
    df.index = df.index + 1

    total_row = pd.DataFrame([{
        'i': '—',
        'xᵢ': '—',
        'yᵢ': '—',
        'Lᵢ(x)': round(sum(Li_list), 8),
        'yᵢ · Lᵢ': round(sum(y_pts[i] * Li_list[i] for i in range(n)), 8),
    }])
    df_display = pd.concat([df, total_row], ignore_index=True)
    df_display.index = list(range(1, n + 1)) + ['Σ']

    st.dataframe(
        df_display.style.set_properties(**{
            'font-family': 'JetBrains Mono, monospace',
            'font-size': '0.82rem',
        }).highlight_max(subset=['Lᵢ(x)'], color='rgba(167,139,250,0.15)'),
        use_container_width=True,
    )
    st.markdown(
        '<div style="font-family:JetBrains Mono,monospace;font-size:0.72rem;color:#4b5574;margin-top:0.4rem;">'
        'Note: Σ Lᵢ(x) should equal 1.0 — verifies correctness of basis polynomials.'
        '</div>',
        unsafe_allow_html=True
    )


def _render_forward_table(x_pts, y_pts, diff_table):
    """Render Newton Forward Difference table with proper triangle structure."""
    n = len(x_pts)
    col_headers = ['x', 'y (Δ⁰)'] + [f'Δ{k}' for k in range(1, n)]
    rows = []
    for i in range(n):
        row = {'x': x_pts[i]}
        for j in range(n - i):
            if j == 0:
                row['y (Δ⁰)'] = round(diff_table[i][j], 8)
            else:
                row[f'Δ{j}'] = round(diff_table[i][j], 8)
        rows.append(row)
    df = pd.DataFrame(rows)
    df.index = df.index + 1
    st.dataframe(df, use_container_width=True)
    st.markdown(
        '<div style="font-family:JetBrains Mono,monospace;font-size:0.72rem;color:#4b5574;margin-top:0.4rem;">'
        'The top row (row 1) provides the coefficients used in the Newton Forward formula.'
        '</div>',
        unsafe_allow_html=True
    )


def _render_divided_table(x_pts, y_pts, div_table):
    """Render Newton Divided Difference table with triangle structure."""
    n = len(x_pts)
    col_headers = ['x', 'f[.]'] + [f'f[{"·"*(k+1)}]' for k in range(1, n)]
    rows = []
    for i in range(n):
        row = {'x': x_pts[i], 'f[.]': round(div_table[i][0], 8)}
        for j in range(1, n - i):
            row[f'f[{"·"*j}]'] = round(div_table[i][j], 8)
        rows.append(row)
    df = pd.DataFrame(rows)
    df.index = df.index + 1
    st.dataframe(df, use_container_width=True)
    st.markdown(
        '<div style="font-family:JetBrains Mono,monospace;font-size:0.72rem;color:#4b5574;margin-top:0.4rem;">'
        'The top row (row 1) gives the divided difference coefficients c₀, c₁, c₂, ... for the polynomial.'
        '</div>',
        unsafe_allow_html=True
    )
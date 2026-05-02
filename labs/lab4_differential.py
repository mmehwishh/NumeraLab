"""
lab4_differential.py - Lab 4: Ordinary Differential Equations
==============================================================
Methods:
  1. Euler Method          -> euler_method()
  2. Modified Euler Method -> modified_euler()
  3. Heun's Method         -> heuns_method()

Main UI function:
  render_lab4()

UI v5.0 — PREMIUM REDESIGN (matches Lab 2 style exactly)
──────────────────────────────────────────────────────────
• Hero section with animated gradient heading and method tags
• Algo cards per tab with numbered steps and property pills
• Metric result cards (consistent with Lab 1 & 2)
• Full step-by-step working shown per iteration after calculation
• Premium styled step tables with proper column headers
• Styled st.dataframe tables with monospace font + highlighted rows
• Dual-panel Plotly chart: solution curve + step-size convergence
• Particle background + full CSS theme
• ALL LOGIC VERIFIED AND CORRECT
• ALL COMMENTS IN ENGLISH
"""

import numpy as np
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.helpers import parse_ode


# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — MATCHES LAB 2 PREMIUM THEME EXACTLY
# ══════════════════════════════════════════════════════════════════════════════
LAB4_CSS = r"""
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
        radial-gradient(ellipse 60% 50% at 10% 20%, rgba(34,211,238,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 50% 60% at 90% 80%, rgba(52,211,153,0.05) 0%, transparent 60%),
        linear-gradient(180deg, rgba(14,20,40,0.8) 0%, rgba(7,9,15,0.9) 100%);
    border: 1px solid rgba(34,211,238,0.08);
}
.hero-section::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent 5%, var(--cyan) 30%, var(--emerald) 70%, transparent 95%);
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
    background: linear-gradient(135deg, var(--cyan) 0%, var(--emerald) 100%);
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
    border-color: var(--accent, var(--cyan));
    box-shadow: 0 0 30px rgba(34,211,238,0.05);
}
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

/* ─── STEP CARDS ──────────────────────────────────────────── */
.step-card {
    background: var(--bg-glass);
    border: 1px solid rgba(34,211,238,0.10);
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
    background: var(--step-accent, var(--cyan));
    opacity: 0.7;
}
.step-card-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--step-accent, var(--cyan));
    margin-bottom: 0.45rem;
}
.step-card-body {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: var(--text-1);
    line-height: 1.9;
}
.step-card-body .hl  { color: var(--amber);   font-weight: 600; }
.step-card-body .hl2 { color: var(--emerald); font-weight: 600; }
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
    align-items: center; justify-content: center;
    margin-bottom: 0.6rem;
    font-size: 0.85rem;
    font-weight: 800;
    color: var(--m-accent, var(--cyan));
    background: var(--m-bg, var(--cyan-dim));
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
    border-color: rgba(34,211,238,0.2);
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
    background: linear-gradient(90deg, var(--cyan), var(--emerald));
    display: inline-block;
}

/* ─── METHOD SUBTITLE ─────────────────────────────────────── */
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

/* ─── ODE INPUT LABEL ─────────────────────────────────────── */
.ode-lbl {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: var(--cyan);
    letter-spacing: 0.08em;
    margin-bottom: 0.3rem;
    font-weight: 600;
}
.ex-lbl {
    font-family: 'Inter', sans-serif;
    font-size: 0.68rem;
    color: var(--text-3);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 0.35rem;
    margin-top: 0.4rem;
}

/* ─── RUN BUTTON ──────────────────────────────────────────── */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #0ea5e9, #10b981, #34d399) !important;
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
    box-shadow: 0 4px 20px rgba(16,185,129,0.3) !important;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(16,185,129,0.45) !important;
    filter: brightness(1.08) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:active {
    transform: translateY(0) scale(0.98) !important;
}

/* ─── SECONDARY BUTTONS ───────────────────────────────────── */
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

/* ─── INPUTS ──────────────────────────────────────────────── */
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
    background: rgba(34,211,238,0.04) !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--cyan) !important;
    background: rgba(34,211,238,0.08) !important;
    border-bottom: 2.5px solid var(--cyan) !important;
}

/* ─── EXPANDER ────────────────────────────────────────────── */
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

/* ─── DATA TABLE OVERRIDE ─────────────────────────────────── */
div[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid rgba(34,211,238,0.10) !important;
}
div[data-testid="stDataFrame"] table {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.80rem !important;
}
div[data-testid="stDataFrame"] thead th {
    background: rgba(34,211,238,0.06) !important;
    color: var(--cyan) !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    border-bottom: 1px solid rgba(34,211,238,0.15) !important;
}
div[data-testid="stDataFrame"] tbody tr:hover {
    background: rgba(34,211,238,0.03) !important;
}

/* ─── MISC ────────────────────────────────────────────────── */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(34,211,238,0.12), rgba(52,211,153,0.12), transparent) !important;
    margin: 1.8rem 0 !important;
}
</style>
"""

# ── Particle Background ───────────────────────────────────────────────────────
PARTICLE_HTML = """
<canvas id="pCanvas4" style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:0;"></canvas>
<script>
(function(){
    var c=document.getElementById('pCanvas4');if(!c)return;
    var ctx=c.getContext('2d'),w,h,pts=[];
    function rs(){w=c.width=window.innerWidth;h=c.height=window.innerHeight;}
    rs();window.addEventListener('resize',rs);
    var cols=['#22d3ee','#34d399','#a78bfa','#fbbf24'];
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
# METHOD 1: EULER METHOD
# ══════════════════════════════════════════════════════════════════════════════
def euler_method(func, x0: float, y0: float, x_end: float, h: float):
    """
    Euler's Method for solving dy/dx = f(x, y).

    Formula:
        y_{n+1} = y_n + h * f(x_n, y_n)

    This is a first-order, single-step explicit method.
    Global truncation error is O(h) — one order in h.

    Parameters:
        func  : callable f(x, y)
        x0    : initial x value
        y0    : initial y value (initial condition)
        x_end : final x value to integrate to
        h     : step size

    Returns:
        x_vals : list of x values at each step (including x0)
        y_vals : list of computed y values (including y0)
        table  : list of dicts — one dict per step with all sub-calculations
    """
    x_vals = [x0]
    y_vals = [y0]
    table  = []
    x, y   = x0, y0

    # March forward until we reach (or pass) x_end
    # The small tolerance 1e-9 avoids floating-point overshoot
    while x < x_end - 1e-9:
        fxy    = float(func(x, y))        # Slope at current point (float ensures numeric result)
        h_f    = h * fxy                  # Increment = h * slope
        y_next = y + h_f                  # New y value
        x_next = round(x + h, 10)         # New x (rounded to avoid float drift)

        table.append({
            'xₙ':          round(x,      8),
            'yₙ':          round(y,      8),
            'f(xₙ, yₙ)':  round(fxy,   8),
            'h · f(xₙ,yₙ)': round(h_f, 8),
            'yₙ₊₁':       round(y_next, 8),
        })

        x, y = x_next, y_next
        x_vals.append(round(x, 10))
        y_vals.append(y)

    return x_vals, y_vals, table


# ══════════════════════════════════════════════════════════════════════════════
# METHOD 2: MODIFIED EULER METHOD (Improved Euler / Euler-Heun)
# ══════════════════════════════════════════════════════════════════════════════
def modified_euler(func, x0: float, y0: float, x_end: float, h: float):
    """
    Modified Euler Method (also called Improved Euler or Euler-Heun).

    Formula:
        k1       = f(x_n, y_n)                    # slope at start of interval
        k2       = f(x_n + h,  y_n + h * k1)      # slope at predicted end
        y_{n+1}  = y_n + (h / 2) * (k1 + k2)      # average of both slopes

    This is a second-order method. Global error is O(h²).
    Two function evaluations are required per step.

    Parameters:
        func  : callable f(x, y)
        x0    : initial x value
        y0    : initial y value
        x_end : final x value
        h     : step size

    Returns:
        x_vals : list of x values
        y_vals : list of computed y values
        table  : list of dicts — one per step
    """
    x_vals = [x0]
    y_vals = [y0]
    table  = []
    x, y   = x0, y0

    while x < x_end - 1e-9:
        k1        = float(func(x, y))             # First slope (at current point)
        k2        = float(func(x + h, y + h * k1)) # Second slope (at predicted next point)
        avg_slope = (k1 + k2) / 2.0               # Average slope
        y_next    = y + h * avg_slope              # Corrected next y
        x_next    = round(x + h, 10)

        table.append({
            'xₙ':                   round(x,         8),
            'yₙ':                   round(y,         8),
            'k1 = f(xₙ, yₙ)':      round(k1,        8),
            'k2 = f(xₙ+h, yₙ+hk1)': round(k2,      8),
            'Avg Slope (k1+k2)/2':  round(avg_slope, 8),
            'yₙ₊₁':                round(y_next,    8),
        })

        x, y = x_next, y_next
        x_vals.append(round(x, 10))
        y_vals.append(y)

    return x_vals, y_vals, table


# ══════════════════════════════════════════════════════════════════════════════
# METHOD 3: HEUN'S METHOD (Predictor-Corrector)
# ══════════════════════════════════════════════════════════════════════════════
def heuns_method(func, x0: float, y0: float, x_end: float, h: float):
    """
    Heun's Method — an explicit predictor-corrector scheme.

    Formula:
        Predictor: y*_{n+1} = y_n + h * f(x_n, y_n)          # Euler step
        f₀       = f(x_n,     y_n)                             # Slope at start
        f₁       = f(x_{n+1}, y*_{n+1})                       # Slope at predicted end
        Corrector: y_{n+1}  = y_n + (h / 2) * (f₀ + f₁)      # Weighted average

    This is a second-order method. Global error is O(h²).
    Mathematically equivalent to Modified Euler but structured as
    an explicit predictor-corrector for pedagogical clarity.

    Parameters:
        func  : callable f(x, y)
        x0    : initial x value
        y0    : initial y value
        x_end : final x value
        h     : step size

    Returns:
        x_vals : list of x values
        y_vals : list of computed y values
        table  : list of dicts — one per step
    """
    x_vals = [x0]
    y_vals = [y0]
    table  = []
    x, y   = x0, y0

    while x < x_end - 1e-9:
        f0     = float(func(x, y))                # Slope at current point
        y_pred = y + h * f0                        # Predictor (Euler forward step)
        f1     = float(func(x + h, y_pred))       # Slope at predicted endpoint
        y_next = y + (h / 2.0) * (f0 + f1)       # Corrector (average slope)
        x_next = round(x + h, 10)

        table.append({
            'xₙ':               round(x,      8),
            'yₙ':               round(y,      8),
            'f₀ = f(xₙ, yₙ)':  round(f0,     8),
            'y* (Predictor)':   round(y_pred, 8),
            'f₁ = f(xₙ₊₁, y*)': round(f1,   8),
            'yₙ₊₁ (Corrected)': round(y_next, 8),
        })

        x, y = x_next, y_next
        x_vals.append(round(x, 10))
        y_vals.append(y)

    return x_vals, y_vals, table


# ══════════════════════════════════════════════════════════════════════════════
# DUAL-PANEL PLOTLY CHART
# ══════════════════════════════════════════════════════════════════════════════
def plot_ode_solution(x_vals, y_vals, method_name, accent='#22d3ee'):
    """
    Build a dual-panel interactive Plotly figure.

    Left panel  : solution curve y(x) with shaded fill, initial condition
                  marker (diamond), and final value marker (star).
    Right panel : bar chart of y values at each step index for quick
                  visual comparison of how y evolves step by step.

    Parameters:
        x_vals      : list of x values
        y_vals      : list of corresponding y values
        method_name : string label used in subplot titles
        accent      : hex color for the solution line

    Returns:
        fig : Plotly Figure object ready for st.plotly_chart()
    """
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(
            f'<b style="font-family:Inter">{method_name}</b>  ·  Solution Curve  y(x)',
            f'<b style="font-family:Inter">{method_name}</b>  ·  y Values per Step',
        ),
        column_widths=[0.62, 0.38],
        horizontal_spacing=0.09,
    )

    # ── Left panel: shaded area under the solution curve ─────────────────────
    y_min = min(y_vals)
    fig.add_trace(go.Scatter(
        x=x_vals + x_vals[::-1],
        y=y_vals + [y_min] * len(y_vals),
        fill='toself',
        fillcolor='rgba(34,211,238,0.04)',
        line=dict(color='rgba(0,0,0,0)'),
        showlegend=False, hoverinfo='skip',
    ), row=1, col=1)

    # Solution curve line + markers
    fig.add_trace(go.Scatter(
        x=x_vals, y=y_vals,
        mode='lines+markers', name='y(x)',
        line=dict(color=accent, width=2.5, shape='spline'),
        marker=dict(size=6, color='#a78bfa', line=dict(width=1.5, color='#ddd6fe')),
        hovertemplate='<b>x = %{x:.4f}</b><br>y = %{y:.8f}<extra></extra>',
    ), row=1, col=1)

    # Initial condition marker — gold diamond
    fig.add_trace(go.Scatter(
        x=[x_vals[0]], y=[y_vals[0]], mode='markers',
        name=f'IC: ({x_vals[0]}, {y_vals[0]:.4f})',
        marker=dict(size=13, color='#fbbf24', symbol='diamond',
                    line=dict(width=2, color='#fef3c7')),
        hovertemplate=f'Initial Condition<br>x={x_vals[0]}<br>y={y_vals[0]:.6f}<extra></extra>',
    ), row=1, col=1)

    # Final value marker — green star with text label
    fig.add_trace(go.Scatter(
        x=[x_vals[-1]], y=[y_vals[-1]], mode='markers+text',
        name=f'Final: y({x_vals[-1]:.3f}) = {y_vals[-1]:.4f}',
        marker=dict(size=13, color='#34d399', symbol='star',
                    line=dict(width=1.5, color='#a7f3d0')),
        text=[f'  y = {y_vals[-1]:.4f}'], textposition='top right',
        textfont=dict(color='#6ee7b7', size=10, family='JetBrains Mono'),
        hovertemplate=f'Final Value<br>x={x_vals[-1]:.4f}<br>y={y_vals[-1]:.8f}<extra></extra>',
    ), row=1, col=1)

    # ── Right panel: gradient bar chart of y values per step ─────────────────
    n_steps     = len(x_vals)
    step_indices = list(range(n_steps))
    bar_colors  = [
        f'rgba(34,211,238,{0.35 + 0.55 * (i / max(n_steps - 1, 1))})'
        for i in step_indices
    ]

    fig.add_trace(go.Bar(
        x=step_indices,
        y=y_vals,
        name='y per step',
        marker=dict(
            color=bar_colors,
            line=dict(color='rgba(34,211,238,0.2)', width=0.5),
        ),
        customdata=[[x_vals[i], y_vals[i]] for i in step_indices],
        hovertemplate='Step %{x}<br>x = %{customdata[0]:.4f}<br>y = %{customdata[1]:.6f}<extra></extra>',
    ), row=1, col=2)

    # ── Shared axis style ─────────────────────────────────────────────────────
    ax = dict(
        gridcolor='rgba(30,41,59,0.5)', gridwidth=0.5,
        zerolinecolor='#1e293b', zerolinewidth=1,
        linecolor='#1e293b', linewidth=0.6,
        tickfont=dict(size=10, color='#4b5574', family='JetBrains Mono'),
        title_font=dict(size=11, color='#64748b', family='Inter'),
    )

    fig.update_layout(
        height=500,
        plot_bgcolor='#0c1021', paper_bgcolor='#07090f',
        font=dict(family='Inter', color='#8b95b0', size=12),
        legend=dict(
            bgcolor='rgba(12,16,33,0.9)', bordercolor='rgba(34,211,238,0.1)', borderwidth=1,
            font=dict(size=10.5, color='#e8ecf4', family='Inter'),
            orientation='h', yanchor='bottom', y=-0.22, xanchor='center', x=0.5,
        ),
        margin=dict(l=55, r=25, t=55, b=80),
        hoverlabel=dict(
            bgcolor='rgba(12,16,33,0.95)', bordercolor='rgba(34,211,238,0.2)',
            font=dict(family='JetBrains Mono', size=12, color='#e8ecf4'),
        ),
        bargap=0.18,
    )
    fig.update_xaxes(title_text='x',          **ax, row=1, col=1)
    fig.update_yaxes(title_text='y(x)',        **ax, row=1, col=1)
    fig.update_xaxes(title_text='Step Index',  **ax, row=1, col=2)
    fig.update_yaxes(title_text='y value',     **ax, row=1, col=2)

    # Style subplot titles
    for ann in fig.layout.annotations:
        ann.font = dict(size=12, color='#e8ecf4', family='Inter')

    return fig


# ══════════════════════════════════════════════════════════════════════════════
# STEP-BY-STEP DISPLAY HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def _step_card(header: str, body: str, accent: str = 'var(--cyan)', delay_idx: int = 0):
    """
    Render a single styled step card with:
      - A left colored accent bar whose color is controlled by --step-accent
      - A monospace header label (e.g. 'Step 1', 'Formula')
      - A monospace body with HTML spans for color highlights
    """
    st.markdown(f"""
    <div class="step-card" style="--step-accent: {accent}; animation-delay:{delay_idx * 0.06}s;">
        <div class="step-card-header">{header}</div>
        <div class="step-card-body">{body}</div>
    </div>
    """, unsafe_allow_html=True)


def _show_euler_steps(table, h, ode_str):
    """
    Render a formula card followed by per-iteration step cards for Euler Method.
    Shows all steps (up to 8 inline cards); remaining steps are noted below.

    Each card shows:
      - x_n, y_n (current values)
      - f(x_n, y_n) (slope)
      - h * f (increment)
      - y_{n+1} (result)
    """
    st.markdown(
        """<div class="sec-title"><span class="sec-title-bar"></span>Step-by-Step Working</div>""",
        unsafe_allow_html=True,
    )

    # Formula reference card shown before all steps
    _step_card(
        "Formula — Euler Method",
        f'dy/dx = f(x, y) = <span class="hl">{ode_str}</span><br>'
        f'y_{{n+1}} = y_n + h &middot; f(x_n, y_n) &nbsp;|&nbsp; h = <span class="hl">{h}</span>',
        accent='var(--violet)', delay_idx=0,
    )

    # Cycle through accent colors to visually distinguish each step
    accents = [
        'var(--cyan)', 'var(--emerald)', 'var(--amber)', 'var(--violet)',
        'var(--cyan)', 'var(--emerald)', 'var(--amber)', 'var(--violet)',
    ]

    display_rows = table[:8]  # Cap inline display at 8 steps; rest visible in table
    for idx, row in enumerate(display_rows):
        body = (
            f'x_n = <span class="hl">{row["xₙ"]}</span> &nbsp;|&nbsp; '
            f'y_n = <span class="hl">{row["yₙ"]}</span><br>'
            f'f(x_n, y_n) = <span class="hl">{row["f(xₙ, yₙ)"]}</span><br>'
            f'h &middot; f = {h} &times; {row["f(xₙ, yₙ)"]} = '
            f'<span class="hl">{row["h · f(xₙ,yₙ)"]}</span><br>'
            f'y_{{n+1}} = {row["yₙ"]} + {row["h · f(xₙ,yₙ)"]} = '
            f'<span class="hl2">{row["yₙ₊₁"]}</span>'
        )
        _step_card(f"Step {idx + 1}", body, accent=accents[idx % len(accents)], delay_idx=idx + 1)

    # Notify user if steps were truncated from inline cards
    if len(table) > 8:
        st.markdown(
            f'<div class="status-row"><span class="s-dot"></span>'
            f'{len(table) - 8} more steps — see full table above.</div>',
            unsafe_allow_html=True,
        )


def _show_modified_euler_steps(table, h, ode_str):
    """
    Render a formula card followed by per-iteration step cards for Modified Euler.
    Shows all steps (up to 8 inline); remaining noted below.

    Each card shows:
      - x_n, y_n
      - k1, k2
      - average slope
      - y_{n+1}
    """
    st.markdown(
        """<div class="sec-title"><span class="sec-title-bar"></span>Step-by-Step Working</div>""",
        unsafe_allow_html=True,
    )

    _step_card(
        "Formula — Modified Euler Method",
        f'dy/dx = f(x, y) = <span class="hl">{ode_str}</span><br>'
        f'k1 = f(x_n, y_n)<br>'
        f'k2 = f(x_n + h, y_n + h &middot; k1)<br>'
        f'y_{{n+1}} = y_n + (h/2) &middot; (k1 + k2) &nbsp;|&nbsp; h = <span class="hl">{h}</span>',
        accent='var(--violet)', delay_idx=0,
    )

    accents = [
        'var(--cyan)', 'var(--emerald)', 'var(--amber)', 'var(--violet)',
        'var(--cyan)', 'var(--emerald)', 'var(--amber)', 'var(--violet)',
    ]

    display_rows = table[:8]
    for idx, row in enumerate(display_rows):
        body = (
            f'x_n = <span class="hl">{row["xₙ"]}</span> &nbsp;|&nbsp; '
            f'y_n = <span class="hl">{row["yₙ"]}</span><br>'
            f'k1 = f(x_n, y_n) = <span class="hl">{row["k1 = f(xₙ, yₙ)"]}</span><br>'
            f'k2 = f(x_n+h, y_n+h&middot;k1) = <span class="hl">{row["k2 = f(xₙ+h, yₙ+hk1)"]}</span><br>'
            f'Avg slope = (k1 + k2) / 2 = <span class="hl">{row["Avg Slope (k1+k2)/2"]}</span><br>'
            f'y_{{n+1}} = {row["yₙ"]} + {h} &middot; {row["Avg Slope (k1+k2)/2"]} = '
            f'<span class="hl2">{row["yₙ₊₁"]}</span>'
        )
        _step_card(f"Step {idx + 1}", body, accent=accents[idx % len(accents)], delay_idx=idx + 1)

    if len(table) > 8:
        st.markdown(
            f'<div class="status-row"><span class="s-dot"></span>'
            f'{len(table) - 8} more steps — see full table above.</div>',
            unsafe_allow_html=True,
        )


def _show_heun_steps(table, h, ode_str):
    """
    Render a formula card followed by per-iteration step cards for Heun's Method.
    Shows all steps (up to 8 inline); remaining noted below.

    Each card shows:
      - x_n, y_n
      - f0 = f(x_n, y_n)
      - Predictor: y* = y_n + h * f0
      - f1 = f(x_{n+1}, y*)
      - Corrector: y_{n+1} = y_n + (h/2)*(f0 + f1)
    """
    st.markdown(
        """<div class="sec-title"><span class="sec-title-bar"></span>Step-by-Step Working</div>""",
        unsafe_allow_html=True,
    )

    _step_card(
        "Formula — Heun's Method (Predictor-Corrector)",
        f'dy/dx = f(x, y) = <span class="hl">{ode_str}</span><br>'
        f'<span class="dim">Predictor:</span> y* = y_n + h &middot; f(x_n, y_n)<br>'
        f'<span class="dim">Corrector:</span> y_{{n+1}} = y_n + (h/2) &middot; [f(x_n, y_n) + f(x_{{n+1}}, y*)]'
        f'&nbsp;|&nbsp; h = <span class="hl">{h}</span>',
        accent='var(--violet)', delay_idx=0,
    )

    accents = [
        'var(--cyan)', 'var(--emerald)', 'var(--amber)', 'var(--violet)',
        'var(--cyan)', 'var(--emerald)', 'var(--amber)', 'var(--violet)',
    ]

    display_rows = table[:8]
    for idx, row in enumerate(display_rows):
        body = (
            f'x_n = <span class="hl">{row["xₙ"]}</span> &nbsp;|&nbsp; '
            f'y_n = <span class="hl">{row["yₙ"]}</span><br>'
            f'f₀ = f(x_n, y_n) = <span class="hl">{row["f₀ = f(xₙ, yₙ)"]}</span><br>'
            f'<span class="dim">Predictor:</span> y* = {row["yₙ"]} + {h} &times; {row["f₀ = f(xₙ, yₙ)"]} '
            f'= <span class="hl">{row["y* (Predictor)"]}</span><br>'
            f'f₁ = f(x_{{n+1}}, y*) = <span class="hl">{row["f₁ = f(xₙ₊₁, y*)"]}</span><br>'
            f'<span class="dim">Corrector:</span> y_{{n+1}} = {row["yₙ"]} + ({h}/2) &times; '
            f'({row["f₀ = f(xₙ, yₙ)"]} + {row["f₁ = f(xₙ₊₁, y*)"]}) '
            f'= <span class="hl2">{row["yₙ₊₁ (Corrected)"]}</span>'
        )
        _step_card(f"Step {idx + 1}", body, accent=accents[idx % len(accents)], delay_idx=idx + 1)

    if len(table) > 8:
        st.markdown(
            f'<div class="status-row"><span class="s-dot"></span>'
            f'{len(table) - 8} more steps — see full table above.</div>',
            unsafe_allow_html=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
# PREMIUM TABLE RENDERER — matches Lab 2 styled dataframe approach
# ══════════════════════════════════════════════════════════════════════════════

def _render_iteration_table(table, method_name, h, ode_str, accent_col):
    """
    Render the full iteration table inside an expander using a styled
    st.dataframe. The last column (y_{n+1}) is highlighted to draw attention
    to the result of each step.

    Parameters:
        table      : list of dicts from euler/modified_euler/heuns_method
        method_name: string for the expander label
        h          : step size (shown in caption below table)
        ode_str    : ODE string (shown in caption)
        accent_col : name of the final result column to highlight
    """
    with st.expander(f"Full Iteration Table — {method_name} — all steps", expanded=True):
        df = pd.DataFrame(table)
        df.index = range(1, len(df) + 1)
        df.index.name = "Step"

        # Apply monospace font and highlight the result column
        styled = (
            df.style
            .set_properties(**{
                'font-family': 'JetBrains Mono, monospace',
                'font-size':   '0.81rem',
            })
            .highlight_max(
                subset=[accent_col],
                color='rgba(52,211,153,0.15)',
            )
            .highlight_min(
                subset=[accent_col],
                color='rgba(251,113,133,0.10)',
            )
            .format(precision=8)
        )

        st.dataframe(styled, use_container_width=True)

        # Caption row below table
        st.markdown(
            '<div style="font-family:JetBrains Mono,monospace;font-size:0.72rem;'
            'color:#4b5574;margin-top:0.4rem;">'
            f'Total {len(table)} step(s) &nbsp;|&nbsp; h = {h} &nbsp;|&nbsp; '
            f'dy/dx = {ode_str} &nbsp;|&nbsp; '
            f'<span style="color:#34d399;">green</span> = max {accent_col} &nbsp;|&nbsp; '
            f'<span style="color:#fb7185;">red</span> = min {accent_col}'
            '</div>',
            unsafe_allow_html=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
# SHARED RESULTS DISPLAY (result banner + metric cards + table + chart + steps)
# ══════════════════════════════════════════════════════════════════════════════

def _show_results(x_vals, y_vals, table, method_name, h, ode_str,
                  accent='#22d3ee', result_col='yₙ₊₁'):
    """
    Full results section rendered after computation. In order:
      1. Result banner (green pill with final answer)
      2. Four metric cards: final y, steps, step size h, x range
      3. Full iteration table (styled dataframe in expander, expanded by default)
      4. Dual-panel interactive Plotly chart

    Parameters:
        x_vals      : list of x values
        y_vals      : list of y values
        table       : list of dicts with per-step data
        method_name : string for display
        h           : step size
        ode_str     : ODE expression string
        accent      : hex color for the chart line
        result_col  : name of the result column in table (used for highlighting)
    """

    # ── 1. Result Banner ─────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="res-banner res-ok">
        <span class="res-dot"></span>
        <span class="res-msg">
            y({x_vals[-1]:.4f}) &asymp; <strong>{y_vals[-1]:.8f}</strong>
            &nbsp;&mdash;&nbsp; {method_name} &nbsp;&mdash;&nbsp; {len(table)} step(s) completed.
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # ── 2. Metric Cards ───────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="m-card" style="--m-accent: var(--amber); animation-delay:.1s;">
            <div class="m-card-bar" style="background:var(--amber);"></div>
            <div class="m-card-icon" style="--m-accent:var(--amber); --m-bg:var(--amber-dim);">y*</div>
            <div class="m-card-val">{y_vals[-1]:.6f}</div>
            <div class="m-card-lbl">Final y value</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="m-card" style="--m-accent: var(--cyan); animation-delay:.2s;">
            <div class="m-card-bar" style="background:var(--cyan);"></div>
            <div class="m-card-icon" style="--m-accent:var(--cyan); --m-bg:var(--cyan-dim);">n</div>
            <div class="m-card-val">{len(table)}</div>
            <div class="m-card-lbl">Steps taken</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="m-card" style="--m-accent: var(--emerald); animation-delay:.3s;">
            <div class="m-card-bar" style="background:var(--emerald);"></div>
            <div class="m-card-icon" style="--m-accent:var(--emerald); --m-bg:var(--emerald-dim);">h</div>
            <div class="m-card-val">{h}</div>
            <div class="m-card-lbl">Step size h</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        x_range = round(x_vals[-1] - x_vals[0], 8)
        st.markdown(f"""
        <div class="m-card" style="--m-accent: var(--violet); animation-delay:.4s;">
            <div class="m-card-bar" style="background:var(--violet);"></div>
            <div class="m-card-icon" style="--m-accent:var(--violet); --m-bg:var(--violet-dim);">Δx</div>
            <div class="m-card-val">{x_range}</div>
            <div class="m-card-lbl">x range</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

    # ── 3. Full Iteration Table ───────────────────────────────────────────────
    _render_iteration_table(table, method_name, h, ode_str, result_col)

    # ── 4. Interactive Dual-Panel Chart ───────────────────────────────────────
    st.markdown(
        """<div class="sec-title"><span class="sec-title-bar"></span>Interactive Visualization</div>""",
        unsafe_allow_html=True,
    )

    fig = plot_ode_solution(x_vals, y_vals, method_name, accent)
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': True,
        'displaylogo':    False,
        'toImageButtonOptions': {
            'format':   'png',
            'filename': f'{method_name.replace(" ", "_")}_ode',
            'scale':    2,
        },
    })
    st.markdown('</div>', unsafe_allow_html=True)

    # Completion status row
    st.markdown(f"""
    <div class="status-row">
        <span class="s-dot"></span>
        Complete &nbsp;&middot;&nbsp; {method_name} &nbsp;&middot;&nbsp;
        {len(table)} step(s) &nbsp;&middot;&nbsp; hover chart to inspect each point
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# STREAMLIT UI — render_lab4()
# ══════════════════════════════════════════════════════════════════════════════

def render_lab4():
    """
    Main entry point for Lab 4.
    Injects CSS, renders the hero section, and displays three method tabs.
    Each tab follows the same pattern:
      1. Method description paragraph
      2. Two-column layout: inputs on left, algo card on right
      3. Calculate button
      4. Results: banner → metric cards → iteration table → chart → step cards
    """
    st.markdown(LAB4_CSS, unsafe_allow_html=True)
    st.components.v1.html(PARTICLE_HTML, height=0, scrolling=False)

    # ── Hero Section ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-section">
        <div class="hero-label"><span class="hero-label-bar"></span>Lab 04 · Numerical Methods</div>
        <div class="hero-heading">Differential <span>Equations</span></div>
        <p class="hero-desc">
            Numerically solve first-order initial value problems
            <code>dy/dx = f(x, y)</code> with initial condition <code>y(x₀) = y₀</code>.
            All three methods march forward from the initial condition
            using a fixed step size h, producing a discrete approximation of the solution curve.
        </p>
        <div class="hero-tags">
            <span class="htag htag-c">Euler · O(h) · 1 eval/step</span>
            <span class="htag htag-v">Modified Euler · O(h²) · 2 evals/step</span>
            <span class="htag htag-e">Heun's · O(h²) · Predictor-Corrector</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Four tabs: three methods + user guide ────────────────────────────────
    tab1, tab2, tab3, tab_guide = st.tabs([
        "📐  Euler Method",
        "📈  Modified Euler Method",
        "🔁  Heun's Method",
        "📖  User Guide",
    ])

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 1: EULER METHOD
    # ═════════════════════════════════════════════════════════════════════════
    with tab1:
        st.markdown("""
        <p class="method-sub" style="--accent: var(--cyan);">
            The simplest one-step explicit method. Uses only the slope at the current point
            to project the solution forward by one step. First-order accurate — global error
            is proportional to h. Use a smaller h for better accuracy.
        </p>
        """, unsafe_allow_html=True)

        ci, ca = st.columns([1.35, 1], gap="large")

        with ci:
            st.markdown("<div class='ode-lbl'>dy/dx = f(x, y)</div>", unsafe_allow_html=True)
            eu_ode = st.text_input(
                "f(x, y) =", value="x + y", key="eu_ode",
                placeholder="e.g.  x + y   or   x*y - 2   or   sin(x)*y",
            )

            st.markdown("<div class='ex-lbl'>Quick examples</div>", unsafe_allow_html=True)
            ec = st.columns(4)
            eu_examples = ["x + y", "x*y", "x - y", "sin(x) + y"]
            for i, (col, ex) in enumerate(zip(ec, eu_examples)):
                if col.button(ex, key=f"eu_ex{i}", use_container_width=True):
                    st.session_state["eu_ode"] = ex
                    st.rerun()

            st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
            r1, r2 = st.columns(2)
            eu_x0   = r1.number_input("Initial x₀", value=0.0, step=0.5, key="eu_x0")
            eu_y0   = r2.number_input("Initial y₀", value=1.0, step=0.5, key="eu_y0")
            r3, r4  = st.columns(2)
            eu_xend = r3.number_input("Final x",    value=2.0, step=0.5, key="eu_xend")
            eu_h    = r4.number_input(
                "Step size h", value=0.2, step=0.05,
                min_value=0.001, format="%.4f", key="eu_h",
            )

        with ca:
            st.markdown("""
            <div class="algo-box" style="--accent: var(--cyan);">
                <div class="algo-box-bar" style="background: var(--cyan);"></div>
                <div class="algo-box-label" style="color: var(--cyan);">Euler Algorithm</div>
                <div class="algo-steps">
                    <span class="step-num">01</span> Evaluate slope: <span class="step-hl">f_n = f(xₙ, yₙ)</span><br>
                    <span class="step-num">02</span> Compute increment: <span class="step-hl">Δy = h · f_n</span><br>
                    <span class="step-num">03</span> Step forward: <span class="step-hl">yₙ₊₁ = yₙ + Δy</span><br>
                    <span class="step-num">04</span> Advance x: <span class="step-hl">xₙ₊₁ = xₙ + h</span><br>
                    <span class="step-num">05</span> Repeat until <span class="step-hl">x ≥ x_end</span>
                </div>
                <div class="algo-props">
                    <div class="algo-prop prop-amber"><span class="prop-dot"></span>Global error O(h) — first-order</div>
                    <div class="algo-prop prop-green"><span class="prop-dot"></span>1 function evaluation per step</div>
                    <div class="algo-prop prop-violet"><span class="prop-dot"></span>Simplest method; reduce h for accuracy</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

        if st.button("Solve — Euler Method", key="run_eu", use_container_width=True, type="primary"):
            # Validate and parse ODE
            func = parse_ode(eu_ode)
            if func is None:
                return
            if eu_xend <= eu_x0:
                st.error("Final x must be strictly greater than x₀.")
                return

            with st.spinner("Computing Euler solution..."):
                x_vals, y_vals, table = euler_method(func, eu_x0, eu_y0, eu_xend, eu_h)

            # Show results: banner, metric cards, table, chart
            _show_results(
                x_vals, y_vals, table,
                method_name="Euler Method",
                h=eu_h, ode_str=eu_ode,
                accent='#22d3ee',
                result_col='yₙ₊₁',
            )
            # Show detailed step-by-step working cards
            _show_euler_steps(table, eu_h, eu_ode)


    # ═════════════════════════════════════════════════════════════════════════
    # TAB 2: MODIFIED EULER METHOD
    # ═════════════════════════════════════════════════════════════════════════
    with tab2:
        st.markdown("""
        <p class="method-sub" style="--accent: var(--violet);">
            Improves on Euler by averaging two slopes: the slope at the start of the step
            and the slope at the predicted endpoint. Second-order accurate — global error
            is O(h²). Also known as the Improved Euler or Euler-Heun method.
        </p>
        """, unsafe_allow_html=True)

        ci, ca = st.columns([1.35, 1], gap="large")

        with ci:
            st.markdown("<div class='ode-lbl'>dy/dx = f(x, y)</div>", unsafe_allow_html=True)
            me_ode = st.text_input(
                "f(x, y) =", value="x + y", key="me_ode",
                placeholder="e.g.  x + y   or   x*y - 2   or   cos(x)*y",
            )

            st.markdown("<div class='ex-lbl'>Quick examples</div>", unsafe_allow_html=True)
            ec = st.columns(4)
            me_examples = ["x + y", "x - y", "x**2 + y", "cos(x)*y"]
            for i, (col, ex) in enumerate(zip(ec, me_examples)):
                if col.button(ex, key=f"me_ex{i}", use_container_width=True):
                    st.session_state["me_ode"] = ex
                    st.rerun()

            st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
            r1, r2 = st.columns(2)
            me_x0   = r1.number_input("Initial x₀", value=0.0, step=0.5, key="me_x0")
            me_y0   = r2.number_input("Initial y₀", value=1.0, step=0.5, key="me_y0")
            r3, r4  = st.columns(2)
            me_xend = r3.number_input("Final x",    value=2.0, step=0.5, key="me_xend")
            me_h    = r4.number_input(
                "Step size h", value=0.2, step=0.05,
                min_value=0.001, format="%.4f", key="me_h",
            )

        with ca:
            st.markdown("""
            <div class="algo-box" style="--accent: var(--violet);">
                <div class="algo-box-bar" style="background: var(--violet);"></div>
                <div class="algo-box-label" style="color: var(--violet);">Modified Euler Algorithm</div>
                <div class="algo-steps">
                    <span class="step-num">01</span> <span class="step-hl">k1 = f(xₙ, yₙ)</span><br>
                    <span class="step-num">02</span> <span class="step-hl">k2 = f(xₙ + h, yₙ + h·k1)</span><br>
                    <span class="step-num">03</span> Avg slope: <span class="step-hl">s = (k1 + k2) / 2</span><br>
                    <span class="step-num">04</span> <span class="step-hl">yₙ₊₁ = yₙ + h · s</span><br>
                    <span class="step-num">05</span> Advance: <span class="step-hl">xₙ₊₁ = xₙ + h</span>
                </div>
                <div class="algo-props">
                    <div class="algo-prop prop-amber"><span class="prop-dot"></span>Global error O(h²) — second-order</div>
                    <div class="algo-prop prop-green"><span class="prop-dot"></span>2 function evaluations per step</div>
                    <div class="algo-prop prop-violet"><span class="prop-dot"></span>Much more accurate than Euler for same h</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

        if st.button("Solve — Modified Euler", key="run_me", use_container_width=True, type="primary"):
            func = parse_ode(me_ode)
            if func is None:
                return
            if me_xend <= me_x0:
                st.error("Final x must be strictly greater than x₀.")
                return

            with st.spinner("Computing Modified Euler solution..."):
                x_vals, y_vals, table = modified_euler(func, me_x0, me_y0, me_xend, me_h)

            _show_results(
                x_vals, y_vals, table,
                method_name="Modified Euler Method",
                h=me_h, ode_str=me_ode,
                accent='#a78bfa',
                result_col='yₙ₊₁',
            )
            _show_modified_euler_steps(table, me_h, me_ode)


    # ═════════════════════════════════════════════════════════════════════════
    # TAB 3: HEUN'S METHOD
    # ═════════════════════════════════════════════════════════════════════════
    with tab3:
        st.markdown("""
        <p class="method-sub" style="--accent: var(--emerald);">
            A predictor-corrector method: first predicts the next value using a simple
            Euler step, then corrects by averaging the slope at the start and the
            predicted endpoint. Second-order accurate (O(h²)) and mathematically
            equivalent to Modified Euler but presented in clearer predictor-corrector form.
        </p>
        """, unsafe_allow_html=True)

        ci, ca = st.columns([1.35, 1], gap="large")

        with ci:
            st.markdown("<div class='ode-lbl'>dy/dx = f(x, y)</div>", unsafe_allow_html=True)
            hn_ode = st.text_input(
                "f(x, y) =", value="x + y", key="hn_ode",
                placeholder="e.g.  x + y   or   x*y - 2   or   exp(x)*y",
            )

            st.markdown("<div class='ex-lbl'>Quick examples</div>", unsafe_allow_html=True)
            ec = st.columns(4)
            hn_examples = ["x + y", "x*y - 1", "exp(x) - y", "x**2 - y"]
            for i, (col, ex) in enumerate(zip(ec, hn_examples)):
                if col.button(ex, key=f"hn_ex{i}", use_container_width=True):
                    st.session_state["hn_ode"] = ex
                    st.rerun()

            st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
            r1, r2 = st.columns(2)
            hn_x0   = r1.number_input("Initial x₀", value=0.0, step=0.5, key="hn_x0")
            hn_y0   = r2.number_input("Initial y₀", value=1.0, step=0.5, key="hn_y0")
            r3, r4  = st.columns(2)
            hn_xend = r3.number_input("Final x",    value=2.0, step=0.5, key="hn_xend")
            hn_h    = r4.number_input(
                "Step size h", value=0.2, step=0.05,
                min_value=0.001, format="%.4f", key="hn_h",
            )

        with ca:
            st.markdown("""
            <div class="algo-box" style="--accent: var(--emerald);">
                <div class="algo-box-bar" style="background: var(--emerald);"></div>
                <div class="algo-box-label" style="color: var(--emerald);">Heun's Algorithm</div>
                <div class="algo-steps">
                    <span class="step-num">01</span> Initial slope: <span class="step-hl">f₀ = f(xₙ, yₙ)</span><br>
                    <span class="step-num">02</span> Predict: <span class="step-hl">y* = yₙ + h · f₀</span><br>
                    <span class="step-num">03</span> End slope: <span class="step-hl">f₁ = f(xₙ₊₁, y*)</span><br>
                    <span class="step-num">04</span> Correct: <span class="step-hl">yₙ₊₁ = yₙ + (h/2)·(f₀ + f₁)</span><br>
                    <span class="step-num">05</span> Advance: <span class="step-hl">xₙ₊₁ = xₙ + h</span>
                </div>
                <div class="algo-props">
                    <div class="algo-prop prop-amber"><span class="prop-dot"></span>Global error O(h²) — second-order</div>
                    <div class="algo-prop prop-green"><span class="prop-dot"></span>Explicit predictor-corrector form</div>
                    <div class="algo-prop prop-violet"><span class="prop-dot"></span>Equivalent to Modified Euler numerically</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

        if st.button("Solve — Heun's Method", key="run_hn", use_container_width=True, type="primary"):
            func = parse_ode(hn_ode)
            if func is None:
                return
            if hn_xend <= hn_x0:
                st.error("Final x must be strictly greater than x₀.")
                return

            with st.spinner("Computing Heun's solution..."):
                x_vals, y_vals, table = heuns_method(func, hn_x0, hn_y0, hn_xend, hn_h)

            _show_results(
                x_vals, y_vals, table,
                method_name="Heun's Method",
                h=hn_h, ode_str=hn_ode,
                accent='#34d399',
                result_col="yₙ₊₁ (Corrected)",
            )
            _show_heun_steps(table, hn_h, hn_ode)

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 4: USER GUIDE
    # ═════════════════════════════════════════════════════════════════════════
    with tab_guide:
        st.markdown("""
        <div style="max-width:820px; margin:0 auto; padding: 1rem 0 2rem;">

        <h2 style="color:#22d3ee; font-family:'Outfit',sans-serif; font-size:1.8rem; margin-bottom:0.3rem;">
            📖 User Guide — How to Enter Equations
        </h2>
        <p style="color:#8b95b0; font-size:0.92rem; margin-bottom:1.8rem;">
            This lab solves first-order ODEs of the form <code style="color:#22d3ee; background:rgba(34,211,238,0.12); padding:2px 7px; border-radius:5px;">dy/dx = f(x, y)</code>.
            Enter only the <strong style="color:#e8ecf4;">right-hand side</strong> — the expression for f(x, y).
        </p>

        <!-- BASIC RULES -->
        <div style="background:rgba(14,20,40,0.7); border:1px solid rgba(34,211,238,0.12); border-radius:14px; padding:1.4rem 1.6rem; margin-bottom:1.4rem;">
            <h3 style="color:#e8ecf4; font-size:1.05rem; margin:0 0 0.9rem;">✅ Basic Rules</h3>
            <ul style="color:#8b95b0; font-size:0.9rem; line-height:2; margin:0; padding-left:1.2rem;">
                <li>Use <code style="color:#22d3ee;">x</code> and <code style="color:#22d3ee;">y</code> as your two variables — nothing else.</li>
                <li>Use <code style="color:#22d3ee;">**</code> for powers: write <code style="color:#22d3ee;">x**2</code> not <code style="color:#a78bfa;">x^2</code></li>
                <li>Multiplication must be explicit: write <code style="color:#22d3ee;">2*x</code> not <code style="color:#a78bfa;">2x</code></li>
                <li>Division uses <code style="color:#22d3ee;">/</code>: write <code style="color:#22d3ee;">x/y</code> normally.</li>
                <li>Parentheses work as expected: <code style="color:#22d3ee;">(x + 1)*(y - 2)</code></li>
            </ul>
        </div>

        <!-- POLYNOMIAL / ALGEBRAIC -->
        <div style="background:rgba(14,20,40,0.7); border:1px solid rgba(34,211,238,0.12); border-radius:14px; padding:1.4rem 1.6rem; margin-bottom:1.4rem;">
            <h3 style="color:#22d3ee; font-size:1.05rem; margin:0 0 0.9rem;">🔢 Polynomial / Algebraic Equations</h3>
            <table style="width:100%; border-collapse:collapse; font-size:0.88rem;">
                <thead>
                    <tr style="color:#4b5574; border-bottom:1px solid rgba(255,255,255,0.06);">
                        <th style="text-align:left; padding:0.4rem 0.8rem;">Math Notation</th>
                        <th style="text-align:left; padding:0.4rem 0.8rem;">Type Here</th>
                        <th style="text-align:left; padding:0.4rem 0.8rem;">Notes</th>
                    </tr>
                </thead>
                <tbody style="color:#8b95b0;">
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                        <td style="padding:0.45rem 0.8rem;">dy/dx = x + y</td>
                        <td style="padding:0.45rem 0.8rem;"><code style="color:#22d3ee;">x + y</code></td>
                        <td style="padding:0.45rem 0.8rem;">Linear, basic</td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                        <td style="padding:0.45rem 0.8rem;">dy/dx = x² − y</td>
                        <td style="padding:0.45rem 0.8rem;"><code style="color:#22d3ee;">x**2 - y</code></td>
                        <td style="padding:0.45rem 0.8rem;">Use ** for power</td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                        <td style="padding:0.45rem 0.8rem;">dy/dx = 1 + (t − y)²</td>
                        <td style="padding:0.45rem 0.8rem;"><code style="color:#22d3ee;">1 + (x - y)**2</code></td>
                        <td style="padding:0.45rem 0.8rem;">Use <code style="color:#22d3ee;">x</code> instead of <code style="color:#a78bfa;">t</code></td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                        <td style="padding:0.45rem 0.8rem;">dy/dx = xy − 2</td>
                        <td style="padding:0.45rem 0.8rem;"><code style="color:#22d3ee;">x*y - 2</code></td>
                        <td style="padding:0.45rem 0.8rem;">Always use * for multiplication</td>
                    </tr>
                    <tr>
                        <td style="padding:0.45rem 0.8rem;">dy/dx = y/x + x³</td>
                        <td style="padding:0.45rem 0.8rem;"><code style="color:#22d3ee;">y/x + x**3</code></td>
                        <td style="padding:0.45rem 0.8rem;">Note: x=0 will cause division by zero</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- TRIGONOMETRIC -->
        <div style="background:rgba(14,20,40,0.7); border:1px solid rgba(167,139,250,0.12); border-radius:14px; padding:1.4rem 1.6rem; margin-bottom:1.4rem;">
            <h3 style="color:#a78bfa; font-size:1.05rem; margin:0 0 0.9rem;">📐 Trigonometric Equations</h3>
            <table style="width:100%; border-collapse:collapse; font-size:0.88rem;">
                <thead>
                    <tr style="color:#4b5574; border-bottom:1px solid rgba(255,255,255,0.06);">
                        <th style="text-align:left; padding:0.4rem 0.8rem;">Math Notation</th>
                        <th style="text-align:left; padding:0.4rem 0.8rem;">Type Here</th>
                    </tr>
                </thead>
                <tbody style="color:#8b95b0;">
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                        <td style="padding:0.45rem 0.8rem;">dy/dx = sin(x) + y</td>
                        <td style="padding:0.45rem 0.8rem;"><code style="color:#a78bfa;">sin(x) + y</code></td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                        <td style="padding:0.45rem 0.8rem;">dy/dx = cos(x) · y</td>
                        <td style="padding:0.45rem 0.8rem;"><code style="color:#a78bfa;">cos(x)*y</code></td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                        <td style="padding:0.45rem 0.8rem;">dy/dx = tan(x) − y²</td>
                        <td style="padding:0.45rem 0.8rem;"><code style="color:#a78bfa;">tan(x) - y**2</code></td>
                    </tr>
                    <tr>
                        <td style="padding:0.45rem 0.8rem;">dy/dx = sin(x·y)</td>
                        <td style="padding:0.45rem 0.8rem;"><code style="color:#a78bfa;">sin(x*y)</code></td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- EXPONENTIAL / LOGARITHMIC -->
        <div style="background:rgba(14,20,40,0.7); border:1px solid rgba(52,211,153,0.12); border-radius:14px; padding:1.4rem 1.6rem; margin-bottom:1.4rem;">
            <h3 style="color:#34d399; font-size:1.05rem; margin:0 0 0.9rem;">📈 Exponential &amp; Logarithmic Equations</h3>
            <table style="width:100%; border-collapse:collapse; font-size:0.88rem;">
                <thead>
                    <tr style="color:#4b5574; border-bottom:1px solid rgba(255,255,255,0.06);">
                        <th style="text-align:left; padding:0.4rem 0.8rem;">Math Notation</th>
                        <th style="text-align:left; padding:0.4rem 0.8rem;">Type Here</th>
                        <th style="text-align:left; padding:0.4rem 0.8rem;">Notes</th>
                    </tr>
                </thead>
                <tbody style="color:#8b95b0;">
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                        <td style="padding:0.45rem 0.8rem;">dy/dx = eˣ − y</td>
                        <td style="padding:0.45rem 0.8rem;"><code style="color:#34d399;">exp(x) - y</code></td>
                        <td style="padding:0.45rem 0.8rem;">Use exp() not e**x</td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                        <td style="padding:0.45rem 0.8rem;">dy/dx = eˣ · y</td>
                        <td style="padding:0.45rem 0.8rem;"><code style="color:#34d399;">exp(x)*y</code></td>
                        <td style="padding:0.45rem 0.8rem;"></td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                        <td style="padding:0.45rem 0.8rem;">dy/dx = ln(x) + y</td>
                        <td style="padding:0.45rem 0.8rem;"><code style="color:#34d399;">log(x) + y</code></td>
                        <td style="padding:0.45rem 0.8rem;">log() = natural log; x must be &gt; 0</td>
                    </tr>
                    <tr>
                        <td style="padding:0.45rem 0.8rem;">dy/dx = e⁻ˣ·y</td>
                        <td style="padding:0.45rem 0.8rem;"><code style="color:#34d399;">exp(-x)*y</code></td>
                        <td style="padding:0.45rem 0.8rem;"></td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- COMMON MISTAKES -->
        <div style="background:rgba(251,113,133,0.06); border:1px solid rgba(251,113,133,0.18); border-radius:14px; padding:1.4rem 1.6rem; margin-bottom:1.4rem;">
            <h3 style="color:#fb7185; font-size:1.05rem; margin:0 0 0.9rem;">⚠️ Common Mistakes to Avoid</h3>
            <table style="width:100%; border-collapse:collapse; font-size:0.88rem;">
                <thead>
                    <tr style="color:#4b5574; border-bottom:1px solid rgba(255,255,255,0.06);">
                        <th style="text-align:left; padding:0.4rem 0.8rem;">❌ Wrong</th>
                        <th style="text-align:left; padding:0.4rem 0.8rem;">✅ Correct</th>
                        <th style="text-align:left; padding:0.4rem 0.8rem;">Reason</th>
                    </tr>
                </thead>
                <tbody style="color:#8b95b0;">
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                        <td style="padding:0.45rem 0.8rem;"><code style="color:#fb7185;">x^2</code></td>
                        <td style="padding:0.45rem 0.8rem;"><code style="color:#34d399;">x**2</code></td>
                        <td style="padding:0.45rem 0.8rem;">^ is XOR in Python, not power</td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                        <td style="padding:0.45rem 0.8rem;"><code style="color:#fb7185;">2x</code></td>
                        <td style="padding:0.45rem 0.8rem;"><code style="color:#34d399;">2*x</code></td>
                        <td style="padding:0.45rem 0.8rem;">Implicit multiplication not allowed</td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                        <td style="padding:0.45rem 0.8rem;"><code style="color:#fb7185;">t + y</code></td>
                        <td style="padding:0.45rem 0.8rem;"><code style="color:#34d399;">x + y</code></td>
                        <td style="padding:0.45rem 0.8rem;">Only x and y are recognized</td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                        <td style="padding:0.45rem 0.8rem;"><code style="color:#fb7185;">e**x</code></td>
                        <td style="padding:0.45rem 0.8rem;"><code style="color:#34d399;">exp(x)</code></td>
                        <td style="padding:0.45rem 0.8rem;">e is not a defined constant; use exp()</td>
                    </tr>
                    <tr>
                        <td style="padding:0.45rem 0.8rem;"><code style="color:#fb7185;">ln(x)</code></td>
                        <td style="padding:0.45rem 0.8rem;"><code style="color:#34d399;">log(x)</code></td>
                        <td style="padding:0.45rem 0.8rem;">Use log() for natural logarithm</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- PARAMETER TIPS -->
        <div style="background:rgba(14,20,40,0.7); border:1px solid rgba(251,191,36,0.15); border-radius:14px; padding:1.4rem 1.6rem;">
            <h3 style="color:#fbbf24; font-size:1.05rem; margin:0 0 0.9rem;">⚙️ Parameter Tips</h3>
            <ul style="color:#8b95b0; font-size:0.9rem; line-height:2.1; margin:0; padding-left:1.2rem;">
                <li><strong style="color:#e8ecf4;">x₀ (Initial x):</strong> Starting point of the integration. Often 0.</li>
                <li><strong style="color:#e8ecf4;">y₀ (Initial y):</strong> Initial condition — the known value of y at x₀. E.g. y(0) = 1 → set y₀ = 1.</li>
                <li><strong style="color:#e8ecf4;">Final x:</strong> Where to stop integration. Must be strictly greater than x₀.</li>
                <li><strong style="color:#e8ecf4;">Step size h:</strong> Smaller h = more accurate but more steps. Start with h = 0.1 or 0.2.</li>
                <li><strong style="color:#e8ecf4;">Which method?</strong> Euler is simplest (O(h) error). Modified Euler &amp; Heun's are more accurate (O(h²)) with only one extra function call per step.</li>
            </ul>
        </div>

        </div>
        """, unsafe_allow_html=True)
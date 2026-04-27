"""
app.py - Main Entry Point
==========================

Run karne :
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

# ── Global CSS Injection ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

/* ── Root Variables ── */
:root {
    --bg:        #0a0e1a;
    --surface:   #111827;
    --surface2:  #1a2236;
    --border:    #1e3a5f;
    --accent:    #00d4ff;
    --accent2:   #7c3aed;
    --accent3:   #f59e0b;
    --text:      #e2e8f0;
    --muted:     #64748b;
    --glow:      0 0 20px rgba(0,212,255,0.3);
}

/* ── Base Reset ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
}

/* ── Animated starfield background ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse at 20% 20%, rgba(124,58,237,0.12) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(0,212,255,0.10) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(245,158,11,0.05) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
    animation: bgPulse 8s ease-in-out infinite alternate;
}

@keyframes bgPulse {
    from { opacity: 0.7; }
    to   { opacity: 1.0; }
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: 4px 0 30px rgba(0,0,0,0.5) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
}

/* Sidebar radio buttons */
[data-testid="stSidebar"] [role="radiogroup"] label {
    display: flex !important;
    align-items: center !important;
    padding: 10px 14px !important;
    margin: 4px 0 !important;
    border-radius: 10px !important;
    border: 1px solid transparent !important;
    transition: all 0.25s ease !important;
    cursor: pointer !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
    color: var(--accent) !important;
    transform: translateX(4px) !important;
}

[data-testid="stSidebar"] [role="radiogroup"] [aria-checked="true"] + label,
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(124,58,237,0.15)) !important;
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    box-shadow: var(--glow) !important;
}

/* ── Main content area ── */
[data-testid="stMain"] {
    background: transparent !important;
}

.block-container {
    padding-top: 2rem !important;
    max-width: 1100px !important;
}

/* ── Headings ── */
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
}

h1 { color: var(--accent) !important; }
h2 { color: var(--text)   !important; }
h3 { color: var(--text)   !important; }

/* ── Streamlit widgets ── */
[data-testid="stSelectbox"] > div,
[data-testid="stNumberInput"] > div,
[data-testid="stTextInput"] > div {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}

/* Slider */
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background: var(--accent) !important;
    box-shadow: var(--glow) !important;
}

/* ── Buttons ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--accent2), var(--accent)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(0,212,255,0.2) !important;
}

[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(0,212,255,0.4) !important;
    filter: brightness(1.1) !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 1rem !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Space Mono', monospace !important;
    color: var(--accent) !important;
}

/* ── DataFrames / Tables ── */
[data-testid="stDataFrame"],
.stDataFrame {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* ── Expanders ── */
[data-testid="stExpander"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

/* ── Dividers ── */
hr {
    border-color: var(--border) !important;
}

/* ── Plotly charts background ── */
.js-plotly-plot .plotly {
    background: transparent !important;
}

/* ── Success / Info / Warning / Error boxes ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border-left-width: 4px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
}

/* ── Code blocks ── */
code, pre {
    font-family: 'Space Mono', monospace !important;
    background: var(--surface2) !important;
    color: var(--accent3) !important;
    border-radius: 8px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover { background: var(--accent2); }

/* ── Floating dots animation ── */
@keyframes float {
    0%, 100% { transform: translateY(0px)  rotate(0deg);   opacity: 0.6; }
    50%       { transform: translateY(-20px) rotate(180deg); opacity: 1;   }
}
</style>
""", unsafe_allow_html=True)

# ── Import all lab modules ────────────────────────────────────────────────────
from labs.lab1_root_finding  import render_lab1
from labs.lab2_interpolation import render_lab2
from labs.lab3_integration   import render_lab3
from labs.lab4_differential  import render_lab4

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 0.5rem;">
        <div style="font-size:2.5rem; margin-bottom:0.3rem;">🔢</div>
        <div style="font-family:'Syne',sans-serif; font-weight:800;
                    font-size:1.1rem; color:#00d4ff; letter-spacing:0.05em;">
            NUMERICAL<br>METHODS
        </div>
        <div style="font-family:'Space Mono',monospace; font-size:0.65rem;
                    color:#64748b; margin-top:0.3rem; letter-spacing:0.1em;">
            SCIENTIFIC PROGRAMMING
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:0.8rem 0;'>", unsafe_allow_html=True)

    lab_options = {
        "🏠  Home"                          : "home",
        "🔍  Lab 1 · Root Finding"          : "lab1",
        "📐  Lab 2 · Interpolation"         : "lab2",
        "∫   Lab 3 · Integration"           : "lab3",
        "📈  Lab 4 · Diff. Equations"       : "lab4",
    }

    selected_label = st.radio("", list(lab_options.keys()), label_visibility="collapsed")
    selected_lab   = lab_options[selected_label]

    st.markdown("<hr style='margin:0.8rem 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Space Mono',monospace; font-size:0.65rem;
                color:#334155; text-align:center; line-height:1.8;">
        v1.0.0 &nbsp;·&nbsp; Streamlit<br>
        Bisection · Newton · Euler
    </div>
    """, unsafe_allow_html=True)

# ── Main Content ──────────────────────────────────────────────────────────────
if selected_lab == "home":

    # Hero section
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(0,212,255,0.08) 0%, rgba(124,58,237,0.08) 100%);
        border: 1px solid #1e3a5f;
        border-radius: 20px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position:absolute; top:-40px; right:-40px;
            width:200px; height:200px;
            background: radial-gradient(circle, rgba(0,212,255,0.15) 0%, transparent 70%);
            border-radius:50%;
        "></div>
        <div style="
            font-family:'Space Mono',monospace;
            font-size:0.75rem;
            color:#00d4ff;
            letter-spacing:0.2em;
            margin-bottom:0.8rem;
        ">◆ WELCOME TO THE LAB</div>
        <h1 style="
            font-family:'Syne',sans-serif;
            font-size:2.8rem;
            font-weight:800;
            color:#e2e8f0;
            line-height:1.1;
            margin:0 0 1rem;
        ">
            Numerical Methods<br>
            <span style="color:#00d4ff;">Web Application</span>
        </h1>
        <p style="
            font-family:'Syne',sans-serif;
            color:#94a3b8;
            font-size:1rem;
            max-width:600px;
            margin:0;
            line-height:1.7;
        ">Four computational labs — interactive algorithms, live graphs, and step-by-step solutions.Select any lab from the sidebar and explore it. </p>
    </div>
    """, unsafe_allow_html=True)

    # Lab cards
    labs_data = [
        {
            "icon": "🔍",
            "num": "Lab 01",
            "title": "Root Finding",
            "methods": ["Bisection Method", "Newton-Raphson", "Secant Method"],
            "color": "#00d4ff",
            "bg": "rgba(0,212,255,0.06)",
        },
        {
            "icon": "📐",
            "num": "Lab 02",
            "title": "Interpolation",
            "methods": ["Lagrange", "Newton Forward", "Newton Divided"],
            "color": "#7c3aed",
            "bg": "rgba(124,58,237,0.08)",
        },
        {
            "icon": "∫",
            "num": "Lab 03",
            "title": "Numerical Integration",
            "methods": ["Trapezoidal Rule", "Simpson's Rule", "Midpoint Rule"],
            "color": "#f59e0b",
            "bg": "rgba(245,158,11,0.07)",
        },
        {
            "icon": "📈",
            "num": "Lab 04",
            "title": "Differential Equations",
            "methods": ["Euler Method", "Modified Euler", "Heun's Method"],
            "color": "#10b981",
            "bg": "rgba(16,185,129,0.07)",
        },
    ]

    cols = st.columns(2, gap="large")
    for i, lab in enumerate(labs_data):
        with cols[i % 2]:
            methods_html = "".join(
                f'<span style="display:inline-block; font-family:Space Mono,monospace; '
                f'font-size:0.7rem; color:{lab["color"]}; background:rgba(255,255,255,0.04); '
                f'border:1px solid {lab["color"]}44; border-radius:20px; '
                f'padding:2px 10px; margin:3px 3px 3px 0;">{m}</span>'
                for m in lab["methods"]
            )
            st.markdown(f"""
            <div style="
                background: {lab['bg']};
                border: 1px solid {lab['color']}33;
                border-radius: 16px;
                padding: 1.5rem;
                margin-bottom: 1.2rem;
                transition: all 0.3s ease;
                cursor: default;
            ">
                <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.8rem;">
                    <div style="font-size:1.8rem;">{lab['icon']}</div>
                    <div>
                        <div style="font-family:'Space Mono',monospace; font-size:0.65rem;
                                    color:{lab['color']}; letter-spacing:0.15em;">{lab['num']}</div>
                        <div style="font-family:'Syne',sans-serif; font-weight:700;
                                    font-size:1.1rem; color:#e2e8f0;">{lab['title']}</div>
                    </div>
                </div>
                <div>{methods_html}</div>
            </div>
            """, unsafe_allow_html=True)

    # Bottom tip
    st.markdown("""
    <div style="
        text-align:center;
        font-family:'Space Mono',monospace;
        font-size:0.75rem;
        color:#334155;
        margin-top:1rem;
        letter-spacing:0.05em;
    ">
         &nbsp; NUMERICAL COMPUTING
    </div>
    """, unsafe_allow_html=True)

elif selected_lab == "lab1":
    render_lab1()

elif selected_lab == "lab2":
    render_lab2()

elif selected_lab == "lab3":
    render_lab3()

elif selected_lab == "lab4":
    render_lab4()
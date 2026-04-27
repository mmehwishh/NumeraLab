"""
app.py - Main Entry Point
==========================
Yeh file poori application ka central hub hai.
Streamlit app yahan se start hota hai.

Kya karta hai:
  - Sidebar navigation banata hai (Lab 1 to 4)
  - User ki selection ke hisaab se sahi lab render karta hai
  - App ka title aur general layout control karta hai

Run karne ke liye:
  streamlit run app.py
"""

import streamlit as st

# ── Page config (sabse pehle call hona chahiye) ──────────────────────────────
st.set_page_config(
    page_title="Numerical Methods Lab",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Import all lab modules ────────────────────────────────────────────────────
from labs.lab1_root_finding  import render_lab1
from labs.lab2_interpolation import render_lab2
from labs.lab3_integration   import render_lab3
from labs.lab4_differential  import render_lab4

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("🔢 Numerical Methods")
st.sidebar.markdown("---")

lab_options = {
    "🏠 Home"                          : "home",
    "🔍 Lab 1: Root Finding"           : "lab1",
    "📐 Lab 2: Interpolation"          : "lab2",
    "∫  Lab 3: Numerical Integration"  : "lab3",
    "📈 Lab 4: Differential Equations" : "lab4",
}

selected_label = st.sidebar.radio("Select a Lab:", list(lab_options.keys()))
selected_lab   = lab_options[selected_label]

st.sidebar.markdown("---")
st.sidebar.caption("Scientific Programming Project")

# ── Main Content ──────────────────────────────────────────────────────────────
if selected_lab == "home":
    st.title("🔢 Numerical Methods Web Application")
    st.markdown("""
    Assalam-o-Alaikum! Is application mein chaar computational labs hain:

    | Lab | Topic | Methods |
    |-----|-------|---------|
    | **Lab 1** | Root Finding | Bisection, Newton-Raphson, Secant |
    | **Lab 2** | Interpolation | Lagrange, Newton Forward, Newton Divided |
    | **Lab 3** | Numerical Integration | Trapezoidal, Simpson's, Midpoint |
    | **Lab 4** | Differential Equations | Euler, Modified Euler, Heun's |

    👈 **Sidebar se koi bhi lab select karo aur shuru karo!**
    """)

elif selected_lab == "lab1":
    render_lab1()

elif selected_lab == "lab2":
    render_lab2()

elif selected_lab == "lab3":
    render_lab3()

elif selected_lab == "lab4":
    render_lab4()

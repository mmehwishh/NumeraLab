"""
lab3_integration.py - Lab 3: Numerical Integration
====================================================
Implements:
  1. Trapezoidal Rule   -> trapezoidal_rule()
  2. Simpson's Rule     -> simpsons_rule()
  3. Midpoint Rule      -> midpoint_rule()
  4. render_lab3()      -> Streamlit UI with area visualizations
"""

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from utils.helpers import parse_function


# ── Shared dark style ─────────────────────────────────────────────────────────
def _apply_dark_style(fig, ax):
    fig.patch.set_facecolor('#111827')
    ax.set_facecolor('#1a2236')
    ax.tick_params(colors='#94a3b8', labelsize=9)
    ax.xaxis.label.set_color('#94a3b8')
    ax.yaxis.label.set_color('#94a3b8')
    ax.title.set_color('#e2e8f0')
    for spine in ax.spines.values():
        spine.set_edgecolor('#1e3a5f')
    ax.grid(True, color='#1e3a5f', linewidth=0.6, linestyle='--', alpha=0.6)


# ─────────────────────────────────────────────
# METHOD 1: TRAPEZOIDAL RULE
# ─────────────────────────────────────────────
def trapezoidal_rule(func, a: float, b: float, n: int):
    """
    Composite Trapezoidal Rule.
    I ≈ (h/2) * [f(a) + 2·Σf(xᵢ) + f(b)]
    """
    h      = (b - a) / n
    x_vals = np.linspace(a, b, n + 1)
    y_vals = np.vectorize(func)(x_vals)

    result = (h / 2) * (y_vals[0] + 2 * np.sum(y_vals[1:-1]) + y_vals[-1])
    return result, x_vals, y_vals


# ─────────────────────────────────────────────
# METHOD 2: SIMPSON'S RULE
# ─────────────────────────────────────────────
def simpsons_rule(func, a: float, b: float, n: int):
    """
    Composite Simpson's 1/3 Rule.
    n must be even.
    I ≈ (h/3) * [f(x₀) + 4f(x₁) + 2f(x₂) + ... + 4f(xₙ₋₁) + f(xₙ)]
    """
    if n % 2 != 0:
        n += 1  # auto-correct to even

    h      = (b - a) / n
    x_vals = np.linspace(a, b, n + 1)
    y_vals = np.vectorize(func)(x_vals)

    # Build coefficient array: 1, 4, 2, 4, 2, ..., 4, 1
    coeffs       = np.ones(n + 1)
    coeffs[1:-1] = np.where(np.arange(1, n) % 2 == 1, 4, 2)

    result = (h / 3) * np.dot(coeffs, y_vals)
    return result, x_vals, y_vals


# ─────────────────────────────────────────────
# METHOD 3: MIDPOINT RULE
# ─────────────────────────────────────────────
def midpoint_rule(func, a: float, b: float, n: int):
    """
    Composite Midpoint Rule.
    I ≈ h · Σf(midpoints)
    """
    h          = (b - a) / n
    mid_points = np.array([a + (i + 0.5) * h for i in range(n)])
    y_vals     = np.vectorize(func)(mid_points)
    result     = h * np.sum(y_vals)
    return result, mid_points, y_vals


# ─────────────────────────────────────────────
# VISUALIZATION
# ─────────────────────────────────────────────
def plot_integration(func, a, b, x_vals, y_vals, method_name, result):
    """
    Two-panel figure:
      Left  — function curve with shaded area + method markers
      Right — bar chart of subinterval contributions
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.8))

    # ── Left: area under curve ────────────────────────────────────────────────
    _apply_dark_style(fig, ax1)

    margin  = abs(b - a) * 0.25
    x_fine  = np.linspace(a - margin, b + margin, 800)
    try:
        y_fine = np.vectorize(func)(x_fine)
    except Exception:
        y_fine = np.zeros_like(x_fine)

    ax1.plot(x_fine, y_fine, color='#00d4ff', linewidth=2.2, label='f(x)', zorder=3)
    ax1.axhline(0, color='#475569', linewidth=0.8)

    # Shade the integration region
    x_shade = np.linspace(a, b, 600)
    try:
        y_shade = np.vectorize(func)(x_shade)
    except Exception:
        y_shade = np.zeros_like(x_shade)
    ax1.fill_between(x_shade, y_shade, 0, alpha=0.25, color='#7c3aed', label='Area')

    # Method-specific overlay
    if 'Trapezoidal' in method_name:
        for i in range(len(x_vals) - 1):
            xs = [x_vals[i], x_vals[i], x_vals[i+1], x_vals[i+1]]
            ys = [0, y_vals[i], y_vals[i+1], 0]
            ax1.fill(xs, ys, alpha=0.18, color='#f59e0b', edgecolor='#f59e0b',
                     linewidth=0.8)

    elif "Simpson" in method_name:
        for i in range(len(x_vals) - 1):
            xs = [x_vals[i], x_vals[i], x_vals[i+1], x_vals[i+1]]
            ys = [0, y_vals[i], y_vals[i+1], 0]
            ax1.fill(xs, ys, alpha=0.18, color='#7c3aed', edgecolor='#a78bfa',
                     linewidth=0.8)

    elif "Midpoint" in method_name:
        # Draw midpoint rectangles
        n = len(x_vals)
        h = (b - a) / n
        for i, (mx, my) in enumerate(zip(x_vals, y_vals)):
            rect_x = mx - h / 2
            rect = plt.Rectangle((rect_x, 0), h, my,
                                  color='#10b981', alpha=0.22,
                                  edgecolor='#34d399', linewidth=0.8)
            ax1.add_patch(rect)
        ax1.scatter(x_vals, y_vals, color='#f59e0b', s=45, zorder=5, label='Midpoints')

    ax1.set_title(f'{method_name}\nResult ≈ {result:.8f}',
                  fontsize=10, fontweight='bold', pad=8)
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.legend(facecolor='#1a2236', edgecolor='#1e3a5f',
               labelcolor='#e2e8f0', fontsize=9)

    # ── Right: subinterval contribution bar chart ─────────────────────────────
    _apply_dark_style(fig, ax2)

    if 'Midpoint' in method_name:
        n      = len(x_vals)
        h_val  = (b - a) / n
        widths = np.full(n, h_val)
        contribs = np.abs(y_vals) * h_val
        colors   = ['#10b981' if v >= 0 else '#ef4444' for v in y_vals]
    else:
        n        = len(x_vals) - 1
        contribs = []
        colors   = []
        for i in range(n):
            seg = abs(y_vals[i] + y_vals[i+1]) / 2 * abs(x_vals[i+1] - x_vals[i])
            contribs.append(seg)
            colors.append('#7c3aed' if y_vals[i] >= 0 else '#ef4444')

    bar_x = np.arange(len(contribs))
    bars  = ax2.bar(bar_x, contribs, color=colors, edgecolor='#1e3a5f',
                    linewidth=0.6, alpha=0.85)

    # Highlight max bar
    if len(contribs):
        max_idx = int(np.argmax(contribs))
        bars[max_idx].set_edgecolor('#f59e0b')
        bars[max_idx].set_linewidth(1.8)

    ax2.set_title('Subinterval Contributions', fontsize=10, fontweight='bold', pad=8)
    ax2.set_xlabel('Subinterval index')
    ax2.set_ylabel('|Contribution|')

    # Cumulative line
    cumsum = np.cumsum(contribs)
    ax2_r  = ax2.twinx()
    ax2_r.plot(bar_x, cumsum, color='#00d4ff', linewidth=1.8,
               marker='o', markersize=4, label='Cumulative')
    ax2_r.set_ylabel('Cumulative sum', color='#00d4ff')
    ax2_r.tick_params(colors='#00d4ff', labelsize=8)
    ax2_r.spines['right'].set_edgecolor('#00d4ff')

    plt.tight_layout(pad=2)
    return fig


def plot_comparison(func, a, b, n_max=50):
    """
    Show how all three methods converge as n increases.
    """
    n_vals = list(range(2, n_max + 1, 2))
    trap_vals, simp_vals, mid_vals = [], [], []

    for n in n_vals:
        try:
            trap_vals.append(trapezoidal_rule(func, a, b, n)[0])
            simp_vals.append(simpsons_rule(func, a, b, n)[0])
            mid_vals.append(midpoint_rule(func, a, b, n)[0])
        except Exception:
            trap_vals.append(np.nan)
            simp_vals.append(np.nan)
            mid_vals.append(np.nan)

    fig, ax = plt.subplots(figsize=(11, 4))
    _apply_dark_style(fig, ax)

    ax.plot(n_vals, trap_vals, color='#f59e0b', linewidth=2,
            marker='o', markersize=4, label='Trapezoidal')
    ax.plot(n_vals, simp_vals, color='#7c3aed', linewidth=2,
            marker='s', markersize=4, label="Simpson's")
    ax.plot(n_vals, mid_vals,  color='#10b981', linewidth=2,
            marker='^', markersize=4, label='Midpoint')

    ax.set_title('Convergence Comparison — All Three Methods vs n', fontsize=11,
                 fontweight='bold', pad=10)
    ax.set_xlabel('Number of subintervals (n)')
    ax.set_ylabel('Approximate integral value')
    ax.legend(facecolor='#1a2236', edgecolor='#1e3a5f',
              labelcolor='#e2e8f0', fontsize=9)
    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────
# STREAMLIT UI
# ─────────────────────────────────────────────
def render_lab3():
    # ── Header ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(245,158,11,.08),rgba(124,58,237,.08));
                border:1px solid #1e3a5f; border-radius:16px; padding:1.6rem 2rem; margin-bottom:1.5rem;">
        <div style="font-family:'Space Mono',monospace;font-size:.7rem;color:#f59e0b;
                    letter-spacing:.2em;margin-bottom:.4rem;">◆ LAB 03</div>
        <h2 style="font-family:'Syne',sans-serif;font-weight:800;color:#e2e8f0;margin:0 0 .5rem;">
            ∫ Numerical Integration
        </h2>
        <p style="color:#64748b;margin:0;font-size:.9rem;">
            Definite integral <code style="color:#f59e0b;">∫ f(x) dx</code> ka approximate value nikalo —
            Trapezoidal · Simpson's · Midpoint
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Global inputs ─────────────────────────────────────────────────────────
    st.markdown("#### ⚙️ Common Settings")
    col1, col2, col3, col4 = st.columns(4)
    func_str = col1.text_input("f(x) =", value="x**2",
                                help="Examples: sin(x), exp(-x), x**3 + 2*x")
    a_val    = col2.number_input("Lower limit a", value=0.0)
    b_val    = col3.number_input("Upper limit b", value=1.0)
    n_val    = col4.number_input("Subintervals n", value=10, min_value=2, step=2)

    st.markdown("<hr style='border-color:#1e3a5f;margin:1rem 0;'>", unsafe_allow_html=True)

    # ── Tabs ─────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📏  Trapezoidal", "〜  Simpson's 1/3", "⬛  Midpoint", "📊  Comparison"])

    # ════════════════════════════════════════════════════════════════════════
    # TAB 1 — TRAPEZOIDAL
    # ════════════════════════════════════════════════════════════════════════
    with tab1:
        col1, col2 = st.columns([1.3, 1])
        with col1:
            st.markdown("##### Connects points with straight-line trapezoids")
            st.markdown("""
            <div style="background:#111827;border:1px solid #1e3a5f;border-radius:12px;
                        padding:1rem 1.2rem;font-family:'Space Mono',monospace;font-size:.78rem;
                        color:#94a3b8;line-height:2;">
            <span style="color:#f59e0b;">Formula:</span><br>
            I ≈ (h/2)·[f(x₀) + 2f(x₁) + ... + 2f(xₙ₋₁) + f(xₙ)]<br>
            <span style="color:#f59e0b;">Error Order:</span> O(h²)
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("##### Quick info")
            st.info("Works for any continuous function. Error decreases quadratically with n.")

        if st.button("▶  Run Trapezoidal", key="run_trap", use_container_width=True):
            func, err = parse_function(func_str)
            if err:
                st.error(f"Function parse error: {err}")
            elif a_val >= b_val:
                st.error("b > a hona chahiye!")
            else:
                result, x_vals, y_vals = trapezoidal_rule(func, a_val, b_val, int(n_val))

                m1, m2, m3 = st.columns(3)
                m1.metric("∫ Result", f"{result:.8f}")
                m2.metric("Subintervals n", int(n_val))
                m3.metric("Step size h", f"{(b_val-a_val)/n_val:.6f}")

                st.markdown("#### 📊 Visualization")
                fig = plot_integration(func, a_val, b_val, x_vals, y_vals,
                                       "Trapezoidal Rule", result)
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)

                with st.expander("📋 x and y values"):
                    import pandas as pd
                    df = pd.DataFrame({'x': x_vals, 'f(x)': y_vals})
                    df.index += 1
                    st.dataframe(df.style.format({'x': '{:.6f}', 'f(x)': '{:.6f}'}),
                                 use_container_width=True)

    # ════════════════════════════════════════════════════════════════════════
    # TAB 2 — SIMPSON'S
    # ════════════════════════════════════════════════════════════════════════
    with tab2:
        col1, col2 = st.columns([1.3, 1])
        with col1:
            st.markdown("##### Parabolic arcs — higher order accuracy")
            st.markdown("""
            <div style="background:#111827;border:1px solid #1e3a5f;border-radius:12px;
                        padding:1rem 1.2rem;font-family:'Space Mono',monospace;font-size:.78rem;
                        color:#94a3b8;line-height:2;">
            <span style="color:#7c3aed;">Formula:</span><br>
            I ≈ (h/3)·[f(x₀)+4f(x₁)+2f(x₂)+4f(x₃)+…+f(xₙ)]<br>
            <span style="color:#7c3aed;">Error Order:</span> O(h⁴) — very accurate!<br>
            <span style="color:#f59e0b;">Note:</span> n even hona chahiye
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("##### Quick info")
            st.warning("Agar n odd diya to automatically even ho jata hai.")

        if st.button("▶  Run Simpson's", key="run_simp", use_container_width=True):
            func, err = parse_function(func_str)
            if err:
                st.error(f"Function parse error: {err}")
            elif a_val >= b_val:
                st.error("b > a hona chahiye!")
            else:
                n_use = int(n_val) if int(n_val) % 2 == 0 else int(n_val) + 1
                if n_use != int(n_val):
                    st.warning(f"n={int(n_val)} odd tha — auto-corrected to n={n_use}")

                result, x_vals, y_vals = simpsons_rule(func, a_val, b_val, n_use)

                m1, m2, m3 = st.columns(3)
                m1.metric("∫ Result", f"{result:.8f}")
                m2.metric("Subintervals n", n_use)
                m3.metric("Step size h", f"{(b_val-a_val)/n_use:.6f}")

                st.markdown("#### 📊 Visualization")
                fig = plot_integration(func, a_val, b_val, x_vals, y_vals,
                                       "Simpson's 1/3 Rule", result)
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)

                with st.expander("📋 x and y values"):
                    import pandas as pd
                    coeffs       = np.ones(n_use + 1)
                    coeffs[1:-1] = np.where(np.arange(1, n_use) % 2 == 1, 4, 2)
                    df = pd.DataFrame({
                        'x':       x_vals,
                        'f(x)':    y_vals,
                        'Coeff':   coeffs.astype(int),
                    })
                    df.index += 1
                    st.dataframe(df.style.format({'x': '{:.6f}', 'f(x)': '{:.6f}'}),
                                 use_container_width=True)

    # ════════════════════════════════════════════════════════════════════════
    # TAB 3 — MIDPOINT
    # ════════════════════════════════════════════════════════════════════════
    with tab3:
        col1, col2 = st.columns([1.3, 1])
        with col1:
            st.markdown("##### Rectangle at midpoint of each subinterval")
            st.markdown("""
            <div style="background:#111827;border:1px solid #1e3a5f;border-radius:12px;
                        padding:1rem 1.2rem;font-family:'Space Mono',monospace;font-size:.78rem;
                        color:#94a3b8;line-height:2;">
            <span style="color:#10b981;">Formula:</span><br>
            mᵢ = a + (i + ½)·h<br>
            I ≈ h · Σ f(mᵢ)<br>
            <span style="color:#10b981;">Error Order:</span> O(h²) — often better than trapezoidal
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.success("Simpler to implement, surprisingly accurate for smooth functions.")

        if st.button("▶  Run Midpoint", key="run_mid", use_container_width=True):
            func, err = parse_function(func_str)
            if err:
                st.error(f"Function parse error: {err}")
            elif a_val >= b_val:
                st.error("b > a hona chahiye!")
            else:
                result, mid_pts, y_vals = midpoint_rule(func, a_val, b_val, int(n_val))

                m1, m2, m3 = st.columns(3)
                m1.metric("∫ Result", f"{result:.8f}")
                m2.metric("Subintervals n", int(n_val))
                m3.metric("Step size h", f"{(b_val-a_val)/n_val:.6f}")

                st.markdown("#### 📊 Visualization")
                fig = plot_integration(func, a_val, b_val, mid_pts, y_vals,
                                       "Midpoint Rule", result)
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)

                with st.expander("📋 Midpoints and values"):
                    import pandas as pd
                    df = pd.DataFrame({'Midpoint x': mid_pts, 'f(midpoint)': y_vals})
                    df.index += 1
                    st.dataframe(df.style.format('{:.8f}'), use_container_width=True)

    # ════════════════════════════════════════════════════════════════════════
    # TAB 4 — COMPARISON
    # ════════════════════════════════════════════════════════════════════════
    with tab4:
        st.markdown("##### Teeno methods ki accuracy compare karo jaise n barhta hai")

        c1, c2 = st.columns(2)
        n_max_cmp = c1.slider("Max n for comparison", 4, 100, 40, step=2)

        if st.button("▶  Run Comparison", key="run_cmp", use_container_width=True):
            func, err = parse_function(func_str)
            if err:
                st.error(f"Function parse error: {err}")
            elif a_val >= b_val:
                st.error("b > a hona chahiye!")
            else:
                # Results at current n
                r_trap, _, _ = trapezoidal_rule(func, a_val, b_val, int(n_val))
                r_simp, _, _ = simpsons_rule(func, a_val, b_val,
                                             int(n_val) if int(n_val)%2==0 else int(n_val)+1)
                r_mid,  _, _ = midpoint_rule(func, a_val, b_val, int(n_val))

                m1, m2, m3 = st.columns(3)
                m1.metric("Trapezoidal", f"{r_trap:.8f}")
                m2.metric("Simpson's",  f"{r_simp:.8f}")
                m3.metric("Midpoint",   f"{r_mid:.8f}")

                st.markdown("#### 📊 Convergence as n increases")
                fig = plot_comparison(func, a_val, b_val, n_max=n_max_cmp)
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)

                # Summary table
                import pandas as pd
                n_list   = list(range(2, min(n_max_cmp, 20) + 1, 2))
                rows     = []
                for nn in n_list:
                    t, _, _  = trapezoidal_rule(func, a_val, b_val, nn)
                    nn_even  = nn if nn % 2 == 0 else nn + 1
                    s, _, _  = simpsons_rule(func, a_val, b_val, nn_even)
                    m2_, _, _ = midpoint_rule(func, a_val, b_val, nn)
                    rows.append({'n': nn, 'Trapezoidal': t,
                                 "Simpson's": s, 'Midpoint': m2_})

                df = pd.DataFrame(rows).set_index('n')
                st.markdown("#### 📋 Value Table (first 10 even n)")
                st.dataframe(df.style.format('{:.8f}'), use_container_width=True)
"""
lab1_root_finding.py - Lab 1: Root Finding Methods
====================================================
Implements:
  1. Bisection Method       -> bisection()
  2. Newton-Raphson Method  -> newton_raphson()
  3. Secant Method          -> secant()
  4. render_lab1()          -> Streamlit UI
"""

import numpy as np
import sympy as sp
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from utils.helpers import parse_function, display_iteration_table, plot_function


# ── Shared plot style ─────────────────────────────────────────────────────────
def _apply_dark_style(fig, ax):
    fig.patch.set_facecolor('#111827')
    ax.set_facecolor('#1a2236')
    ax.tick_params(colors='#94a3b8', labelsize=9)
    ax.xaxis.label.set_color('#94a3b8')
    ax.yaxis.label.set_color('#94a3b8')
    ax.title.set_color('#e2e8f0')
    for spine in ax.spines.values():
        spine.set_edgecolor('#1e3a5f')
    ax.grid(True, color='#1e3a5f', linewidth=0.6, linestyle='--', alpha=0.7)


# ─────────────────────────────────────────────
# METHOD 1: BISECTION
# ─────────────────────────────────────────────
def bisection(func, a: float, b: float, tol: float = 1e-6, max_iter: int = 100):
    f_a = func(a)
    f_b = func(b)

    if f_a * f_b >= 0:
        return None, [], "Error: f(a) aur f(b) ke signs opposite hone chahiye (Bolzano's Theorem)."

    iterations = []
    message = "Maximum iterations reached without convergence."
    c = a

    for i in range(max_iter):
        c     = (a + b) / 2
        f_c   = func(c)
        error = abs(b - a) / 2

        iterations.append({
            'Iteration': i + 1,
            'a':         round(a,   8),
            'b':         round(b,   8),
            'c (midpoint)': round(c, 8),
            'f(c)':      round(f_c, 8),
            'Error':     round(error, 8),
        })

        if abs(f_c) < tol or error < tol:
            message = f"✅ Root mil gaya! {i+1} iterations mein converge hua."
            break

        if f_a * f_c < 0:
            b   = c
            f_b = f_c
        else:
            a   = c
            f_a = f_c

    return c, iterations, message


# ─────────────────────────────────────────────
# METHOD 2: NEWTON-RAPHSON
# ─────────────────────────────────────────────
def newton_raphson(func, func_derivative, x0: float, tol: float = 1e-6, max_iter: int = 100):
    iterations = []
    message    = "Maximum iterations reached without convergence."
    x1         = x0

    for i in range(max_iter):
        f_val      = func(x0)
        f_prime    = func_derivative(x0)

        if abs(f_prime) < 1e-14:
            return None, iterations, "Error: Derivative zero ho gaya — division by zero!"

        x1    = x0 - f_val / f_prime
        error = abs(x1 - x0)

        iterations.append({
            'Iteration': i + 1,
            'x0':        round(x0,      8),
            'f(x0)':     round(f_val,   8),
            "f'(x0)":    round(f_prime, 8),
            'x1':        round(x1,      8),
            'Error':     round(error,   8),
        })

        if error < tol:
            message = f"✅ Root mil gaya! {i+1} iterations mein converge hua."
            break

        x0 = x1

    return x1, iterations, message


# ─────────────────────────────────────────────
# METHOD 3: SECANT
# ─────────────────────────────────────────────
def secant(func, x0: float, x1: float, tol: float = 1e-6, max_iter: int = 100):
    iterations = []
    message    = "Maximum iterations reached without convergence."
    x2         = x1

    for i in range(max_iter):
        f0 = func(x0)
        f1 = func(x1)
        denom = f1 - f0

        if abs(denom) < 1e-14:
            return None, iterations, "Error: f(x1) - f(x0) = 0, division by zero!"

        x2    = x1 - f1 * (x1 - x0) / denom
        error = abs(x2 - x1)

        iterations.append({
            'Iteration': i + 1,
            'x0':        round(x0,       8),
            'x1':        round(x1,       8),
            'x2':        round(x2,       8),
            'f(x2)':     round(func(x2), 8),
            'Error':     round(error,    8),
        })

        if error < tol:
            message = f"✅ Root mil gaya! {i+1} iterations mein converge hua."
            break

        x0, x1 = x1, x2

    return x2, iterations, message


# ─────────────────────────────────────────────
# PLOTS
# ─────────────────────────────────────────────
def plot_root(func, root, a, b, method_name, iterations):
    """Plot function with root marker and convergence graph side by side."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5))

    # ── Left: function curve ──────────────────────────────────────────────────
    margin  = abs(b - a) * 0.4
    x_min   = min(a, b) - margin
    x_max   = max(a, b) + margin
    x_range = np.linspace(x_min, x_max, 600)

    try:
        y_range = np.vectorize(func)(x_range)
    except Exception:
        y_range = np.zeros_like(x_range)

    _apply_dark_style(fig, ax1)
    ax1.plot(x_range, y_range, color='#00d4ff', linewidth=2.2, label='f(x)')
    ax1.axhline(0, color='#64748b', linewidth=0.8, linestyle='-')
    ax1.axvline(0, color='#64748b', linewidth=0.8, linestyle='-')

    if root is not None:
        ax1.scatter([root], [func(root)], color='#f59e0b', s=120, zorder=5,
                    label=f'Root ≈ {root:.6f}')
        ax1.axvline(root, color='#f59e0b', linewidth=1.2, linestyle='--', alpha=0.6)

    # shade zero crossing area
    try:
        ax1.fill_between(x_range, y_range, 0,
                         where=(np.abs(y_range) < max(np.abs(y_range)) * 0.15),
                         alpha=0.15, color='#7c3aed')
    except Exception:
        pass

    ax1.set_title(f'{method_name} — f(x) Curve', fontsize=11, fontweight='bold', pad=10)
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.legend(facecolor='#1a2236', edgecolor='#1e3a5f',
               labelcolor='#e2e8f0', fontsize=9)

    # ── Right: convergence (error per iteration) ──────────────────────────────
    _apply_dark_style(fig, ax2)
    if iterations:
        errors = [it['Error'] for it in iterations]
        iters  = [it['Iteration'] for it in iterations]
        ax2.semilogy(iters, errors, color='#7c3aed', linewidth=2, marker='o',
                     markersize=5, markerfacecolor='#f59e0b', markeredgewidth=0)
        ax2.fill_between(iters, errors, alpha=0.15, color='#7c3aed')
        ax2.set_title('Convergence — Error per Iteration', fontsize=11,
                      fontweight='bold', pad=10)
        ax2.set_xlabel('Iteration #')
        ax2.set_ylabel('Error (log scale)')

    plt.tight_layout(pad=2)
    return fig


# ─────────────────────────────────────────────
# STREAMLIT UI
# ─────────────────────────────────────────────
def render_lab1():
    # ── Header ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(0,212,255,.09),rgba(124,58,237,.09));
                border:1px solid #1e3a5f; border-radius:16px; padding:1.6rem 2rem; margin-bottom:1.5rem;">
        <div style="font-family:'Space Mono',monospace;font-size:.7rem;color:#00d4ff;
                    letter-spacing:.2em;margin-bottom:.4rem;">◆ LAB 01</div>
        <h2 style="font-family:'Syne',sans-serif;font-weight:800;color:#e2e8f0;margin:0 0 .5rem;">
            🔍 Root Finding Methods
        </h2>
        <p style="color:#64748b;margin:0;font-size:.9rem;">
            Nonlinear equation <code style="color:#00d4ff;">f(x) = 0</code> ka root dhundho —
            Bisection · Newton-Raphson · Secant
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Method selector tabs ──────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(
        ["🔀  Bisection", "📉  Newton-Raphson", "📏  Secant"])

    # ════════════════════════════════════════════════════════════════════════
    # TAB 1 — BISECTION
    # ════════════════════════════════════════════════════════════════════════
    with tab1:
        st.markdown("##### Interval halving — guaranteed convergence if sign change exists")
        col1, col2 = st.columns([1.2, 1])

        with col1:
            func_str_b = st.text_input(
                "f(x) =", value="x**3 - x - 2",
                key="b_func", help="Python/numpy syntax. Example: x**3 - 2*x - 5")
            c1, c2 = st.columns(2)
            a_b = c1.number_input("Left bound a", value=1.0, key="b_a")
            b_b = c2.number_input("Right bound b", value=2.0, key="b_b")
            c3, c4 = st.columns(2)
            tol_b  = c3.number_input("Tolerance", value=1e-6, format="%.2e", key="b_tol")
            mi_b   = c4.number_input("Max iterations", value=50, min_value=1, key="b_mi")

        with col2:
            st.markdown("""
            <div style="background:#111827;border:1px solid #1e3a5f;border-radius:12px;
                        padding:1rem 1.2rem;font-family:'Space Mono',monospace;font-size:.78rem;
                        color:#94a3b8;line-height:2;">
            <span style="color:#00d4ff;">Algorithm:</span><br>
            1. c = (a + b) / 2<br>
            2. if f(a)·f(c) &lt; 0 → b = c<br>
            3. else → a = c<br>
            4. repeat until |b−a| &lt; tol
            </div>
            """, unsafe_allow_html=True)

        if st.button("▶  Run Bisection", key="run_b", use_container_width=True):
            func, err = parse_function(func_str_b)
            if err:
                st.error(f"Function parse error: {err}")
            else:
                root, iters, msg = bisection(func, a_b, b_b, tol_b, int(mi_b))
                if root is None:
                    st.error(msg)
                else:
                    st.success(msg)
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Root found", f"{root:.8f}")
                    m2.metric("Iterations", len(iters))
                    m3.metric("Final error", f"{iters[-1]['Error']:.2e}")

                    st.markdown("#### 📊 Convergence Graph")
                    fig = plot_root(func, root, a_b, b_b, "Bisection", iters)
                    st.pyplot(fig, use_container_width=True)
                    plt.close(fig)

                    with st.expander("📋 Iteration Table"):
                        display_iteration_table(iters)

    # ════════════════════════════════════════════════════════════════════════
    # TAB 2 — NEWTON-RAPHSON
    # ════════════════════════════════════════════════════════════════════════
    with tab2:
        st.markdown("##### Tangent line method — quadratic convergence near root")
        col1, col2 = st.columns([1.2, 1])

        with col1:
            func_str_n = st.text_input(
                "f(x) =", value="x**3 - x - 2",
                key="n_func")
            x0_n   = st.number_input("Initial guess x₀", value=1.5, key="n_x0")
            c3, c4 = st.columns(2)
            tol_n  = c3.number_input("Tolerance", value=1e-6, format="%.2e", key="n_tol")
            mi_n   = c4.number_input("Max iterations", value=50, min_value=1, key="n_mi")

        with col2:
            st.markdown("""
            <div style="background:#111827;border:1px solid #1e3a5f;border-radius:12px;
                        padding:1rem 1.2rem;font-family:'Space Mono',monospace;font-size:.78rem;
                        color:#94a3b8;line-height:2;">
            <span style="color:#7c3aed;">Algorithm:</span><br>
            x₁ = x₀ − f(x₀) / f'(x₀)<br>
            until |x₁ − x₀| &lt; tol<br><br>
            <span style="color:#f59e0b;">Note:</span> derivative auto-computed<br>
            via SymPy symbolic diff
            </div>
            """, unsafe_allow_html=True)

        if st.button("▶  Run Newton-Raphson", key="run_n", use_container_width=True):
            func, err = parse_function(func_str_n)
            if err:
                st.error(f"Function parse error: {err}")
            else:
                # Auto-derive using sympy
                try:
                    x_sym    = sp.Symbol('x')
                    expr     = sp.sympify(func_str_n)
                    deriv    = sp.diff(expr, x_sym)
                    func_d   = sp.lambdify(x_sym, deriv, modules=['numpy'])
                    st.info(f"f'(x) = `{sp.simplify(deriv)}`  (SymPy se auto-compute hua)")
                except Exception as e:
                    st.error(f"Derivative compute nahi hua: {e}")
                    st.stop()

                root, iters, msg = newton_raphson(func, func_d, x0_n, tol_n, int(mi_n))
                if root is None:
                    st.error(msg)
                else:
                    st.success(msg)
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Root found", f"{root:.8f}")
                    m2.metric("Iterations", len(iters))
                    m3.metric("Final error", f"{iters[-1]['Error']:.2e}")

                    st.markdown("#### 📊 Convergence Graph")
                    a_plot = x0_n - 2
                    b_plot = x0_n + 2
                    fig = plot_root(func, root, a_plot, b_plot, "Newton-Raphson", iters)
                    st.pyplot(fig, use_container_width=True)
                    plt.close(fig)

                    with st.expander("📋 Iteration Table"):
                        display_iteration_table(iters)

    # ════════════════════════════════════════════════════════════════════════
    # TAB 3 — SECANT
    # ════════════════════════════════════════════════════════════════════════
    with tab3:
        st.markdown("##### Finite-difference approximation — no derivative needed")
        col1, col2 = st.columns([1.2, 1])

        with col1:
            func_str_s = st.text_input(
                "f(x) =", value="x**3 - x - 2",
                key="s_func")
            c1, c2 = st.columns(2)
            x0_s   = c1.number_input("First guess x₀", value=1.0, key="s_x0")
            x1_s   = c2.number_input("Second guess x₁", value=2.0, key="s_x1")
            c3, c4 = st.columns(2)
            tol_s  = c3.number_input("Tolerance", value=1e-6, format="%.2e", key="s_tol")
            mi_s   = c4.number_input("Max iterations", value=50, min_value=1, key="s_mi")

        with col2:
            st.markdown("""
            <div style="background:#111827;border:1px solid #1e3a5f;border-radius:12px;
                        padding:1rem 1.2rem;font-family:'Space Mono',monospace;font-size:.78rem;
                        color:#94a3b8;line-height:2;">
            <span style="color:#10b981;">Algorithm:</span><br>
            x₂ = x₁ − f(x₁)·(x₁−x₀)<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/ (f(x₁) − f(x₀))<br>
            until |x₂ − x₁| &lt; tol<br><br>
            <span style="color:#f59e0b;">Advantage:</span> derivative-free
            </div>
            """, unsafe_allow_html=True)

        if st.button("▶  Run Secant", key="run_s", use_container_width=True):
            func, err = parse_function(func_str_s)
            if err:
                st.error(f"Function parse error: {err}")
            else:
                root, iters, msg = secant(func, x0_s, x1_s, tol_s, int(mi_s))
                if root is None:
                    st.error(msg)
                else:
                    st.success(msg)
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Root found", f"{root:.8f}")
                    m2.metric("Iterations", len(iters))
                    m3.metric("Final error", f"{iters[-1]['Error']:.2e}")

                    st.markdown("#### 📊 Convergence Graph")
                    a_plot = min(x0_s, x1_s) - 1
                    b_plot = max(x0_s, x1_s) + 1
                    fig = plot_root(func, root, a_plot, b_plot, "Secant", iters)
                    st.pyplot(fig, use_container_width=True)
                    plt.close(fig)

                    with st.expander("📋 Iteration Table"):
                        display_iteration_table(iters)


# ── standalone test ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    f = lambda x: x**3 - x - 2
    root, logs, msg = bisection(f, 1, 2)
    print(msg, "| Root:", root)
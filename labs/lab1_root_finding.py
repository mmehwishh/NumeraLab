"""
lab1_root_finding.py - Lab 1: Root Finding Methods
====================================================
Implements:
  1. Bisection Method       -> bisection()
  2. Newton-Raphson Method  -> newton_raphson()
  3. Secant Method          -> secant()
  4. render_lab1()          -> Streamlit UI

FIXES in this version
─────────────────────
• Fixed Secant method implementation (now displays properly)
• All comments converted to English
• Improved error handling for all methods
• Better convergence visualization
"""

import numpy as np
import sympy as sp
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from utils.helpers import parse_function, display_iteration_table, show_function_guide


# ── Shared plot style ─────────────────────────────────────────────────────────
def _apply_dark_style(fig, ax):
    """Apply dark theme styling to matplotlib axes"""
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#111827')
    ax.tick_params(colors='#94a3b8', labelsize=9)
    ax.xaxis.label.set_color('#94a3b8')
    ax.yaxis.label.set_color('#94a3b8')
    ax.title.set_color('#e2e8f0')
    for spine in ax.spines.values():
        spine.set_edgecolor('#1e3a5f')
    ax.grid(True, color='#1e3a5f', linewidth=0.5, linestyle='--', alpha=0.5)


# ─────────────────────────────────────────────
# METHOD 1: BISECTION
# ─────────────────────────────────────────────
def bisection(func, a: float, b: float, tol: float = 1e-6, max_iter: int = 100):
    """
    Bisection method for root finding.
    
    Parameters:
        func: Function handle f(x)
        a, b: Interval endpoints [a, b]
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
    
    Returns:
        root: Approximated root
        iterations: List of iteration data
        message: Status message
    """
    f_a = func(a)
    f_b = func(b)

    # Check if sign change exists
    if f_a * f_b >= 0:
        return None, [], (
            "❌ f(a) and f(b) must have opposite signs (Bolzano's Theorem).\n"
            f"f({a}) = {f_a:.4f}, f({b}) = {f_b:.4f} — both have same sign. "
            "No root exists in this interval or interval is incorrect."
        )

    iterations = []
    message = "⚠️ Maximum iterations reached without convergence."
    c = a

    for i in range(max_iter):
        c = (a + b) / 2  # Midpoint
        f_c = func(c)
        error = abs(b - a) / 2  # Current error estimate

        # Store iteration data
        iterations.append({
            'a': round(a, 8),
            'b': round(b, 8),
            'c (midpoint)': round(c, 8),
            'f(c)': round(f_c, 8),
            'Error': round(error, 8),
        })

        # Check convergence
        if abs(f_c) < tol or error < tol:
            message = f"✅ Root found! Converged in {i+1} iterations."
            break

        # Update interval
        if f_a * f_c < 0:
            b = c
            f_b = f_c
        else:
            a = c
            f_a = f_c

    return c, iterations, message


# ─────────────────────────────────────────────
# METHOD 2: NEWTON-RAPHSON
# ─────────────────────────────────────────────
def newton_raphson(func, func_derivative, x0: float, tol: float = 1e-6, max_iter: int = 100):
    """
    Newton-Raphson method for root finding.
    
    Parameters:
        func: Function handle f(x)
        func_derivative: Derivative function handle f'(x)
        x0: Initial guess
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
    
    Returns:
        root: Approximated root
        iterations: List of iteration data
        message: Status message
    """
    iterations = []
    message = "⚠️ Maximum iterations reached without convergence."
    x1 = x0

    for i in range(max_iter):
        f_val = func(x0)
        f_prime = func_derivative(x0)

        # Check for zero derivative
        if abs(f_prime) < 1e-14:
            return None, iterations, "❌ Derivative became zero — division by zero! Change initial guess x₀."

        # Newton-Raphson update formula
        x1 = x0 - f_val / f_prime
        error = abs(x1 - x0)

        # Store iteration data
        iterations.append({
            'x₀': round(x0, 8),
            'f(x₀)': round(f_val, 8),
            "f'(x₀)": round(f_prime, 8),
            'x₁': round(x1, 8),
            'Error': round(error, 8),
        })

        # Check convergence
        if error < tol:
            message = f"✅ Root found! Converged in {i+1} iterations."
            break

        x0 = x1

    return x1, iterations, message


# ─────────────────────────────────────────────
# METHOD 3: SECANT
# ─────────────────────────────────────────────
def secant(func, x0: float, x1: float, tol: float = 1e-6, max_iter: int = 100):
    """
    Secant method for root finding (derivative-free).
    
    Parameters:
        func: Function handle f(x)
        x0, x1: Two initial guesses
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
    
    Returns:
        root: Approximated root
        iterations: List of iteration data
        message: Status message
    """
    iterations = []
    message = "⚠️ Maximum iterations reached without convergence."
    x2 = x1
    
    # Evaluate function at initial points
    f0 = func(x0)
    f1 = func(x1)
    
    for i in range(max_iter):
        # Calculate denominator
        denom = f1 - f0
        
        # Check for division by zero
        if abs(denom) < 1e-14:
            return None, iterations, "❌ f(x₁) - f(x₀) = 0, division by zero! Change initial guesses."
        
        # Secant update formula
        x2 = x1 - f1 * (x1 - x0) / denom
        error = abs(x2 - x1)
        
        # Evaluate function at new point
        f2 = func(x2)
        
        # Store iteration data
        iterations.append({
            'x₀': round(x0, 8),
            'x₁': round(x1, 8),
            'x₂': round(x2, 8),
            'f(x₂)': round(f2, 8),
            'Error': round(error, 8),
        })
        
        # Check convergence
        if error < tol:
            message = f"✅ Root found! Converged in {i+1} iterations."
            break
        
        # Update points for next iteration
        x0, x1 = x1, x2
        f0, f1 = f1, f2
    
    return x2, iterations, message


# ─────────────────────────────────────────────
# IMPROVED DUAL-PANEL PLOT
# ─────────────────────────────────────────────
def plot_root(func, root, a, b, method_name, iterations, accent_color='#00d4ff'):
    """
    Create a beautiful dual-panel plot:
      Left  — function curve with root marker, zero-crossing highlight, and interval shading
      Right — convergence (error per iteration on log scale) with gradient fill
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.patch.set_facecolor('#0d1117')
    fig.subplots_adjust(wspace=0.32)

    # ── Left: function curve ──────────────────────────────────────────────────
    _apply_dark_style(fig, ax1)
    margin = max(abs(b - a) * 0.45, 0.5)
    x_min = min(a, b) - margin
    x_max = max(a, b) + margin
    x_range = np.linspace(x_min, x_max, 800)

    try:
        y_range = np.vectorize(func)(x_range)
        # Clip extreme values for cleaner display
        y_med = np.nanmedian(np.abs(y_range[np.isfinite(y_range)]))
        clip = y_med * 8 if y_med > 0 else 10
        y_range = np.clip(y_range, -clip, clip)
    except Exception:
        y_range = np.zeros_like(x_range)

    # Background interval band
    ax1.axvspan(min(a, b), max(a, b), alpha=0.06, color='#7c3aed', zorder=0)

    # Main curve
    ax1.plot(x_range, y_range, color=accent_color, linewidth=2.4,
             label='f(x)', zorder=4, solid_capstyle='round')

    # Zero axes
    ax1.axhline(0, color='#334155', linewidth=1.2, linestyle='-', zorder=1)
    ax1.axvline(0, color='#334155', linewidth=1.2, linestyle='-', zorder=1)

    # Zero-crossing fill
    try:
        ax1.fill_between(x_range, y_range, 0,
                         where=(y_range >= 0), alpha=0.07, color='#00d4ff', zorder=2)
        ax1.fill_between(x_range, y_range, 0,
                         where=(y_range < 0), alpha=0.07, color='#7c3aed', zorder=2)
    except Exception:
        pass

    # Interval markers a, b
    for pt, label, col in [(min(a, b), 'a', '#7c3aed'), (max(a, b), 'b', '#a78bfa')]:
        try:
            ax1.axvline(pt, color=col, linewidth=1, linestyle=':', alpha=0.7, zorder=3)
            ax1.annotate(label, xy=(pt, 0), xytext=(pt, ax1.get_ylim()[0] * 0.15 if ax1.get_ylim()[0] < 0 else 0),
                         color=col, fontsize=9, ha='center', fontweight='bold')
        except Exception:
            pass

    # Root marker
    if root is not None:
        try:
            y_root = func(root)
            ax1.scatter([root], [y_root], color='#f59e0b', s=160, zorder=7,
                        label=f'Root ≈ {root:.6f}', edgecolors='#fde68a',
                        linewidths=1.8)
            ax1.axvline(root, color='#f59e0b', linewidth=1.5,
                        linestyle='--', alpha=0.65, zorder=5)
            # Annotation
            ax1.annotate(f'  {root:.4f}',
                         xy=(root, y_root),
                         xytext=(root + margin * 0.15, y_root),
                         color='#fde68a', fontsize=8.5,
                         arrowprops=dict(arrowstyle='->', color='#f59e0b', lw=1.2))
        except Exception:
            pass

    ax1.set_title(f'{method_name} — f(x) Curve',
                  fontsize=11, fontweight='bold', pad=12, color='#e2e8f0')
    ax1.set_xlabel('x', fontsize=10)
    ax1.set_ylabel('f(x)', fontsize=10)
    ax1.legend(facecolor='#111827', edgecolor='#1e3a5f',
               labelcolor='#e2e8f0', fontsize=9, loc='best')

    # ── Right: convergence graph ──────────────────────────────────────────────
    _apply_dark_style(fig, ax2)

    if iterations:
        errors = [max(it['Error'], 1e-15) for it in iterations]
        iters = list(range(1, len(iterations) + 1))

        # Gradient-ish line with glow effect
        ax2.semilogy(iters, errors, color='#7c3aed', linewidth=2.5,
                     marker='o', markersize=6, markerfacecolor='#f59e0b',
                     markeredgecolor='#fde68a', markeredgewidth=1.2,
                     zorder=4, label='Error')

        # Tolerance line
        tol_ref = errors[-1]
        ax2.axhline(tol_ref, color='#10b981', linewidth=1,
                    linestyle='--', alpha=0.7, label=f'Final tol ≈ {tol_ref:.1e}')

        # Fill under error curve
        ax2.fill_between(iters, errors, min(errors),
                         alpha=0.18, color='#7c3aed', zorder=2)

        # Annotate first and last
        if len(iters) > 0:
            ax2.annotate(f'{errors[0]:.2e}', xy=(iters[0], errors[0]),
                         xytext=(iters[0] + 0.4, errors[0] * 3),
                         color='#94a3b8', fontsize=7.5,
                         arrowprops=dict(arrowstyle='->', color='#475569', lw=0.8))
            ax2.annotate(f'{errors[-1]:.2e}', xy=(iters[-1], errors[-1]),
                         xytext=(max(1, iters[-1] - 2), errors[-1] * 30),
                         color='#94a3b8', fontsize=7.5,
                         arrowprops=dict(arrowstyle='->', color='#475569', lw=0.8))

        ax2.set_title('Convergence — Error per Iteration',
                      fontsize=11, fontweight='bold', pad=12, color='#e2e8f0')
        ax2.set_xlabel('Iteration #', fontsize=10)
        ax2.set_ylabel('Error (log scale)', fontsize=10)
        ax2.legend(facecolor='#111827', edgecolor='#1e3a5f',
                   labelcolor='#e2e8f0', fontsize=9)
        
        # Set x-ticks with reasonable spacing
        step = max(1, len(iters) // 8)
        ax2.set_xticks(iters[::step])

    plt.tight_layout(pad=1.5)
    return fig


# ─────────────────────────────────────────────
# RESULTS DISPLAY HELPER
# ─────────────────────────────────────────────
def _show_results(root, iters, msg, func, a_plot, b_plot, method_name, accent='#00d4ff'):
    """Display metrics, graph, and iteration table after a successful run."""
    if root is None:
        st.error(msg)
        return

    st.success(msg)

    # Metric cards
    m1, m2, m3 = st.columns(3)
    m1.metric("🎯 Root found", f"{root:.8f}")
    m2.metric("🔄 Iterations", len(iters))
    m3.metric("📉 Final error", f"{iters[-1]['Error']:.2e}" if iters else "N/A")

    st.markdown("#### 📊 Graph")
    fig = plot_root(func, root, a_plot, b_plot, method_name, iters, accent)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    with st.expander("📋 Iteration Table (click to expand)"):
        display_iteration_table(iters)


# ─────────────────────────────────────────────
# HELPER: Parse and validate function input
# ─────────────────────────────────────────────
def validate_and_parse_function(func_str):
    """Parse function string and return callable function or error message"""
    func, err = parse_function(func_str)
    if err:
        st.error(err)
        return None, True
    return func, False


# ─────────────────────────────────────────────
# MAIN LAB RENDERER
# ─────────────────────────────────────────────
def render_lab1():
    """Main Streamlit UI renderer for Lab 1"""
    # ── Page header ───────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Outfit:wght@400;600;800&display=swap');
    .lab-header {
        background: linear-gradient(135deg,
            rgba(0,212,255,.07) 0%,
            rgba(124,58,237,.07) 60%,
            rgba(16,185,129,.04) 100%);
        border: 1px solid rgba(0,212,255,.2);
        border-radius: 20px;
        padding: 1.8rem 2.2rem;
        margin-bottom: 1.6rem;
        position: relative;
        overflow: hidden;
    }
    .lab-header::before {
        content: '';
        position: absolute;
        top: -40px; right: -40px;
        width: 180px; height: 180px;
        background: radial-gradient(circle, rgba(0,212,255,.08), transparent 70%);
        border-radius: 50%;
    }
    .lab-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: .65rem;
        color: #00d4ff;
        letter-spacing: .2em;
        text-transform: uppercase;
        margin-bottom: .5rem;
    }
    .lab-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 1.75rem;
        color: #f1f5f9;
        margin: 0 0 .4rem;
    }
    .lab-subtitle {
        color: #64748b;
        font-size: .9rem;
        margin: 0;
    }
    .lab-subtitle code {
        color: #00d4ff;
        background: rgba(0,212,255,.08);
        padding: .1rem .35rem;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
    }
    .method-card {
        background: rgba(15,25,45,.6);
        border: 1px solid rgba(30,58,95,.7);
        border-radius: 14px;
        padding: 1rem 1.3rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: .76rem;
        color: #94a3b8;
        line-height: 1.9;
        height: 100%;
    }
    .method-card .mc-label {
        font-family: 'Outfit', sans-serif;
        font-size: .65rem;
        font-weight: 700;
        letter-spacing: .15em;
        text-transform: uppercase;
        margin-bottom: .5rem;
    }
    </style>

    <div class="lab-header">
        <div class="lab-badge">◆ Lab 01 · Numerical Methods</div>
        <div class="lab-title">🔍 Root Finding Methods</div>
        <p class="lab-subtitle">
            Find roots of nonlinear equations <code>f(x) = 0</code> —
            Bisection · Newton-Raphson · Secant
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Function guide (collapsible) ──────────────────────────────────────────
    show_function_guide()

    st.markdown("---")

    # ── Method tabs ───────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs([
        "⟨ ⟩  Bisection",
        "∂  Newton-Raphson",
        "∕∕  Secant",
    ])

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 1 — BISECTION
    # ══════════════════════════════════════════════════════════════════════════
    with tab1:
        st.markdown("##### Interval Halving — guaranteed convergence if sign change exists")
        st.markdown("")

        col_inp, col_algo = st.columns([1.3, 1], gap="large")

        with col_inp:
            func_str_b = st.text_input(
                "f(x) =",
                value="x**3 - x - 2",
                key="b_func",
                placeholder="e.g.  3x - e^x  or  sin(x) - 0.5  or  x^3 - 2",
                help="Python/numpy/math syntax. e^x, sin(x), ln(x), x^2, sqrt(x) — all work!",
            )

            # Example quick-fill buttons
            st.markdown("<div style='font-size:.72rem;color:#64748b;margin-bottom:.3rem;'>Quick examples:</div>", unsafe_allow_html=True)
            ex_cols = st.columns(4)
            examples_b = ["x**3 - x - 2", "3*x - exp(x)", "sin(x) - 0.5", "x*exp(x) - 1"]
            for i, (col, ex) in enumerate(zip(ex_cols, examples_b)):
                if col.button(ex, key=f"bex_{i}", use_container_width=True):
                    st.session_state["b_func"] = ex
                    st.rerun()

            st.markdown("")
            c1, c2 = st.columns(2)
            a_b = c1.number_input("Left bound a", value=1.0, step=0.5, key="b_a",
                                   help="Left endpoint of interval. f(a) and f(b) must have opposite signs.")
            b_b = c2.number_input("Right bound b", value=2.0, step=0.5, key="b_b",
                                   help="Right endpoint of interval.")
            c3, c4 = st.columns(2)
            tol_b = c3.number_input("Tolerance", value=1e-6, format="%.2e", key="b_tol",
                                     help="Desired accuracy. 1e-6 = 0.000001")
            mi_b = c4.number_input("Max iterations", value=50, min_value=1, max_value=500, key="b_mi")

        with col_algo:
            st.markdown("""
            <div class="method-card">
                <div class="mc-label" style="color:#00d4ff;">Algorithm</div>
                1. c = (a + b) / 2<br>
                2. if f(a)·f(c) &lt; 0 → b = c<br>
                3. else → a = c<br>
                4. repeat until |b−a| &lt; tol<br><br>
                <span style="color:#f59e0b;">Convergence:</span> Linear — O(1/2ⁿ)<br>
                <span style="color:#10b981;">Guarantee:</span> Always converges<br>
                <span style="color:#7c3aed;">Requirement:</span> Sign change in [a,b]
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")
        run_b = st.button("▶  Run Bisection", key="run_b", use_container_width=True,
                           type="primary")

        if run_b:
            func, err = parse_function(func_str_b)
            if not err:
                root, iters, msg = bisection(func, a_b, b_b, tol_b, int(mi_b))
                _show_results(root, iters, msg, func, a_b, b_b, "Bisection", '#00d4ff')

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 2 — NEWTON-RAPHSON
    # ══════════════════════════════════════════════════════════════════════════
    with tab2:
        st.markdown("##### Tangent Line Method — quadratic convergence near root")
        st.markdown("")

        col_inp, col_algo = st.columns([1.3, 1], gap="large")

        with col_inp:
            func_str_n = st.text_input(
                "f(x) =",
                value="x**3 - x - 2",
                key="n_func",
                placeholder="e.g.  cos(x) - x  or  exp(x) - 3*x  or  x**2 - 2",
                help="Derivative will be automatically computed using SymPy.",
            )

            ex_cols_n = st.columns(4)
            examples_n = ["x**3 - x - 2", "cos(x) - x", "exp(x) - 3*x", "x**2 - 2"]
            for i, (col, ex) in enumerate(zip(ex_cols_n, examples_n)):
                if col.button(ex, key=f"nex_{i}", use_container_width=True):
                    st.session_state["n_func"] = ex
                    st.rerun()

            st.markdown("")
            x0_n = st.number_input("Initial guess x₀", value=1.5, step=0.5, key="n_x0",
                                     help="Starting point. Should be close to the root for better results.")
            c3, c4 = st.columns(2)
            tol_n = c3.number_input("Tolerance", value=1e-6, format="%.2e", key="n_tol")
            mi_n = c4.number_input("Max iterations", value=50, min_value=1, key="n_mi")

        with col_algo:
            st.markdown("""
            <div class="method-card">
                <div class="mc-label" style="color:#7c3aed;">Algorithm</div>
                x₁ = x₀ − f(x₀) / f'(x₀)<br>
                repeat until |x₁ − x₀| &lt; tol<br><br>
                <span style="color:#f59e0b;">Convergence:</span> Quadratic — very fast!<br>
                <span style="color:#10b981;">Advantage:</span> Very few iterations<br>
                <span style="color:#7c3aed;">Note:</span> f'(x) auto-computed<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;via SymPy symbolic differentiation
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")
        run_n = st.button("▶  Run Newton-Raphson", key="run_n", use_container_width=True,
                           type="primary")

        if run_n:
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
                    st.info(f"🔢 Auto-computed: f'(x) = `{sp.simplify(deriv)}`  (via SymPy)")
                except Exception as ex:
                    st.error(f"❌ Could not compute derivative: {ex}")
                    st.stop()

                root, iters, msg = newton_raphson(func, func_d, x0_n, tol_n, int(mi_n))
                a_plot = x0_n - 3
                b_plot = x0_n + 3
                _show_results(root, iters, msg, func, a_plot, b_plot, "Newton-Raphson", '#7c3aed')

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 3 — SECANT (FIXED)
    # ══════════════════════════════════════════════════════════════════════════
    with tab3:
        st.markdown("##### Secant Method — derivative-free, superlinear convergence")
        st.markdown("")

        col_inp, col_algo = st.columns([1.3, 1], gap="large")

        with col_inp:
            func_str_s = st.text_input(
                "f(x) =",
                value="x**3 - x - 2",
                key="s_func",
                placeholder="e.g.  x*log(x) - 1  or  tan(x) - x  or  exp(x) - 2",
                help="Any continuous function. Two initial guesses are required.",
            )

            ex_cols_s = st.columns(4)
            examples_s = ["x**3 - x - 2", "x*log(x) - 1", "exp(x) - 2", "sin(x) - x/2"]
            for i, (col, ex) in enumerate(zip(ex_cols_s, examples_s)):
                if col.button(ex, key=f"sex_{i}", use_container_width=True):
                    st.session_state["s_func"] = ex
                    st.rerun()

            st.markdown("")
            c1, c2 = st.columns(2)
            x0_s = c1.number_input("First guess x₀", value=1.0, step=0.5, key="s_x0")
            x1_s = c2.number_input("Second guess x₁", value=2.0, step=0.5, key="s_x1")
            c3, c4 = st.columns(2)
            tol_s = c3.number_input("Tolerance", value=1e-6, format="%.2e", key="s_tol")
            mi_s = c4.number_input("Max iterations", value=50, min_value=1, key="s_mi")

        with col_algo:
            st.markdown("""
            <div class="method-card">
                <div class="mc-label" style="color:#10b981;">Algorithm</div>
                x₂ = x₁ − f(x₁)·(x₁−x₀)<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/ (f(x₁) − f(x₀))<br>
                repeat until |x₂ − x₁| &lt; tol<br><br>
                <span style="color:#f59e0b;">Convergence:</span> Superlinear ~1.618<br>
                <span style="color:#10b981;">Advantage:</span> No derivative needed<br>
                <span style="color:#7c3aed;">Input:</span> Two initial guesses
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")
        run_s = st.button("▶  Run Secant", key="run_s", use_container_width=True,
                           type="primary")

        if run_s:
            func, err = parse_function(func_str_s)
            if not err:
                # Ensure x0 != x1
                if abs(x0_s - x1_s) < 1e-14:
                    st.error("❌ Initial guesses x₀ and x₁ must be different!")
                else:
                    root, iters, msg = secant(func, x0_s, x1_s, tol_s, int(mi_s))
                    a_plot = min(x0_s, x1_s) - 1.5
                    b_plot = max(x0_s, x1_s) + 1.5
                    _show_results(root, iters, msg, func, a_plot, b_plot, "Secant", '#10b981')


# ── standalone test ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    f = lambda x: x**3 - x - 2
    root, logs, msg = bisection(f, 1, 2)
    print(msg, "| Root:", root)
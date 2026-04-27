"""
helpers.py - Utility functions shared across all labs
=====================================================
Robust function parser that handles:
  • Arithmetic:         2/(x-4), x^2+3, (x+1)*(x-2)
  • Trig:               sin(x), cos(x), tan(x), sec(x), csc(x), cot(x)
  • Inverse trig:       asin(x), acos(x), atan(x)  [also arcsin etc.]
  • Exponentials:       e^x, exp(x), 2^x
  • Logarithms:         ln(x), log(x), log2(x), log10(x)
  • Roots:              sqrt(x), cbrt(x), x^(1/3)
  • Hyperbolic:         sinh(x), cosh(x), tanh(x)
  • Implicit multiply:  2x, 3sin(x), 5(x+1)
  • Constants:          pi, e
  • ODE form:           f(x, y) for use in lab ODE solvers
"""

import numpy as np
import sympy as sp
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)

# ─────────────────────────────────────────────────────────────────────────────
# SYMBOL ALIASES — map common shorthand → sympy-valid strings before parsing
# ─────────────────────────────────────────────────────────────────────────────
_ALIASES = [
    # Logarithms
    (r'\bln\b',    'log'),          # ln  → sympy log (natural)
    (r'\blog2\b',  'log2_custom'),  # handled below
    (r'\blog10\b', 'log10_custom'),
    # Inverse trig alternate names
    (r'\barcsin\b', 'asin'),
    (r'\barccos\b', 'acos'),
    (r'\barctan\b', 'atan'),
    (r'\barcsec\b', 'asec'),
    (r'\barccsc\b', 'acsc'),
    (r'\barccot\b', 'acot'),
    # Degree trig (rare, but nice to support)
    (r'\bsind\b',  'sin'),
    (r'\bcosd\b',  'cos'),
    (r'\btand\b',  'tan'),
    # Cube root
    (r'\bcbrt\b',  'cbrt_custom'),
    # Absolute value  |x|  →  Abs(x)
    (r'\|([^|]+)\|', r'Abs(\1)'),
    # ^ → ** (caret as power)
    (r'\^',        '**'),
]

_NUMPY_EXTRAS = {
    'log2_custom':  lambda x: np.log2(x),
    'log10_custom': lambda x: np.log10(x),
    'cbrt_custom':  lambda x: np.cbrt(x),
    'sec':  lambda x: 1.0 / np.cos(x),
    'csc':  lambda x: 1.0 / np.sin(x),
    'cot':  lambda x: np.cos(x) / np.sin(x),
    'asec': lambda x: np.arccos(1.0 / x),
    'acsc': lambda x: np.arcsin(1.0 / x),
    'acot': lambda x: np.pi / 2 - np.arctan(x),
}

_SYMPY_EXTRAS = {
    'log2_custom':  lambda x: sp.log(x, 2),
    'log10_custom': lambda x: sp.log(x, 10),
    'cbrt_custom':  lambda x: sp.cbrt(x),
    'sec':  lambda x: 1 / sp.cos(x),
    'csc':  lambda x: 1 / sp.sin(x),
    'cot':  lambda x: sp.cos(x) / sp.sin(x),
    'asec': lambda x: sp.acos(1 / x),
    'acsc': lambda x: sp.asin(1 / x),
    'acot': lambda x: sp.atan(1 / x),  # simplified
}


def _preprocess(func_str: str) -> str:
    """Apply alias substitutions and light cleanup."""
    s = func_str.strip()
    for pattern, repl in _ALIASES:
        s = re.sub(pattern, repl, s)
    return s


# ─────────────────────────────────────────────────────────────────────────────
# PRIMARY PARSER  — f(x)
# ─────────────────────────────────────────────────────────────────────────────

def parse_function(func_str: str):
    """
    Parse a mathematical expression in x and return (callable, sympy_expr).

    Supported syntax examples
    ─────────────────────────
    Polynomials   : x**2 - 3x + 2,  (x+1)*(x-3)
    Fractions     : 2/(x-4),  (x^2+1)/(x-1)
    Powers        : x^3,  e^x,  2^x,  x^(1/3)
    Trig          : sin(x), cos(2x), tan(x), sec(x), csc(x), cot(x)
    Inverse trig  : asin(x), arctan(x)
    Logarithms    : ln(x), log(x), log2(x), log10(x)
    Exponentials  : exp(x),  e^x
    Roots         : sqrt(x),  cbrt(x),  x^0.5
    Hyperbolic    : sinh(x), cosh(x), tanh(x)
    Abs value     : |x|,  Abs(x)
    Constants     : pi,  e
    Implicit mul  : 2x,  3sin(x),  5(x+1)

    Returns
    ───────
    (func, None)       on success  — func is numpy-safe callable
    (None, error_str)  on failure  — compatible with lab pattern: if err: st.error(err)
    """
    if not func_str or not func_str.strip():
        msg = "Function field khali hai. Kuch enter karein."
        st.error("❌ " + msg)
        return None, msg

    x_sym = sp.Symbol('x')
    s = _preprocess(func_str)

    try:
        transformations = (
            standard_transformations
            + (implicit_multiplication_application, convert_xor)
        )

        # Local dict for sympy to recognise our custom symbols + constants
        local_dict = {name: sp.Function(name) for name in _SYMPY_EXTRAS}
        local_dict['x'] = x_sym
        local_dict['e'] = sp.E      # Euler's number
        local_dict['pi'] = sp.pi

        expr = parse_expr(s, local_dict=local_dict,
                          transformations=transformations)

        # Build numpy module map including our extras
        numpy_modules = ['numpy', _NUMPY_EXTRAS]
        raw_func = sp.lambdify(x_sym, expr, modules=numpy_modules)

        def func(val):
            result = raw_func(val)
            if isinstance(val, np.ndarray) and not isinstance(result, np.ndarray):
                return np.full_like(val, float(result), dtype=float)
            return result

        # ✅ Success — second value is None so `if err:` stays False in labs
        return func, None

    except Exception as e:
        error_msg = str(e)
        _show_parse_error(func_str, error_msg)
        return None, error_msg


# ─────────────────────────────────────────────────────────────────────────────
# ODE PARSER  — f(x, y)
# ─────────────────────────────────────────────────────────────────────────────

def parse_ode(func_str: str):
    """
    Parse an ODE RHS expression in x and y.
    e.g. "x + y",  "x*y - 2",  "sin(x)*y"

    Returns: callable(x, y)  or  None
    """
    if not func_str or not func_str.strip():
        st.error("❌ ODE function khali hai.")
        return None

    x_sym, y_sym = sp.symbols('x y')
    s = _preprocess(func_str)

    try:
        local_dict = {name: sp.Function(name) for name in _SYMPY_EXTRAS}
        local_dict.update({'x': x_sym, 'y': y_sym, 'e': sp.E, 'pi': sp.pi})

        transformations = (
            standard_transformations
            + (implicit_multiplication_application, convert_xor)
        )
        expr = parse_expr(s, local_dict=local_dict,
                          transformations=transformations)

        numpy_modules = ['numpy', _NUMPY_EXTRAS]
        func = sp.lambdify((x_sym, y_sym), expr, modules=numpy_modules)
        return func

    except Exception as e:
        st.error(f"❌ ODE parse error: {e}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
# VALIDATION HELPER  — check for singularities / domain issues in [a, b]
# ─────────────────────────────────────────────────────────────────────────────

def validate_on_interval(func, a: float, b: float, n_check: int = 200):
    """
    Lightly probe the function on [a, b].
    Returns (is_ok, warning_message_or_None).
    """
    xs = np.linspace(a, b, n_check)
    try:
        ys = func(xs)
        ys = np.atleast_1d(ys).astype(float)
        if np.any(~np.isfinite(ys)):
            bad = xs[~np.isfinite(ys)]
            return False, (
                f"Function interval [{a}, {b}] mein undefined/infinite values hain "
                f"(approx x ≈ {bad[0]:.4f}). "
                "Shayad singularity ho — bounds badlein."
            )
        return True, None
    except Exception as e:
        return False, f"Evaluation error on [{a}, {b}]: {e}"


# ─────────────────────────────────────────────────────────────────────────────
# USER-FACING INPUT GUIDE  (call once near the top of your lab's UI)
# ─────────────────────────────────────────────────────────────────────────────

def show_function_guide():
    """
    Animated, styled reference card telling the user exactly what syntax is
    accepted.  Call this inside a Streamlit expander or sidebar.
    """
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Syne:wght@600;800&display=swap');

    .guide-wrap {
        background: linear-gradient(135deg, #0d1117 0%, #0f1e35 100%);
        border: 1px solid #1e3a5f;
        border-radius: 16px;
        padding: 1.4rem 1.8rem 1.6rem;
        font-family: 'JetBrains Mono', monospace;
        animation: fadeSlide 0.5s ease both;
        box-shadow: 0 8px 40px rgba(0,212,255,0.07);
    }
    @keyframes fadeSlide {
        from { opacity:0; transform:translateY(-8px); }
        to   { opacity:1; transform:translateY(0); }
    }
    .guide-title {
        font-family: 'Syne', sans-serif;
        font-size: 1rem;
        font-weight: 800;
        letter-spacing: .12em;
        color: #00d4ff;
        margin-bottom: 1rem;
        text-transform: uppercase;
    }
    .guide-section { margin-bottom: .9rem; }
    .guide-label {
        font-size: .65rem;
        font-weight: 600;
        letter-spacing: .15em;
        text-transform: uppercase;
        color: #f59e0b;
        margin-bottom: .3rem;
    }
    .guide-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: .4rem .8rem;
    }
    .guide-chip {
        background: rgba(30,58,95,.55);
        border: 1px solid #1e3a5f;
        border-radius: 8px;
        padding: .28rem .7rem;
        font-size: .72rem;
        color: #e2e8f0;
        transition: border-color .2s, background .2s;
    }
    .guide-chip b { color: #7ee8fa; }
    .guide-chip:hover {
        background: rgba(0,212,255,.08);
        border-color: #00d4ff44;
    }
    .guide-note {
        background: rgba(239,68,68,.08);
        border-left: 3px solid #ef4444;
        border-radius: 0 8px 8px 0;
        padding: .5rem .9rem;
        font-size: .72rem;
        color: #fca5a5;
        margin-top: .6rem;
    }
    .guide-ok {
        background: rgba(16,185,129,.08);
        border-left: 3px solid #10b981;
        border-radius: 0 8px 8px 0;
        padding: .5rem .9rem;
        font-size: .72rem;
        color: #6ee7b7;
        margin-top: .4rem;
    }
    </style>

    <div class="guide-wrap">
      <div class="guide-title">📐 Function Input Guide</div>

      <div class="guide-section">
        <div class="guide-label">✅ Allowed — Trig</div>
        <div class="guide-grid">
          <div class="guide-chip"><b>sin(x)</b> &nbsp;cos(x)</div>
          <div class="guide-chip"><b>tan(x)</b> &nbsp;sec(x)</div>
          <div class="guide-chip"><b>csc(x)</b> &nbsp;cot(x)</div>
          <div class="guide-chip"><b>asin(x)</b> arcsin(x)</div>
          <div class="guide-chip"><b>acos(x)</b> acos(x)</div>
          <div class="guide-chip"><b>atan(x)</b> arctan(x)</div>
        </div>
      </div>

      <div class="guide-section">
        <div class="guide-label">✅ Allowed — Exponentials & Logs</div>
        <div class="guide-grid">
          <div class="guide-chip"><b>exp(x)</b> or e^x</div>
          <div class="guide-chip"><b>ln(x)</b> — natural log</div>
          <div class="guide-chip"><b>log(x)</b> — natural log</div>
          <div class="guide-chip"><b>log2(x)</b> — base 2</div>
          <div class="guide-chip"><b>log10(x)</b> — base 10</div>
          <div class="guide-chip"><b>2^x</b> or 2**x</div>
        </div>
      </div>

      <div class="guide-section">
        <div class="guide-label">✅ Allowed — Roots, Power & Other</div>
        <div class="guide-grid">
          <div class="guide-chip"><b>sqrt(x)</b> — square root</div>
          <div class="guide-chip"><b>cbrt(x)</b> — cube root</div>
          <div class="guide-chip"><b>x^(1/3)</b> fractional power</div>
          <div class="guide-chip"><b>|x|</b> or Abs(x)</div>
          <div class="guide-chip"><b>sinh(x)</b> cosh(x) tanh(x)</div>
          <div class="guide-chip"><b>pi</b>, <b>e</b> — constants</div>
        </div>
      </div>

      <div class="guide-section">
        <div class="guide-label">✅ Implicit Multiplication — No * needed</div>
        <div class="guide-grid">
          <div class="guide-chip"><b>2x</b> → 2*x</div>
          <div class="guide-chip"><b>3sin(x)</b> → 3*sin(x)</div>
          <div class="guide-chip"><b>5(x+1)</b> → 5*(x+1)</div>
          <div class="guide-chip"><b>(x+1)(x-2)</b> → multiply</div>
        </div>
      </div>

      <div class="guide-note">
        ❌ <b>Na likhein:</b> &nbsp;
        <code>2/(x-4)</code> mein x=4 singularity hai — bounds mein 4 mat rakhein. &nbsp;
        <code>ln(x)</code> ke liye x&gt;0 chahiye. &nbsp;
        <code>asin(x)</code> / <code>acos(x)</code> ke liye -1 ≤ x ≤ 1 chahiye. &nbsp;
        <code>sqrt(x)</code> ke liye x≥0 chahiye.
      </div>
      <div class="guide-ok">
        💡 <b>Pro tip:</b> &nbsp;Use <code>x**2</code> or <code>x^2</code> — dono chalte hain.
        Spaces allowed: <code>sin( x ) + 2 x</code> bhi sahi hai.
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# INTERNAL ERROR DISPLAY
# ─────────────────────────────────────────────────────────────────────────────

def _show_parse_error(original: str, detail: str):
    """Show a styled, helpful error when parsing fails."""
    st.markdown(f"""
    <div style="
        background:rgba(239,68,68,.1);
        border:1px solid #ef4444;
        border-radius:12px;
        padding:1rem 1.2rem;
        font-family:'JetBrains Mono',monospace;
        font-size:.78rem;
        color:#fca5a5;
        animation: shake .35s ease;
    ">
    <b style="color:#ef4444;font-size:.85rem;">❌ Parse Error</b><br><br>
    Input: <code style="color:#fde68a;">{original}</code><br><br>
    Detail: <span style="color:#f87171;">{detail}</span><br><br>
    <span style="color:#94a3b8;">
    ↳ Oopar wala Function Input Guide dekho — allowed syntax aur examples hain wahan.
    </span>
    </div>
    <style>
    @keyframes shake {{
        0%,100% {{ transform:translateX(0); }}
        25%      {{ transform:translateX(-4px); }}
        75%      {{ transform:translateX(4px); }}
    }}
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SHARED UI COMPONENTS
# ─────────────────────────────────────────────────────────────────────────────

def display_iteration_table(columns: list, data: list):
    """
    Iteration steps ko pandas DataFrame ki tarah display karta hai.
    columns: list of column names
    data: list of rows (each row is a list/tuple)
    """
    df = pd.DataFrame(data, columns=columns)
    df.index += 1
    df.index.name = "Iteration"
    st.dataframe(df, use_container_width=True)


def plot_function(func, x_range: tuple, roots=None, title="Function Plot"):
    """
    Function plot karta hai given x_range mein.
    roots: list of root x-values (optional, red dots lagata hai)
    """
    x_vals = np.linspace(x_range[0], x_range[1], 500)
    try:
        y_vals = func(x_vals)
    except Exception:
        st.error("Plotting error: function could not be evaluated over the range.")
        return

    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor('#111827')
    ax.set_facecolor('#1a2236')
    ax.tick_params(colors='#94a3b8', labelsize=9)
    ax.xaxis.label.set_color('#94a3b8')
    ax.yaxis.label.set_color('#94a3b8')
    ax.title.set_color('#e2e8f0')
    for spine in ax.spines.values():
        spine.set_edgecolor('#1e3a5f')
    ax.grid(True, color='#1e3a5f', linewidth=0.6, linestyle='--', alpha=0.6)

    ax.plot(x_vals, y_vals, color='#00d4ff', linewidth=2, label='f(x)')
    ax.axhline(0, color='#475569', linewidth=0.8, linestyle='--')
    ax.axvline(0, color='#475569', linewidth=0.8, linestyle='--')

    if roots:
        for r in roots:
            try:
                ax.plot(r, func(r), 'ro', markersize=8, label=f'Root ≈ {r:.6f}')
            except Exception:
                pass

    ax.set_title(title, color='#e2e8f0')
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend(facecolor='#1a2236', edgecolor='#1e3a5f',
              labelcolor='#e2e8f0', fontsize=9)
    st.pyplot(fig)
    plt.close(fig)
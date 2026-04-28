"""
helpers.py - Utility functions shared across all labs
=====================================================
Robust function parser that handles:
  • Arithmetic:         2/(x-4), x^2+3, (x+1)*(x-2)
  • Trig:               sin(x), cos(x), tan(x), sec(x), csc(x), cot(x)
  • Inverse trig:       asin(x), acos(x), atan(x)  [also arcsin etc.]
  • Exponentials:       e^x, exp(x), 2^x, e**x
  • Logarithms:         ln(x), log(x), log2(x), log10(x)
  • Roots:              sqrt(x), cbrt(x), x^(1/3)
  • Hyperbolic:         sinh(x), cosh(x), tanh(x)
  • Implicit multiply:  2x, 3sin(x), 5(x+1)
  • Constants:          pi, e
  • Equation form:      3x - e^x = 0  (auto-strips '= 0' side)
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
    'acot': lambda x: sp.atan(1 / x),
}


def _strip_equation(func_str: str) -> str:
    """
    If user typed an equation like '3x - e^x = 0' or 'f(x) = sin(x)',
    strip the '= <rhs>' part and return only the LHS expression.
    Also handles '=>' so we don't accidentally strip that.
    """
    # Match '= something' but NOT '=>' or '<=' or '>='
    # We strip the FIRST occurrence of '= <rhs>' only
    cleaned = re.sub(r'(?<![=!<>])=(?!=).*$', '', func_str).strip()
    return cleaned if cleaned else func_str


def _preprocess(func_str: str) -> str:
    """Apply alias substitutions, equation stripping, and light cleanup."""
    s = func_str.strip()
    s = _strip_equation(s)           # ← NEW: handle 'f(x) = 0' form
    for pattern, repl in _ALIASES:
        s = re.sub(pattern, repl, s)
    return s


# ─────────────────────────────────────────────────────────────────────────────
# PRIMARY PARSER  — f(x)
# ─────────────────────────────────────────────────────────────────────────────

def parse_function(func_str: str):
    """
    Parse a mathematical expression in x and return (callable, error).

    Supported syntax examples
    ─────────────────────────
    Polynomials   : x**2 - 3x + 2,  (x+1)*(x-3)
    Fractions     : 2/(x-4),  (x^2+1)/(x-1)
    Powers        : x^3,  e^x,  2^x,  x^(1/3)
    Trig          : sin(x), cos(2x), tan(x), sec(x), csc(x), cot(x)
    Inverse trig  : asin(x), arctan(x)
    Logarithms    : ln(x), log(x), log2(x), log10(x)
    Exponentials  : exp(x),  e^x,  e**x
    Roots         : sqrt(x),  cbrt(x),  x^0.5
    Hyperbolic    : sinh(x), cosh(x), tanh(x)
    Abs value     : |x|,  Abs(x)
    Constants     : pi,  e
    Implicit mul  : 2x,  3sin(x),  5(x+1)
    Equation form : 3x - e^x = 0   (auto-strips rhs)

    Returns
    ───────
    (func, None)       on success  — func is numpy-safe callable
    (None, error_str)  on failure
    """
    if not func_str or not func_str.strip():
        msg = "Function field khali hai. Kuch enter karein."
        st.error("❌ " + msg)
        return None, msg

    x_sym = sp.Symbol('x')

    # Show user what we're parsing after stripping equation form
    original_stripped = _strip_equation(func_str.strip())
    was_equation = original_stripped != func_str.strip()

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

        # Show info if equation form was stripped
        if was_equation:
            st.info(
                f"💡 Equation form detect hua: `{func_str.strip()}` "
                f"→ f(x) = `{original_stripped}` ke roop mein parse kiya gaya "
                f"(right side automatically strip ho gayi)"
            )

        return func, None

    except Exception as e:
        error_msg = str(e)
        _show_parse_error(func_str, error_msg, was_equation)
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
    Renders a polished, comprehensive function input guide with syntax examples
    for all supported function types.
    """
    with st.expander("📐 Function Input Guide — How to write? (click to expand)", expanded=False):
        st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Outfit:wght@400;600;800&display=swap');

.guide-wrap {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1a2e 100%);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 20px;
    padding: 1.6rem 2rem;
    font-family: 'JetBrains Mono', monospace;
}
.guide-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.1rem;
    font-weight: 800;
    color: #00d4ff;
    margin-bottom: 1.2rem;
    letter-spacing: 0.05em;
}
.guide-section { margin-bottom: 1.2rem; }
.guide-label {
    font-size: .65rem;
    font-weight: 600;
    letter-spacing: .18em;
    text-transform: uppercase;
    color: #f59e0b;
    margin-bottom: .5rem;
    display: flex;
    align-items: center;
    gap: .4rem;
}
.guide-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
    gap: .4rem .7rem;
}
.guide-chip {
    background: rgba(30,58,95,.4);
    border: 1px solid rgba(30,58,95,0.8);
    border-radius: 8px;
    padding: .32rem .8rem;
    font-size: .73rem;
    color: #cbd5e1;
    transition: all .2s;
}
.guide-chip b { color: #7ee8fa; }
.guide-chip .arrow { color: #64748b; margin: 0 .3em; }
.guide-warn {
    background: rgba(239,68,68,.08);
    border-left: 3px solid #ef4444;
    border-radius: 0 10px 10px 0;
    padding: .6rem 1rem;
    font-size: .73rem;
    color: #fca5a5;
    margin-top: .8rem;
    line-height: 1.8;
}
.guide-ok {
    background: rgba(16,185,129,.08);
    border-left: 3px solid #10b981;
    border-radius: 0 10px 10px 0;
    padding: .6rem 1rem;
    font-size: .73rem;
    color: #6ee7b7;
    margin-top: .5rem;
    line-height: 1.8;
}
.guide-highlight {
    background: rgba(124,58,237,.12);
    border-left: 3px solid #7c3aed;
    border-radius: 0 10px 10px 0;
    padding: .6rem 1rem;
    font-size: .73rem;
    color: #c4b5fd;
    margin-top: .5rem;
    line-height: 1.8;
}
</style>

<div class="guide-wrap">
  <div class="guide-title">📐 Complete Function Input Guide</div>

  <div class="guide-section">
    <div class="guide-label">🟣 Exponentials — e^x, exp(x)</div>
    <div class="guide-grid">
      <div class="guide-chip"><b>e^x</b> <span class="arrow">→</span> eˣ (Euler's number)</div>
      <div class="guide-chip"><b>exp(x)</b> <span class="arrow">→</span> same as e^x</div>
      <div class="guide-chip"><b>e^(2x)</b> <span class="arrow">→</span> e²ˣ</div>
      <div class="guide-chip"><b>3 - e^x</b> <span class="arrow">→</span> works!</div>
      <div class="guide-chip"><b>2^x</b> or <b>2**x</b> <span class="arrow">→</span> 2ˣ</div>
      <div class="guide-chip"><b>e^(-x)</b> <span class="arrow">→</span> decaying exp</div>
    </div>
  </div>

  <div class="guide-section">
    <div class="guide-label">🔵 Polynomials & Fractions</div>
    <div class="guide-grid">
      <div class="guide-chip"><b>x**2 - 3x + 2</b></div>
      <div class="guide-chip"><b>x^3 - x - 2</b> (^ supported)</div>
      <div class="guide-chip"><b>(x+1)*(x-3)</b></div>
      <div class="guide-chip"><b>2/(x-4)</b> (avoid x=4)</div>
      <div class="guide-chip"><b>(x^2+1)/(x-1)</b></div>
      <div class="guide-chip"><b>x^(1/3)</b> fractional power</div>
    </div>
  </div>

  <div class="guide-section">
    <div class="guide-label">🟡 Trigonometric</div>
    <div class="guide-grid">
      <div class="guide-chip"><b>sin(x)</b>  cos(x)  tan(x)</div>
      <div class="guide-chip"><b>sec(x)</b>  csc(x)  cot(x)</div>
      <div class="guide-chip"><b>asin(x)</b> or arcsin(x)</div>
      <div class="guide-chip"><b>acos(x)</b> or arccos(x)</div>
      <div class="guide-chip"><b>atan(x)</b> or arctan(x)</div>
      <div class="guide-chip"><b>sin(2x)</b>  cos(x/2)</div>
    </div>
  </div>

  <div class="guide-section">
    <div class="guide-label">🟢 Logarithms & Roots</div>
    <div class="guide-grid">
      <div class="guide-chip"><b>ln(x)</b> <span class="arrow">→</span> natural log</div>
      <div class="guide-chip"><b>log(x)</b> <span class="arrow">→</span> natural log</div>
      <div class="guide-chip"><b>log2(x)</b> <span class="arrow">→</span> base-2 log</div>
      <div class="guide-chip"><b>log10(x)</b> <span class="arrow">→</span> base-10</div>
      <div class="guide-chip"><b>sqrt(x)</b> <span class="arrow">→</span> √x</div>
      <div class="guide-chip"><b>cbrt(x)</b> <span class="arrow">→</span> ∛x</div>
    </div>
  </div>

  <div class="guide-section">
    <div class="guide-label">⚪ Implicit Multiplication & Constants</div>
    <div class="guide-grid">
      <div class="guide-chip"><b>2x</b> <span class="arrow">→</span> 2*x (no * needed)</div>
      <div class="guide-chip"><b>3sin(x)</b> <span class="arrow">→</span> 3*sin(x)</div>
      <div class="guide-chip"><b>5(x+1)</b> <span class="arrow">→</span> 5*(x+1)</div>
      <div class="guide-chip"><b>(x+1)(x-2)</b> <span class="arrow">→</span> multiply</div>
      <div class="guide-chip"><b>pi</b> <span class="arrow">→</span> π ≈ 3.14159</div>
      <div class="guide-chip"><b>e</b> <span class="arrow">→</span> e ≈ 2.71828</div>
    </div>
  </div>

  <div class="guide-section">
    <div class="guide-label">🔴 Hyperbolic & Absolute Value</div>
    <div class="guide-grid">
      <div class="guide-chip"><b>sinh(x)</b>  cosh(x)  tanh(x)</div>
      <div class="guide-chip"><b>|x|</b> or <b>Abs(x)</b></div>
      <div class="guide-chip"><b>|x - 2|</b> <span class="arrow">→</span> |x-2|</div>
    </div>
  </div>

  <div class="guide-highlight">
    ✨ <b>Equation form bhi chalti hai!</b> &nbsp;
    <code>3x - e^x = 0</code> likhein — parser automatically right side strip karega!<br>
    Yani <code>sin(x) - 0.5 = 0</code> bhi valid input hai.
  </div>

  <div class="guide-warn">
    ❌ <b>Ye cheezein avoid karein:</b><br>
    • <code>2/(x-4)</code> mein x=4 singularity hai — bounds mein 4 mat rakhein<br>
    • <code>ln(x)</code> ke liye x &gt; 0 chahiye — negative x se domain error aata hai<br>
    • <code>asin(x)</code> / <code>acos(x)</code> ke liye strictly -1 ≤ x ≤ 1 chahiye<br>
    • <code>sqrt(x)</code> ke liye x ≥ 0 chahiye
  </div>
  <div class="guide-ok">
    💡 <b>Pro Tips:</b><br>
    • <code>x**2</code> aur <code>x^2</code> dono same hain<br>
    • Spaces allowed hain: <code>sin( x ) + 2 x</code> bhi theek hai<br>
    • <code>3x</code> likhein, <code>3*x</code> likhne ki zaroorat nahi<br>
    • Bisection mein ensure karein k f(a) aur f(b) ke signs opposite hon (sign change)
  </div>
</div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# INTERNAL ERROR DISPLAY
# ─────────────────────────────────────────────────────────────────────────────

def _show_parse_error(original: str, detail: str, was_equation: bool = False):
    """Show a styled, helpful error when parsing fails."""

    # Give user a targeted hint based on what they typed
    hint = "Look at the Function Input Guide above — it contains the allowed syntax and examples."
    low = original.lower()
    if '=' in original and not was_equation:
        hint = "💡 Equation form? Just write the f(x) side. e.g. <code>3x - e^x</code> (without '= 0')"
    elif 'e^' in low or 'e**' in low:
        hint = "💡 <code>e^x</code> ya <code>exp(x)</code> — Both are valid. Try: <code>e^x</code>"
    elif any(w in low for w in ['ln', 'log']):
        hint = "💡 Log syntax: <code>ln(x)</code>, <code>log(x)</code>, <code>log2(x)</code>, <code>log10(x)</code>"
    elif any(w in low for w in ['sin', 'cos', 'tan']):
        hint = "💡 Trig syntax: <code>sin(x)</code>, <code>cos(2x)</code>, <code>tan(x/2)</code>"

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(239,68,68,.08), rgba(239,68,68,.04));
        border: 1px solid rgba(239,68,68,.5);
        border-radius: 14px;
        padding: 1.1rem 1.4rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: .78rem;
        animation: shake .35s ease;
        margin-top: .5rem;
    ">
    <div style="color:#ef4444; font-size:.9rem; font-weight:700; margin-bottom:.6rem;">
        ✗ Parse Error
    </div>
    <div style="margin-bottom:.4rem;">
        <span style="color:#64748b;">Input:</span>
        <code style="color:#fde68a; background:rgba(255,255,255,.05);
                     padding:.1rem .4rem; border-radius:4px;">{original}</code>
    </div>
    <div style="margin-bottom:.8rem;">
        <span style="color:#64748b;">Detail:</span>
        <span style="color:#f87171;">{detail}</span>
    </div>
    <div style="
        background: rgba(0,0,0,.2);
        border-left: 2px solid #64748b;
        padding: .4rem .7rem;
        border-radius: 0 6px 6px 0;
        color: #94a3b8;
        font-size: .72rem;
    ">↳ {hint}</div>
    </div>
    <style>
    @keyframes shake {{
        0%,100% {{ transform:translateX(0); }}
        25%      {{ transform:translateX(-5px); }}
        75%      {{ transform:translateX(5px); }}
    }}
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SHARED UI COMPONENTS
# ─────────────────────────────────────────────────────────────────────────────

def display_iteration_table(data: list):
    """
    Iteration steps ko pandas DataFrame ki tarah display karta hai.
    data: list of dicts (each dict is one iteration row)
    """
    if not data:
        return
    df = pd.DataFrame(data)
    df.index = range(1, len(df) + 1)
    df.index.name = "Iteration"
    st.dataframe(df, use_container_width=True)


def plot_function(func, x_range: tuple, roots=None, title="Function Plot"):
    """
    Function plot karta hai given x_range mein.
    roots: list of root x-values (optional, amber dots lagata hai)
    """
    x_vals = np.linspace(x_range[0], x_range[1], 500)
    try:
        y_vals = func(x_vals)
    except Exception:
        st.error("Plotting error: function could not be evaluated over the range.")
        return

    fig, ax = plt.subplots(figsize=(9, 4.5))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#111827')
    ax.tick_params(colors='#94a3b8', labelsize=9)
    ax.xaxis.label.set_color('#94a3b8')
    ax.yaxis.label.set_color('#94a3b8')
    ax.title.set_color('#e2e8f0')
    for spine in ax.spines.values():
        spine.set_edgecolor('#1e3a5f')
    ax.grid(True, color='#1e3a5f', linewidth=0.5, linestyle='--', alpha=0.5)

    ax.plot(x_vals, y_vals, color='#00d4ff', linewidth=2.2, label='f(x)')
    ax.axhline(0, color='#334155', linewidth=1, linestyle='-')
    ax.axvline(0, color='#334155', linewidth=1, linestyle='-')

    if roots:
        for r in roots:
            try:
                ax.plot(r, func(r), 'o', color='#f59e0b',
                        markersize=10, zorder=6,
                        label=f'Root ≈ {r:.6f}',
                        markeredgecolor='#fde68a', markeredgewidth=1.5)
                ax.axvline(r, color='#f59e0b', linewidth=1,
                           linestyle='--', alpha=0.5)
            except Exception:
                pass

    ax.set_title(title, color='#e2e8f0', fontsize=11, fontweight='bold')
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend(facecolor='#111827', edgecolor='#1e3a5f',
              labelcolor='#e2e8f0', fontsize=9)
    st.pyplot(fig)
    plt.close(fig)
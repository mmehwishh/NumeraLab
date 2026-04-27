"""
helpers.py - Utility functions shared across all labs
Yahan common helper functions hain jaise function parsing, table display, etc.
"""

import numpy as np
import sympy as sp
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def parse_function(func_str: str):
    """
    User ka string input (e.g. "x**2 - 4") ko callable Python function mein convert karta hai.
    Returns: (callable, sympy_expr) ya (None, None) agar error ho.
    """
    x = sp.Symbol('x')
    try:
        expr = sp.sympify(func_str)
        func = sp.lambdify(x, expr, modules=['numpy'])
        return func, expr
    except Exception as e:
        st.error(f"❌ Function parse error: {e}")
        return None, None


def parse_ode(func_str: str):
    """
    ODE ke liye f(x, y) string parse karta hai.
    e.g. "x + y", "x*y - 2"
    Returns: callable(x, y) ya None
    """
    x, y = sp.symbols('x y')
    try:
        expr = sp.sympify(func_str)
        func = sp.lambdify((x, y), expr, modules=['numpy'])
        return func
    except Exception as e:
        st.error(f"❌ ODE parse error: {e}")
        return None


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
    ax.plot(x_vals, y_vals, 'b-', linewidth=2, label='f(x)')
    ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
    ax.axvline(0, color='black', linewidth=0.8, linestyle='--')

    if roots:
        for r in roots:
            ax.plot(r, func(r), 'ro', markersize=8, label=f'Root ≈ {r:.6f}')

    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)

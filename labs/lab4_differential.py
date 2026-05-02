"""
lab4_differential.py - Lab 4: Ordinary Differential Equations
==============================================================
Methods:
  1. Euler Method          -> euler_method()
  2. Modified Euler Method -> modified_euler()
  3. Heun's Method         -> heuns_method()

Main UI function:
  render_lab4()
"""

import numpy as np
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.helpers import parse_ode


# ─────────────────────────────────────────────
# METHOD 1: EULER METHOD
# ─────────────────────────────────────────────
def euler_method(func, x0: float, y0: float, x_end: float, h: float):
    x_vals = [x0]
    y_vals = [y0]
    table = []
    x, y = x0, y0
    while x < x_end - 1e-12:
        fxy = func(x, y)
        y_next = y + h * fxy
        x_next = round(x + h, 12)
        table.append({'x': round(x, 8), 'y': round(y, 8),
                      'f(x,y)': round(fxy, 8), 'y_next': round(y_next, 8)})
        x, y = x_next, y_next
        x_vals.append(x)
        y_vals.append(y)
    return x_vals, y_vals, table


# ─────────────────────────────────────────────
# METHOD 2: MODIFIED EULER
# ─────────────────────────────────────────────
def modified_euler(func, x0: float, y0: float, x_end: float, h: float):
    x_vals = [x0]
    y_vals = [y0]
    table = []
    x, y = x0, y0
    while x < x_end - 1e-12:
        k1 = func(x, y)
        k2 = func(x + h, y + h * k1)
        y_next = y + (h / 2) * (k1 + k2)
        x_next = round(x + h, 12)
        table.append({'x': round(x, 8), 'y': round(y, 8),
                      'k1': round(k1, 8), 'k2': round(k2, 8),
                      'y_next': round(y_next, 8)})
        x, y = x_next, y_next
        x_vals.append(x)
        y_vals.append(y)
    return x_vals, y_vals, table


# ─────────────────────────────────────────────
# METHOD 3: HEUN'S METHOD
# ─────────────────────────────────────────────
def heuns_method(func, x0: float, y0: float, x_end: float, h: float):
    x_vals = [x0]
    y_vals = [y0]
    table = []
    x, y = x0, y0
    while x < x_end - 1e-12:
        fxy = func(x, y)
        y_pred = y + h * fxy
        y_next = y + (h / 2) * (fxy + func(x + h, y_pred))
        x_next = round(x + h, 12)
        table.append({'x': round(x, 8), 'y': round(y, 8),
                      'y_pred': round(y_pred, 8), 'y_corrected': round(y_next, 8)})
        x, y = x_next, y_next
        x_vals.append(x)
        y_vals.append(y)
    return x_vals, y_vals, table


# ─────────────────────────────────────────────
# PLOT
# ─────────────────────────────────────────────
def plot_ode_solution(x_vals, y_vals, method_name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines+markers',
        name='y(x)', line=dict(color='#22d3ee', width=2.5, shape='spline'),
        marker=dict(size=6, color='#a78bfa', line=dict(width=1.5, color='#ddd6fe')),
        hovertemplate='x=%{x:.4f}<br>y=%{y:.6f}<extra></extra>'))
    fig.add_trace(go.Scatter(x=[x_vals[0]], y=[y_vals[0]], mode='markers',
        name=f'Initial ({x_vals[0]}, {y_vals[0]})',
        marker=dict(size=12, color='#fbbf24', symbol='diamond',
        line=dict(width=2, color='#fef3c7'))))

    fig.update_layout(
        title=f'{method_name} — Solution Curve',
        height=450, plot_bgcolor='#0c1021', paper_bgcolor='#07090f',
        font=dict(family='Inter', color='#8b95b0', size=12),
        legend=dict(bgcolor='rgba(12,16,33,0.9)', bordercolor='rgba(34,211,238,0.1)',
            font=dict(size=10, color='#e8ecf4'), orientation='h',
            yanchor='bottom', y=-0.25, xanchor='center', x=0.5),
        margin=dict(l=50, r=25, t=50, b=70),
        xaxis=dict(title='x', gridcolor='rgba(30,41,59,0.5)', zerolinecolor='#1e293b',
            tickfont=dict(color='#4b5574', family='JetBrains Mono')),
        yaxis=dict(title='y', gridcolor='rgba(30,41,59,0.5)', zerolinecolor='#1e293b',
            tickfont=dict(color='#4b5574', family='JetBrains Mono')),
    )
    return fig


# ─────────────────────────────────────────────
# STREAMLIT UI
# ─────────────────────────────────────────────
def render_lab4():
    st.header("📈 Lab 4: Differential Equations")
    st.markdown("First-order ODE **dy/dx = f(x,y)** numerically solve.")

    method = st.selectbox("Select Method", [
        "Euler Method",
        "Modified Euler Method",
        "Heun's Method"
    ], key="lab4_method")

    ode_str = st.text_input("dy/dx = f(x, y)", value="x + y", key="lab4_ode",
        placeholder="e.g. x + y, x*y - 2, sin(x)*y")

    col1, col2 = st.columns(2)
    with col1:
        x0 = st.number_input("Initial x₀", value=0.0, step=0.1, key="lab4_x0")
        y0 = st.number_input("Initial y₀", value=1.0, step=0.1, key="lab4_y0")
    with col2:
        x_end = st.number_input("Final x", value=2.0, step=0.1, key="lab4_xend")
        h = st.number_input("Step size h", value=0.2, step=0.05, min_value=0.001, key="lab4_h")

    if st.button("Calculate", key="lab4_calc", use_container_width=True, type="primary"):
        func = parse_ode(ode_str)
        if func is None:
            return

        if x_end <= x0:
            st.error("❌ Final x must be greater than x₀.")
            return

        with st.spinner("Computing..."):
            if method == "Euler Method":
                x_vals, y_vals, table = euler_method(func, x0, y0, x_end, h)
            elif method == "Modified Euler Method":
                x_vals, y_vals, table = modified_euler(func, x0, y0, x_end, h)
            else:
                x_vals, y_vals, table = heuns_method(func, x0, y0, x_end, h)

        st.success(f"✅ y({x_end}) ≈ **{y_vals[-1]:.8f}** using {method}")

        # Results table
        with st.expander("Step-by-Step Table", expanded=True):
            df = pd.DataFrame(table)
            df.index = df.index + 1
            df.index.name = "Step"
            st.dataframe(df, use_container_width=True)

        # Solution summary
        c1, c2, c3 = st.columns(3)
        c1.metric("Final y", f"{y_vals[-1]:.6f}")
        c2.metric("Steps", f"{len(table)}")
        c3.metric("Step Size", f"{h}")

        # Plot
        fig = plot_ode_solution(x_vals, y_vals, method)
        st.plotly_chart(fig, use_container_width=True)

"""
lab2_interpolation.py - Lab 2: Interpolation Methods
======================================================
Methods:
  1. Lagrange Interpolation         -> lagrange_interpolation()
  2. Newton Forward Difference       -> newton_forward_difference()
  3. Newton Divided Difference       -> newton_divided_difference()

Main UI function:
  render_lab2()
"""

import numpy as np
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# ─────────────────────────────────────────────
# METHOD 1: LAGRANGE INTERPOLATION
# ─────────────────────────────────────────────
def lagrange_interpolation(x_points: list, y_points: list, x_query: float):
    n = len(x_points)
    Li_list = []
    result = 0.0
    for i in range(n):
        Li = 1.0
        for j in range(n):
            if j != i:
                Li *= (x_query - x_points[j]) / (x_points[i] - x_points[j])
        Li_list.append(Li)
        result += y_points[i] * Li
    return result, Li_list


# ─────────────────────────────────────────────
# METHOD 2: NEWTON FORWARD DIFFERENCE
# ─────────────────────────────────────────────
def newton_forward_difference(x_points: list, y_points: list, x_query: float):
    n = len(x_points)
    h = x_points[1] - x_points[0]
    s = (x_query - x_points[0]) / h

    # Build forward difference table
    diff_table = [[0.0] * n for _ in range(n)]
    for i in range(n):
        diff_table[i][0] = y_points[i]
    for j in range(1, n):
        for i in range(n - j):
            diff_table[i][j] = diff_table[i + 1][j - 1] - diff_table[i][j - 1]

    # Apply Newton forward formula
    result = diff_table[0][0]
    s_term = 1.0
    for k in range(1, n):
        s_term *= (s - (k - 1)) / k
        result += s_term * diff_table[0][k]

    return result, diff_table


# ─────────────────────────────────────────────
# METHOD 3: NEWTON DIVIDED DIFFERENCE
# ─────────────────────────────────────────────
def newton_divided_difference(x_points: list, y_points: list, x_query: float):
    n = len(x_points)
    div_table = [[0.0] * n for _ in range(n)]
    for i in range(n):
        div_table[i][0] = y_points[i]
    for j in range(1, n):
        for i in range(n - j):
            div_table[i][j] = (div_table[i + 1][j - 1] - div_table[i][j - 1]) / (x_points[i + j] - x_points[i])

    # Evaluate polynomial
    result = div_table[0][0]
    prod = 1.0
    for k in range(1, n):
        prod *= (x_query - x_points[k - 1])
        result += div_table[0][k] * prod

    return result, div_table


# ─────────────────────────────────────────────
# PLOTTING
# ─────────────────────────────────────────────
def plot_interpolation(x_points, y_points, x_query, y_result, method_name):
    x_min, x_max = min(x_points) - 1, max(x_points) + 1
    x_fine = np.linspace(x_min, x_max, 300)

    # Evaluate interpolation curve using Lagrange for all methods
    y_fine = []
    for xv in x_fine:
        val, _ = lagrange_interpolation(list(x_points), list(y_points), float(xv))
        y_fine.append(val)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_fine, y=y_fine, mode='lines', name='P(x)',
        line=dict(color='#22d3ee', width=2.5, shape='spline'),
        hovertemplate='x=%{x:.4f}<br>P(x)=%{y:.6f}<extra></extra>'))
    fig.add_trace(go.Scatter(x=list(x_points), y=list(y_points), mode='markers',
        name='Data Points', marker=dict(size=10, color='#a78bfa',
        line=dict(width=2, color='#ddd6fe')),
        hovertemplate='x=%{x}<br>y=%{y}<extra></extra>'))
    fig.add_trace(go.Scatter(x=[x_query], y=[y_result], mode='markers+text',
        name=f'Query ({x_query:.4f}, {y_result:.6f})',
        marker=dict(size=13, color='#fbbf24', symbol='diamond',
        line=dict(width=2, color='#fef3c7')),
        text=[f'  {y_result:.4f}'], textposition='top right',
        textfont=dict(color='#fde68a', size=11, family='JetBrains Mono')))

    fig.update_layout(
        title=f'{method_name} Interpolation',
        height=450, plot_bgcolor='#0c1021', paper_bgcolor='#07090f',
        font=dict(family='Inter', color='#8b95b0', size=12),
        legend=dict(bgcolor='rgba(12,16,33,0.9)', bordercolor='rgba(34,211,238,0.1)',
            font=dict(size=10, color='#e8ecf4'), orientation='h',
            yanchor='bottom', y=-0.25, xanchor='center', x=0.5),
        margin=dict(l=50, r=25, t=50, b=70),
        xaxis=dict(gridcolor='rgba(30,41,59,0.5)', zerolinecolor='#1e293b',
            tickfont=dict(color='#4b5574', family='JetBrains Mono')),
        yaxis=dict(gridcolor='rgba(30,41,59,0.5)', zerolinecolor='#1e293b',
            tickfont=dict(color='#4b5574', family='JetBrains Mono')),
    )
    return fig


# ─────────────────────────────────────────────
# STREAMLIT UI
# ─────────────────────────────────────────────
def render_lab2():
    st.header("📐 Lab 2: Interpolation Methods")
    st.markdown("Known data points se unknown values estimate karo.")

    method = st.selectbox("Select Method", [
        "Lagrange Interpolation",
        "Newton Forward Difference",
        "Newton Divided Difference"
    ], key="lab2_method")

    col1, col2 = st.columns(2)
    with col1:
        x_str = st.text_input("x values (comma separated)", value="1, 2, 3, 4", key="lab2_x")
    with col2:
        y_str = st.text_input("y values (comma separated)", value="1, 4, 9, 16", key="lab2_y")

    x_query = st.number_input("Interpolation point (x_query)", value=2.5, step=0.1, key="lab2_xq")

    if st.button("Calculate", key="lab2_calc", use_container_width=True, type="primary"):
        try:
            x_pts = [float(v.strip()) for v in x_str.split(",")]
            y_pts = [float(v.strip()) for v in y_str.split(",")]
        except ValueError:
            st.error("❌ Invalid input. Enter comma-separated numbers.")
            return

        if len(x_pts) != len(y_pts):
            st.error("❌ x and y must have the same number of values.")
            return
        if len(x_pts) < 2:
            st.error("❌ At least 2 data points required.")
            return

        with st.spinner("Computing..."):
            if method == "Lagrange Interpolation":
                result, Li_list = lagrange_interpolation(x_pts, y_pts, x_query)
                st.success(f"✅ P({x_query}) = **{result:.8f}**")

                # Show Li values
                li_df = pd.DataFrame({
                    'i': list(range(len(Li_list))),
                    'x_i': x_pts,
                    'y_i': y_pts,
                    'L_i(x)': [round(v, 8) for v in Li_list],
                    'y_i * L_i': [round(y_pts[i] * Li_list[i], 8) for i in range(len(Li_list))]
                })
                li_df.index = li_df.index + 1
                with st.expander("Basis Polynomials L_i", expanded=True):
                    st.dataframe(li_df, use_container_width=True)

            elif method == "Newton Forward Difference":
                result, diff_table = newton_forward_difference(x_pts, y_pts, x_query)
                st.success(f"✅ P({x_query}) = **{result:.8f}**")

                n = len(x_pts)
                headers = ['y'] + [f'Δ{k}y' for k in range(1, n)]
                table_data = []
                for i in range(n):
                    row = {}
                    row['x'] = x_pts[i]
                    for j in range(n - i):
                        row[headers[j]] = round(diff_table[i][j], 6)
                    table_data.append(row)
                with st.expander("Forward Difference Table", expanded=True):
                    st.dataframe(pd.DataFrame(table_data), use_container_width=True)

            elif method == "Newton Divided Difference":
                result, div_table = newton_divided_difference(x_pts, y_pts, x_query)
                st.success(f"✅ P({x_query}) = **{result:.8f}**")

                n = len(x_pts)
                headers = ['f[.]'] + [f'f[{"."*(k+1)}]' for k in range(1, n)]
                table_data = []
                for i in range(n):
                    row = {'x': x_pts[i]}
                    for j in range(n - i):
                        row[headers[j]] = round(div_table[i][j], 6)
                    table_data.append(row)
                with st.expander("Divided Difference Table", expanded=True):
                    st.dataframe(pd.DataFrame(table_data), use_container_width=True)

            # Plot
            fig = plot_interpolation(x_pts, y_pts, x_query, result, method)
            st.plotly_chart(fig, use_container_width=True)

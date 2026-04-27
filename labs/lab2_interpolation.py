"""
lab2_interpolation.py - Lab 2: Interpolation Methods
======================================================
Teen methods:
  1. Lagrange Interpolation         -> lagrange_interpolation()
  2. Newton Forward Difference       -> newton_forward_difference()
  3. Newton Divided Difference       -> newton_divided_difference()

Main UI function:
  render_lab2()

TODO list:
  - [ ] lagrange_interpolation() implement karo
  - [ ] newton_forward_difference() implement karo
  - [ ] newton_divided_difference() implement karo
  - [ ] render_lab2() UI complete karo
"""

import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ─────────────────────────────────────────────
# METHOD 1: LAGRANGE INTERPOLATION
# ─────────────────────────────────────────────
def lagrange_interpolation(x_points: list, y_points: list, x_query: float):
    """
    Lagrange Interpolation Formula.

    Parameters:
        x_points : list of float - known x values
        y_points : list of float - known y values (f(x))
        x_query  : float         - point jahan interpolate karna hai

    Returns:
        result   : float  - interpolated y value
        steps    : list   - list of Li values (basis polynomials)

    TODO:
        1. n = len(x_points)
        2. Har i ke liye Li(x) calculate karo:
              Li = product of (x_query - x_j)/(x_i - x_j) for all j != i
        3. result = sum of y_points[i] * Li for all i
        4. Return (result, Li_list)
    """
    # TODO: Apna code yahan likhna hai
    raise NotImplementedError("lagrange_interpolation() implement karo!")


# ─────────────────────────────────────────────
# METHOD 2: NEWTON FORWARD DIFFERENCE
# ─────────────────────────────────────────────
def newton_forward_difference(x_points: list, y_points: list, x_query: float):
    """
    Newton's Forward Difference Interpolation.
    (Equally spaced data ke liye)

    Parameters:
        x_points : list of float - equally spaced x values
        y_points : list of float - corresponding y values
        x_query  : float         - interpolation point

    Returns:
        result   : float
        diff_table: 2D list - forward difference table

    TODO:
        1. h = x_points[1] - x_points[0]  (spacing)
        2. s = (x_query - x_points[0]) / h
        3. Forward difference table banao (delta^k y)
        4. Newton forward formula apply karo:
              P(x) = y0 + s*Δy0 + s(s-1)/2! * Δ²y0 + ...
        5. Return (result, diff_table)
    """
    # TODO: Apna code yahan likhna hai
    raise NotImplementedError("newton_forward_difference() implement karo!")


# ─────────────────────────────────────────────
# METHOD 3: NEWTON DIVIDED DIFFERENCE
# ─────────────────────────────────────────────
def newton_divided_difference(x_points: list, y_points: list, x_query: float):
    """
    Newton's Divided Difference Interpolation.
    (Unequally spaced data ke liye bhi kaam karta hai)

    Parameters:
        x_points : list of float
        y_points : list of float
        x_query  : float

    Returns:
        result     : float
        div_table  : 2D list - divided difference table

    TODO:
        1. Divided difference table banao:
              f[xi] = yi
              f[xi, xi+1] = (f[xi+1] - f[xi]) / (xi+1 - xi)
              ... aur aage
        2. Coefficients = first row of each order
        3. Newton polynomial:
              P(x) = f[x0] + f[x0,x1](x-x0) + f[x0,x1,x2](x-x0)(x-x1) + ...
        4. Return (result, div_table)
    """
    # TODO: Apna code yahan likhna hai
    raise NotImplementedError("newton_divided_difference() implement karo!")


# ─────────────────────────────────────────────
# STREAMLIT UI
# ─────────────────────────────────────────────
def render_lab2():
    """
    Lab 2 Streamlit UI.

    TODO:
        1. Method select karo (Lagrange / Newton Forward / Newton Divided)
        2. Data points input karo - st.text_area se comma separated values
           e.g. x_points: "1, 2, 3, 4"
                y_points: "1, 4, 9, 16"
        3. x_query input karo (kahan interpolate karna hai)
        4. Calculate button par:
              - string ko list mein convert karo
              - Method call karo
              - Result display karo
              - Table aur graph dikhao
    """
    st.header("📐 Lab 2: Interpolation Methods")
    st.markdown("Known data points se unknown values estimate karo.")

    # TODO: UI yahan add karo
    st.info("⚙️ UI implementation pending - TODO comments follow karo!")

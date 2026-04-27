"""
lab3_integration.py - Lab 3: Numerical Integration
====================================================
Teen methods:
  1. Trapezoidal Rule   -> trapezoidal_rule()
  2. Simpson's Rule     -> simpsons_rule()
  3. Midpoint Rule      -> midpoint_rule()

Main UI function:
  render_lab3()

TODO list:
  - [ ] trapezoidal_rule() implement karo
  - [ ] simpsons_rule() implement karo
  - [ ] midpoint_rule() implement karo
  - [ ] render_lab3() UI complete karo
  - [ ] Area visualization add karo
"""

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from utils.helpers import parse_function


# ─────────────────────────────────────────────
# METHOD 1: TRAPEZOIDAL RULE
# ─────────────────────────────────────────────
def trapezoidal_rule(func, a: float, b: float, n: int):
    """
    Trapezoidal Rule for numerical integration.

    Parameters:
        func : callable - f(x)
        a, b : float    - integration limits
        n    : int      - number of subintervals

    Returns:
        result : float  - approximate integral value
        x_vals : array  - x points used
        y_vals : array  - y values at those points

    TODO:
        1. h = (b - a) / n
        2. x_vals = [a, a+h, a+2h, ..., b]
        3. Trapezoidal formula:
              I ≈ (h/2) * [f(a) + 2*f(x1) + 2*f(x2) + ... + 2*f(x_{n-1}) + f(b)]
        4. Return (result, x_vals, y_vals)
    """
    # TODO: Apna code yahan likhna hai
    raise NotImplementedError("trapezoidal_rule() implement karo!")


# ─────────────────────────────────────────────
# METHOD 2: SIMPSON'S RULE
# ─────────────────────────────────────────────
def simpsons_rule(func, a: float, b: float, n: int):
    """
    Simpson's 1/3 Rule.
    Note: n even hona chahiye!

    Parameters:
        func : callable
        a, b : float
        n    : int (must be even)

    Returns:
        result : float
        x_vals : array
        y_vals : array

    TODO:
        1. Agar n odd hai to error/warning do
        2. h = (b - a) / n
        3. Simpson formula:
              I ≈ (h/3) * [f(x0) + 4f(x1) + 2f(x2) + 4f(x3) + ... + 4f(x_{n-1}) + f(xn)]
              (coefficients: 1, 4, 2, 4, 2, ..., 4, 1)
        4. Return (result, x_vals, y_vals)
    """
    # TODO: Apna code yahan likhna hai
    raise NotImplementedError("simpsons_rule() implement karo!")


# ─────────────────────────────────────────────
# METHOD 3: MIDPOINT RULE
# ─────────────────────────────────────────────
def midpoint_rule(func, a: float, b: float, n: int):
    """
    Midpoint Rule.

    Parameters:
        func : callable
        a, b : float
        n    : int - number of subintervals

    Returns:
        result : float
        mid_points : array - midpoints of each subinterval
        y_vals : array

    TODO:
        1. h = (b - a) / n
        2. Midpoints = [a + h/2, a + 3h/2, a + 5h/2, ...]
        3. I ≈ h * sum(f(midpoints))
        4. Return (result, midpoints, y_vals)
    """
    # TODO: Apna code yahan likhna hai
    raise NotImplementedError("midpoint_rule() implement karo!")


def plot_integration(func, a, b, x_vals, method_name):
    """
    Integration area visualize karta hai.

    TODO:
        1. Function curve plot karo
        2. Area fill karo (ax.fill_between)
        3. Subintervals dikhao
        4. Title, labels, grid lagao
    """
    # TODO: Plotting code yahan likhna hai
    pass


# ─────────────────────────────────────────────
# STREAMLIT UI
# ─────────────────────────────────────────────
def render_lab3():
    """
    Lab 3 Streamlit UI.

    TODO:
        1. Method select karo
        2. Function string input lo (e.g. "x**2", "sin(x)")
        3. a, b (limits) aur n (subintervals) input lo
        4. Simpson ke liye n even validate karo
        5. Calculate par:
              - Function parse karo
              - Method call karo
              - Result display karo
              - plot_integration() se area dikhao
    """
    st.header("∫ Lab 3: Numerical Integration")
    st.markdown("Definite integral ka approximate value nikalo.")

    # TODO: UI yahan add karo
    st.info("⚙️ UI implementation pending - TODO comments follow karo!")

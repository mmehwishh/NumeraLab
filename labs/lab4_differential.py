"""
lab4_differential.py - Lab 4: Ordinary Differential Equations
==============================================================
Teen methods:
  1. Euler Method          -> euler_method()
  2. Modified Euler Method -> modified_euler()
  3. Heun's Method         -> heuns_method()

Main UI function:
  render_lab4()

TODO list:
  - [ ] euler_method() implement 
  - [ ] modified_euler() implement 
  - [ ] heuns_method() implement 
  - [ ] render_lab4() UI complete 
  - [ ] Solution curve plot 
"""

import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.helpers import parse_ode


# ─────────────────────────────────────────────
# METHOD 1: EULER METHOD
# ─────────────────────────────────────────────
def euler_method(func, x0: float, y0: float, x_end: float, h: float):
    """
    Euler's Method for solving dy/dx = f(x, y).

    Parameters:
        func  : callable - f(x, y)
        x0    : float    - initial x
        y0    : float    - initial y (condition)
        x_end : float    - end x value
        h     : float    - step size

    Returns:
        x_vals : list of float
        y_vals : list of float
        table  : list of dicts (for display)

    TODO:
        1. x_vals = [x0], y_vals = [y0]
        2. Loop karo jab tak x < x_end:
              y_next = y + h * f(x, y)
              x_next = x + h
        3. Har step ka dict: {'x': x, 'y': y, 'f(x,y)': func(x,y), 'y_next': y_next}
        4. Return (x_vals, y_vals, table)
    """
    # TODO: implemnnet code here
    raise NotImplementedError("euler_method() implement !")


# ─────────────────────────────────────────────
# METHOD 2: MODIFIED EULER
# ─────────────────────────────────────────────
def modified_euler(func, x0: float, y0: float, x_end: float, h: float):
    """
    Modified Euler Method (Improved Euler).

    Parameters:
        Same as euler_method()

    Returns:
        x_vals, y_vals, table

    TODO:
        1. Loop karo:
              k1 = f(x, y)                          (slope at start)
              k2 = f(x + h, y + h*k1)               (slope at end - predicted)
              y_next = y + (h/2) * (k1 + k2)        (average slope use karo)
        2. Iteration dict: {'x': x, 'y': y, 'k1': k1, 'k2': k2, 'y_next': y_next}
        3. Return (x_vals, y_vals, table)
    """
    # TODO: Apna code yahan likhna hai
    raise NotImplementedError("modified_euler() implement karo!")


# ─────────────────────────────────────────────
# METHOD 3: HEUN'S METHOD
# ─────────────────────────────────────────────
def heuns_method(func, x0: float, y0: float, x_end: float, h: float):
    """
    Heun's Method (Predictor-Corrector).

    Parameters:
        Same as euler_method()

    Returns:
        x_vals, y_vals, table

    TODO:
        PREDICTOR step:
              y_pred = y + h * f(x, y)       (predict from eular)

        CORRECTOR step:
              y_next = y + (h/2) * [f(x, y) + f(x+h, y_pred)]

        2. Iteration dict:
              {'x': x, 'y': y, 'y_pred': y_pred, 'y_corrected': y_next}
        3. Return (x_vals, y_vals, table)
    """
    # TODO: Apna code yahan likhna hai
    raise NotImplementedError("heuns_method() implement karo!")


def plot_ode_solution(x_vals, y_vals, method_name):
    """
    ODE solution curve plot karta hai.

    TODO:
        1. x_vals vs y_vals plot karo
        2. Initial point mark karo
        3. Title, labels, grid lagao
    """
    # TODO: Plot code yahan likhna hai
    pass


# ─────────────────────────────────────────────
# STREAMLIT UI
# ─────────────────────────────────────────────
def render_lab4():
    """
    Lab 4 Streamlit UI.

    TODO:
       ODE Solver WorkflowS
       elect Method (Choose the numerical integration method)
       Input Parameters (Final $x$ value ($x_{end}$) and step size ($h$))
       On 'Calculate' Click:
       Parse Function: Convert the ODE string into a callable function using parse_ode()
       Execute Method: Call the selected numerical solver.
       Display Results: Show a table with $x$ and $y$ columns.
    """
    st.header("📈 Lab 4: Differential Equations")
    st.markdown("First-order ODE **dy/dx = f(x,y)** numerically solve .")

    # TODO: UI yahan add karo
    st.info("⚙️ UI implementation pending !")

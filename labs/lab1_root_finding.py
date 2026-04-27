"""
lab1_root_finding.py - Lab 1: Root Finding Methods
====================================================
Is file mein teen methods implement karne hain:
  1. Bisection Method       -> bisection()
  2. Newton-Raphson Method  -> newton_raphson()
  3. Secant Method          -> secant()

Aur ek main Streamlit UI function:
  render_lab1()  -> yeh function app.py se call hoga

TODO list (har method ke andar comments se guide milegi):
  - [ ] bisection() algorithm likho
  - [ ] newton_raphson() algorithm likho  
  - [ ] secant() algorithm likho
  - [ ] render_lab1() mein input widgets complete karo
  - [ ] results aur graphs display karo
"""

import numpy as np
import sympy as sp
import streamlit as st
from utils.helpers import parse_function, display_iteration_table, plot_function


# ─────────────────────────────────────────────
# METHOD 1: BISECTION
# ─────────────────────────────────────────────
def bisection(func, a: float, b: float, tol: float = 1e-6, max_iter: int = 100):
    """
    Bisection Method to find root of func in interval [a, b].

    Parameters:
        func     : callable - the mathematical function
        a, b     : float    - interval endpoints (f(a)*f(b) < 0 hona chahiye)
        tol      : float    - tolerance/error limit
        max_iter : int      - maximum iterations allowed

    Returns:
        root     : float        - approximate root
        iterations: list        - list of dicts with iteration details
        message  : str          - success/failure message

    TODO:
        1. Check karo ke f(a)*f(b) < 0, warna return error message
        2. Loop chalao max_iter tak:
              midpoint c = (a + b) / 2
              agar |f(c)| < tol ya interval bahut chhota ho -> root mil gaya
              agar f(a)*f(c) < 0 -> b = c, warna a = c
        3. Har iteration ka data dict mein store karo:
              {'a': a, 'b': b, 'c': c, 'f(c)': func(c), 'error': abs(b-a)/2}
        4. Return karo (c, iterations_list, message)
    """
    # TODO: Apna code yahan likhna hai
    raise NotImplementedError("bisection() abhi implement nahi hui - TODO dekho upar!")


# ─────────────────────────────────────────────
# METHOD 2: NEWTON-RAPHSON
# ─────────────────────────────────────────────
def newton_raphson(func, func_derivative, x0: float, tol: float = 1e-6, max_iter: int = 100):
    """
    Newton-Raphson Method.

    Parameters:
        func            : callable - f(x)
        func_derivative : callable - f'(x)
        x0              : float    - initial guess
        tol             : float    - tolerance
        max_iter        : int      - max iterations

    Returns:
        root       : float
        iterations : list of dicts
        message    : str

    TODO:
        1. Loop chalao max_iter tak:
              x1 = x0 - f(x0)/f'(x0)
              agar f'(x0) == 0 -> derivative zero error
              agar |x1 - x0| < tol -> converged
              x0 = x1
        2. Iteration dict: {'x0': x0, 'f(x0)': func(x0), "f'(x0)": f_prime, 'x1': x1, 'error': abs(x1-x0)}
        3. Return (x1, iterations_list, message)
    """
    # TODO: Apna code yahan likhna hai
    raise NotImplementedError("newton_raphson() abhi implement nahi hui - TODO dekho upar!")


# ─────────────────────────────────────────────
# METHOD 3: SECANT
# ─────────────────────────────────────────────
def secant(func, x0: float, x1: float, tol: float = 1e-6, max_iter: int = 100):
    """
    Secant Method.

    Parameters:
        func     : callable - f(x)
        x0, x1   : float    - two initial guesses
        tol      : float    - tolerance
        max_iter : int      - max iterations

    Returns:
        root       : float
        iterations : list of dicts
        message    : str

    TODO:
        1. Loop chalao max_iter tak:
              denominator = f(x1) - f(x0)
              agar denominator == 0 -> division by zero error
              x2 = x1 - f(x1) * (x1 - x0) / denominator
              agar |x2 - x1| < tol -> converged
              x0, x1 = x1, x2
        2. Iteration dict: {'x0': x0, 'x1': x1, 'x2': x2, 'f(x2)': func(x2), 'error': abs(x2-x1)}
        3. Return (x2, iterations_list, message)
    """
    # TODO: Apna code yahan likhna hai
    raise NotImplementedError("secant() abhi implement nahi hui - TODO dekho upar!")


# ─────────────────────────────────────────────
# STREAMLIT UI
# ─────────────────────────────────────────────
def render_lab1():
    """
    Lab 1 ka poora Streamlit UI yahan render hoga.
    app.py se yeh function call hoga.

    TODO:
        1. st.selectbox se method choose karwao (Bisection / Newton-Raphson / Secant)
        2. st.text_input se function string lo (e.g. "x**3 - x - 2")
        3. Method ke hisaab se inputs lo (interval ya initial guesses)
        4. Tolerance aur max_iter ke liye st.number_input
        5. "Calculate" button par click hone par:
              - parse_function() se function parse karo
              - Newton ke liye derivative bhi nikalo (sympy se)
              - Selected method call karo
              - Results display karo: root, iterations count, success message
              - display_iteration_table() se iteration table dikhao
              - plot_function() se graph dikhao
    """
    st.header("🔍 Lab 1: Root Finding Methods")
    st.markdown("Nonlinear equation **f(x) = 0** ka root dhundho.")

    # TODO: method selection aur inputs yahan add karo
    st.info("⚙️ UI implementation pending - TODO comments follow karo!")

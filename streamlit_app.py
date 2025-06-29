import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Investment Simulator", layout="wide")

st.title("Investment Simulator")

col1, col2 = st.columns([1, 2.5])

with col1:
    income = st.slider("Current Income ($)", 50_000, 1_500_000, 300_000, step=10_000)
    tax_rate = st.slider("Tax Rate (%)", 0, 60, 38)
    salary_growth = st.slider("Salary Growth Rate (%/year)", 0.0, 20.0, 5.0, step=0.5)
    expenses = st.slider("Annual Cost of Living ($)", 30_000, 300_000, 70_000, step=1_000)
    inflation = st.slider("Inflation Rate (%/year)", 0.0, 10.0, 2.0, step=0.5)
    years = st.slider("Years to Simulate", 1, 40, 10)

    st.subheader("Investment Parameters")
    init_high = st.slider("Initial High-Return Investment ($)", 0, 1_000_000, 50_000, step=10_000)
    high_return = st.slider("Expected High Return (%/year)*", 0.0, 50.0, 35.0, step=1.0)

    init_safe = st.slider("Initial Safe Investment ($)", 0, 1_000_000, 250_000, step=10_000)
    safe_return = st.slider("Expected Safe Return (%/year)", 0.0, 15.0, 10.0, step=0.5)

with col2:
    def simulate_growth(income, tax_rate, salary_growth, expenses, inflation,
                        init_high, high_r, init_safe, safe_r, years):
        high_bal = [init_high]
        safe_bal = [init_safe]

        for _ in range(years):
            net = income * (1 - tax_rate / 100) - expenses
            net = max(0, net)

            high_next = high_bal[-1] * (1 + high_r / 100) + net * 0.8
            safe_next = safe_bal[-1] * (1 + safe_r / 100) + net * 0.2

            high_bal.append(high_next)
            safe_bal.append(safe_next)

            income *= (1 + salary_growth / 100)
            expenses *= (1 + inflation / 100)

        return high_bal, safe_bal

    high, safe = simulate_growth(income, tax_rate, salary_growth, expenses, inflation,
                                 init_high, high_return, init_safe, safe_return, years)

    total = np.array(high) + np.array(safe)
    x = np.arange(0, years + 1)

    # Plot
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, np.array(high) / 1e6, label="High-Return Investment")
    ax.plot(x, np.array(safe) / 1e6, label="Safe Investment")
    ax.plot(x, np.array(total) / 1e6, label="Total Net Worth", linestyle="--", linewidth=2)
    ax.set_xlabel("Year")
    ax.set_ylabel("Value ($M)")
    ax.set_title("Investment Growth Over Time")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    # Clean single-line summary
    st.write(
        f"Final Net Worth: ${total[-1]:,.0f} | "
        f"High-Return Balance: ${high[-1]:,.0f} | "
        f"Safe Investment Balance: ${safe[-1]:,.0f}"
    )

    # TQQQ footnote
    st.caption("*Historical average annual return of TQQQ: ~33% (10y), ~40% (15y), ~30% (since inception).")

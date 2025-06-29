# streamlit_app.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Wealth Growth Simulator", layout="wide")

st.title("📈 High-Return Investment Wealth Simulator")

# --- Layout ---
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Inputs")

    income = st.slider("Current Income ($)", 50_000, 1_500_000, 250_000, step=10_000)
    tax_rate = st.slider("Tax Rate (%)", 0, 60, 40)
    salary_growth = st.slider("Salary Growth Rate (%/year)", 0.0, 20.0, 5.0, step=0.5)
    expenses = st.slider("Annual Cost of Living ($)", 30_000, 300_000, 100_000, step=1_000)
    cost_growth = st.slider("Cost Growth Rate (%/year)", 0.0, 10.0, 2.0, step=0.5)
    years = st.slider("Years to Simulate", 1, 40, 10)

    st.subheader("💸 Investment Parameters")
    init_high = st.slider("Initial High-Return Investment ($)", 0, 1_000_000, 100_000, step=10_000)
    high_return = st.slider("Expected High Return (%/year)", 0.0, 50.0, 35.0, step=1.0)

    init_safe = st.slider("Initial Safe Investment ($)", 0, 1_000_000, 100_000, step=10_000)
    safe_return = st.slider("Expected Safe Return (%/year)", 0.0, 15.0, 7.0, step=0.5)

with col2:
    st.header("📊 Results & Growth Chart")

    def simulate_growth(income, tax_rate, salary_growth, expenses, cost_growth,
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
            expenses *= (1 + cost_growth / 100)

        return high_bal, safe_bal

    high, safe = simulate_growth(income, tax_rate, salary_growth, expenses, cost_growth,
                                 init_high, high_return, init_safe, safe_return, years)

    total = np.array(high) + np.array(safe)
    x = np.arange(0, years + 1)

    st.subheader(f"Final Net Worth: **${total[-1]:,.0f}**")
    st.write(f"• High-Return Balance: **${high[-1]:,.0f}**")
    st.write(f"• Safe Investment Balance: **${safe[-1]:,.0f}**")

    fig, ax = plt.subplots()
    ax.plot(x, high, label="High-Return Investment")
    ax.plot(x, safe, label="Safe Investment")
    ax.plot(x, total, label="Total Net Worth", linestyle="--", linewidth=2)
    ax.set_xlabel("Year")
    ax.set_ylabel("Portfolio Value ($)")
    ax.set_title("Wealth Growth Over Time")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    # --- TQQQ Historical Returns Note ---
    st.markdown("---")
    st.markdown(
        "<small>📌 **Note:** Historical average annual return of TQQQ:<br>"
        "• Past 10 years: ~33% CAGR<br>"
        "• Past 15 years: ~40% CAGR<br>"
        "• Past 20 years (since inception): ~30% CAGR</small>",
        unsafe_allow_html=True
    )

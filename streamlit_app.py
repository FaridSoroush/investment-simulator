# streamlit_app.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="TQQQ Wealth Growth Calculator", layout="centered")

st.title("📈 TQQQ Wealth Growth Simulator")

# Input widgets
income = st.slider("Current Income ($)", 50_000, 1_500_000, 250_000, step=10_000)
tax_rate = st.slider("Tax Rate (%)", 0, 60, 40)
salary_growth = st.slider("Salary Growth Rate (%/year)", 0.0, 20.0, 5.0, step=0.5)
expenses = st.slider("Annual Cost of Living ($)", 30_000, 300_000, 100_000, step=1_000)
cost_growth = st.slider("Cost Growth Rate (%/year)", 0.0, 10.0, 2.0, step=0.5)
years = st.slider("Years to Simulate", 1, 40, 10)

st.markdown("---")

st.subheader("💸 Investment Parameters")
init_tqqq = st.slider("Initial TQQQ Investment ($)", 0, 1_000_000, 100_000, step=10_000)
tqqq_return = st.slider("Expected TQQQ Return (%/year)", 0.0, 50.0, 35.0, step=1.0)

init_safe = st.slider("Initial Safer Investment ($)", 0, 1_000_000, 100_000, step=10_000)
safe_return = st.slider("Expected Safe Return (%/year)", 0.0, 15.0, 7.0, step=0.5)

# Simulation function
def simulate_growth(income, tax_rate, salary_growth, expenses, cost_growth,
                    init_tqqq, tqqq_r, init_safe, safe_r, years):
    net_income = []
    tqqq_bal = [init_tqqq]
    safe_bal = [init_safe]

    for year in range(years):
        net = income * (1 - tax_rate / 100) - expenses
        net = max(0, net)

        tqqq_next = tqqq_bal[-1] * (1 + tqqq_r / 100) + net * 0.8
        safe_next = safe_bal[-1] * (1 + safe_r / 100) + net * 0.2

        tqqq_bal.append(tqqq_next)
        safe_bal.append(safe_next)

        income *= (1 + salary_growth / 100)
        expenses *= (1 + cost_growth / 100)
        net_income.append(net)

    return tqqq_bal, safe_bal

# Run simulation
tqqq, safe = simulate_growth(income, tax_rate, salary_growth, expenses, cost_growth,
                             init_tqqq, tqqq_return, init_safe, safe_return, years)

total = np.array(tqqq) + np.array(safe)
x = np.arange(0, years + 1)

# Show results
st.markdown("## 📊 Results")
st.write(f"**Final Net Worth:** ${total[-1]:,.0f}")
st.write(f"• TQQQ Balance: ${tqqq[-1]:,.0f}")
st.write(f"• Safe Investment Balance: ${safe[-1]:,.0f}")

# Plot
fig, ax = plt.subplots()
ax.plot(x, tqqq, label="TQQQ Portfolio")
ax.plot(x, safe, label="Safe Investment")
ax.plot(x, total, label="Total Net Worth", linestyle="--", linewidth=2)
ax.set_xlabel("Year")
ax.set_ylabel("Portfolio Value ($)")
ax.set_title("Wealth Growth Over Time")
ax.grid(True)
ax.legend()
st.pyplot(fig)

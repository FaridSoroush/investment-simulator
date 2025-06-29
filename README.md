# Investment Simulator

A Streamlit-based interactive simulator for modeling long-term investment growth using income, tax, expense, and portfolio return assumptions.

**Live App:**  
[https://investment-simulator-farid.streamlit.app](https://investment-simulator-farid.streamlit.app)

---

## Overview

This project models the growth of two investment portfolios over time:

- **High-Return Portfolio** (e.g., leveraged ETFs like TQQQ or high-growth equities)
- **Safe Portfolio** (e.g., bonds, treasury funds, or diversified index investments)

Users can interactively adjust financial assumptions such as:

- Annual income, tax rate, and salary growth
- Cost of living and inflation
- Initial investment amounts and expected return rates

Each year, the simulator:

1. Calculates post-tax income
2. Subtracts annual living expenses
3. Allocates surplus (default: 80% to high-return, 20% to safe)
4. Compounds investment growth over a user-defined horizon

---

## Example Use Cases

- Quantifying how expected returns affect long-term wealth
- Modeling different career paths and expense levels
- Comparing portfolio strategies under inflation and tax scenarios
- Visualizing compound growth over time

---

## Screenshot

![Investment Simulator Screenshot](docs/screenshot.png)  <!-- Optional: replace with your own hosted image -->

---

## Tech Stack

- **Python**
- **Streamlit** – interactive web interface and deployment
- **NumPy** – annual financial calculations
- **Matplotlib** – time-series visualizations

---

## Code Snippet

Core investment logic per year:

```python
net = income * (1 - tax_rate / 100) - expenses
high_next = high_balance[-1] * (1 + high_return / 100) + max(0, net) * 0.8
safe_next = safe_balance[-1] * (1 + safe_return / 100) + max(0, net) * 0.2

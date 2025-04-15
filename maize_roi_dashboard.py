
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Maize Loan ROI Calculator", layout="wide")
st.title("🌽 Maize Production Loan & ROI Calculator")

# --- Inputs ---
st.sidebar.header("Input Parameters")
bags = st.sidebar.slider("Bags Harvested (50kg each)", 50, 250, 150)
price_per_bag = st.sidebar.slider("Market Price per Bag (MWK)", 30000, 100000, 60000, step=1000)
loan_type = st.sidebar.selectbox("Loan Repayment Type", ["Bullet Repayment", "Installments (2x)"])
include_insurance = st.sidebar.checkbox("Include Crop Insurance (5%)", value=True)

# --- Fixed values ---
budget = 4452000
processing_fee = 0.055 * budget
interest_rate = 0.022 if loan_type == "Bullet Repayment" else 0.044
interest = interest_rate * budget
insurance = 0.05 * budget if include_insurance else 0

total_loan_repayment = budget + processing_fee + interest + insurance
revenue = bags * price_per_bag
profit = revenue - total_loan_repayment

# --- Output Metrics ---
st.subheader("📊 Financial Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue (MWK)", f"{revenue:,.0f}")
col2.metric("Loan Repayment (MWK)", f"{total_loan_repayment:,.0f}")
col3.metric("Net Profit (MWK)", f"{profit:,.0f}", delta_color="normal")

# --- Chart: Revenue vs Repayment ---
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(["Revenue", "Repayment"], [revenue, total_loan_repayment], color=["green", "red"])
ax.set_ylabel("MWK")
ax.set_title("Revenue vs Loan Repayment")
st.pyplot(fig)

# --- Chart: ROI Sensitivity Analysis ---
st.subheader("📈 ROI Sensitivity (Price per Bag vs Profit)")
price_range = list(range(30000, 100001, 5000))
profits = [(bags * p) - total_loan_repayment for p in price_range]
fig2, ax2 = plt.subplots()
ax2.plot(price_range, profits, marker='o')
ax2.set_xlabel("Price per Bag (MWK)")
ax2.set_ylabel("Profit (MWK)")
ax2.set_title("Profit Sensitivity to Market Price")
ax2.grid(True)
st.pyplot(fig2)

# --- Advisory ---
st.subheader("🧠 Recommendation")
if profit > 0:
    st.success("Your maize production is profitable under the current scenario. Aim to maximize yield and sell when market prices are favorable.")
else:
    st.warning("This scenario results in a loss. Consider increasing production or targeting higher market prices to improve ROI.")

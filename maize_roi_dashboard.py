
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
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# --- Custom Styling ---
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stButton>button {
        color: white;
        background-color: green;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Input Section ---
st.title("Maize Loan ROI Calculator")

# Sidebar for inputs
st.sidebar.header("Input Parameters")
acres = st.sidebar.number_input("Acres of Land", value=5)
fertilizer_cost = st.sidebar.number_input("Fertilizer Cost per Acre", value=10000)
seed_type = st.sidebar.selectbox("Seed Variety", ["Hybrid", "OPV", "Local"])
min_yield = st.sidebar.number_input("Minimum Yield per Acre (kg)", value=200)
max_yield = st.sidebar.number_input("Maximum Yield per Acre (kg)", value=800)
tractor_used = st.sidebar.checkbox("Use Tractor for Plowing?")
tractor_cost = st.sidebar.number_input("Tractor Cost per Acre", value=30000) if tractor_used else 0
labor_cost = st.sidebar.number_input("Labor Cost per Acre", value=5000)

# Add validation for max and min yield
if max_yield <= min_yield:
    st.sidebar.warning("Maximum yield must be greater than minimum yield.")

# --- Calculations ---
# Yield Range
avg_yield = (min_yield + max_yield) / 2

# Total Cost (fertilizer + labor + tractor cost)
total_cost = (fertilizer_cost + labor_cost + tractor_cost) * acres

# Revenue (average yield * price per kg * acres)
price_per_kg = 5  # Example price per kg of maize
revenue = avg_yield * price_per_kg * acres

# ROI (Revenue - Total Cost)
roi = revenue - total_cost

# --- Display Results ---
st.header("Results")
st.write(f"**Total Cost:** {total_cost} (including labor, fertilizer, and tractor)")
st.write(f"**Revenue from {acres} Acres:** {revenue}")
st.write(f"**Return on Investment (ROI):** {roi}")

# --- Plot Results ---
# Simple bar chart for cost vs revenue
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(["Total Cost", "Revenue"], [total_cost, revenue], color=["red", "green"])
ax.set_title("Cost vs Revenue")
st.pyplot(fig)

# --- Yield vs ROI Graph (Interactive) ---
# Using Plotly for interactivity
data = {
    "Acres": [acres],
    "Yield": [avg_yield],
    "ROI": [roi],
}
df = pd.DataFrame(data)

fig = px.bar(df, x='Acres', y='ROI', title="ROI vs Acres of Land", color='ROI', 
             labels={'ROI': 'Return on Investment (ROI)', 'Acres': 'Number of Acres'},
             color_continuous_scale='Viridis')
st.plotly_chart(fig, use_container_width=True)

# --- Additional Info ---
st.subheader("Optional: Further Analysis")
st.write("""
If you want to analyze different scenarios (e.g., tractor vs manual labor), modify the inputs in the sidebar. You can experiment with different seed varieties, labor costs, or yields.
""")

# --- Scenario Comparison (Mobile-Responsive) ---
st.subheader("Scenario Comparison")

col1, col2 = st.columns(2)
with col1:
    tractor_scenario = st.radio("Choose Scenario", ("Tractor", "Manual"))
with col2:
    manual_labor_cost = st.number_input("Manual Labor Cost per Acre", value=4000 if tractor_scenario == "Manual" else 0)

# Update tractor cost based on scenario
if tractor_scenario == "Tractor":
    tractor_cost = st.sidebar.number_input("Tractor Cost per Acre", value=30000)

# Update cost and ROI based on scenario
total_cost_scenario = (fertilizer_cost + manual_labor_cost + tractor_cost) * acres
revenue_scenario = avg_yield * price_per_kg * acres
roi_scenario = revenue_scenario - total_cost_scenario

# Display the results of the selected scenario
st.write(f"**Scenario: {tractor_scenario}**")
st.write(f"**Total Cost:** {total_cost_scenario}")
st.write(f"**Revenue:** {revenue_scenario}")
st.write(f"**ROI:** {roi_scenario}")

# --- Download Button (CSV Report) ---
st.subheader("Download Your Report")
csv_data = {
    "Parameter": ["Acres", "Fertilizer Cost", "Labor Cost", "Tractor Cost", "Total Cost", "Revenue", "ROI"],
    "Value": [acres, fertilizer_cost, labor_cost, tractor_cost, total_cost, revenue, roi]
}
df_csv = pd.DataFrame(csv_data)
csv_file = df_csv.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Report",
    data=csv_file,
    file_name="maize_loan_roi_report.csv",
    mime="text/csv"
)

# Final version with full refactor and UI enhancement will be here.
# Due to the length, I will now rebuild it from scratch in a clean, modular way.

import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import datetime

# --- CONFIG ---
st.set_page_config(page_title="🌽 Maize ROI & Farm Management Tool", layout="wide")
st.markdown("""
    <style>
    .sidebar .sidebar-content { background-color: #f0f2f6; padding: 20px; border-radius: 8px; }
    .stButton>button { background-color: #1a936f; color: white; font-weight: bold; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR INPUTS ---
st.sidebar.title("🛠️ Farm Setup & Cost Inputs")
farm_size = st.sidebar.number_input("Farm Size (Acres)", value=5)
bags = st.sidebar.slider("Expected Yield (Bags of 50kg)", 50, 300, 150)
price_per_bag = st.sidebar.slider("Market Price per Bag (MWK)", 30000, 100000, 60000, step=1000)
loan_type = st.sidebar.selectbox("Loan Repayment Type", ["Bullet Repayment", "Installments (2x)"])
include_insurance = st.sidebar.checkbox("Include Crop Insurance (5%)", value=True)

# --- Labor Cost Settings ---
st.sidebar.subheader("💼 Labor Cost Settings")
labor_costs = {
    "Tractor": st.sidebar.number_input("Tractor Cost/Acre", value=30000),
    "Casual": st.sidebar.number_input("Casual Labor Cost/Day", value=2000),
    "Seasonal": st.sidebar.number_input("Seasonal Labor Cost/Day", value=2500)
}

# --- Work Plan Section ---
st.title("🌽 Maize ROI & Mega Farm Planner")
st.header("📋 Customizable Work Plan")
default_plan = pd.DataFrame({
    "Activity": [
        "Land Preparation", "Planting", "Fertilizer Application", "Weeding",
        "Pest Control", "Harvesting", "Post-Harvest Handling"
    ],
    "Start Week": [1, 2, 3, 5, 6, 8, 9],
    "End Week": [1, 2, 3, 5, 6, 8, 10],
    "Labor Type": [
        "Tractor", "Casual", "Casual", "Seasonal",
        "Casual", "Seasonal", "Seasonal"
    ]
})
editable_plan = st.data_editor(default_plan, use_container_width=True, num_rows="dynamic")

# --- Validate Work Plan and Estimate Labor ---
validated_rows = []
for _, row in editable_plan.iterrows():
    start, end = int(row["Start Week"]), int(row["End Week"])
    duration = max(end - start + 1, 0)
    cost = labor_costs.get(row["Labor Type"], 0) * duration * 5 if row["Labor Type"] != "Tractor" else labor_costs["Tractor"] * farm_size
    validated_rows.append({
        **row,
        "Duration (weeks)": duration,
        "Estimated Cost (MWK)": cost
    })

validated_df = pd.DataFrame(validated_rows)
st.subheader("📊 Labor Summary")
st.dataframe(validated_df, use_container_width=True)
total_labor_cost = validated_df["Estimated Cost (MWK)"].sum()
st.success(f"💰 Total Estimated Labor Cost: MWK {total_labor_cost:,.0f}")

# --- Financial Summary ---
st.header("💵 Financial Overview")
budget = 4452000
processing_fee = 0.055 * budget
interest_rate = 0.022 if loan_type == "Bullet Repayment" else 0.044
interest = interest_rate * budget
insurance = 0.05 * budget if include_insurance else 0
total_loan_repayment = budget + processing_fee + interest + insurance
revenue = bags * price_per_bag
profit = revenue - total_loan_repayment

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"MWK {revenue:,.0f}")
col2.metric("Loan Repayment", f"MWK {total_loan_repayment:,.0f}")
col3.metric("Net Profit", f"MWK {profit:,.0f}", delta_color="normal")

# --- ROI Chart ---
st.subheader("📈 ROI Sensitivity (Price per Bag vs Profit)")
price_range = list(range(30000, 100001, 5000))
profits = [(bags * p) - total_loan_repayment for p in price_range]
fig1, ax1 = plt.subplots()
ax1.plot(price_range, profits, marker='o')
ax1.set_xlabel("Price per Bag (MWK)")
ax1.set_ylabel("Profit (MWK)")
ax1.grid(True)
st.pyplot(fig1)

# --- Gantt Timeline ---
st.subheader("📆 Activity Timeline")
start_date = datetime.date.today()
timeline_data = []
activity_durations = {row['Activity']: row['End Week'] - row['Start Week'] + 1 for _, row in validated_df.iterrows()}

for i, row in validated_df.iterrows():
    start = start_date + datetime.timedelta(weeks=row['Start Week'])
    end = start_date + datetime.timedelta(weeks=row['End Week'])
    timeline_data.append({
        "Task": row['Activity'], "Start": start, "Finish": end, "Type": row['Labor Type']
    })

fig2 = px.timeline(pd.DataFrame(timeline_data), x_start="Start", x_end="Finish", y="Task", color="Type")
fig2.update_yaxes(autorange="reversed")
st.plotly_chart(fig2, use_container_width=True)

# --- Cash Flow Tracker ---
st.subheader("💸 Cash Flow Overview")
total_income = st.number_input("Expected Income (MWK)", value=revenue, step=10000)
cashflow = []
for i, row in validated_df.iterrows():
    week = f"Week {row['Start Week']}"
    cost = row['Estimated Cost (MWK)']
    income = total_income if row['Activity'] == 'Post-Harvest Handling' else 0
    cashflow.append({"Week": week, "Cost": cost, "Income": income, "Net Flow": income - cost})
cf_df = pd.DataFrame(cashflow)

fig3 = px.bar(cf_df, x="Week", y=["Cost", "Income"], barmode="group")
fig4 = px.line(cf_df, x="Week", y="Net Flow", markers=True)
fig4.update_traces(line=dict(color="green", width=3))

st.plotly_chart(fig3, use_container_width=True)
st.plotly_chart(fig4, use_container_width=True)

# --- Advisory ---
st.subheader("🧠 Smart Recommendation")
if profit > 0:
    st.success("✅ Your maize production is profitable under the current assumptions.")
else:
    st.warning("⚠️ This scenario is loss-making. Review inputs or market strategy.")

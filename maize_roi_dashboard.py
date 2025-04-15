import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import datetime

# --- Temporary Workplan Definition (REQUIRED) ---
workplan = pd.DataFrame([
    {"Activity": "Land Preparation", "Labor Type": "Tractor"},
    {"Activity": "Planting", "Labor Type": "Casual"},
    {"Activity": "Fertilizer Application", "Labor Type": "Casual"},
    {"Activity": "Weeding", "Labor Type": "Seasonal"},
    {"Activity": "Pest & Disease Control", "Labor Type": "Casual"},
    {"Activity": "Harvesting", "Labor Type": "Seasonal"},
    {"Activity": "Post-Harvest Handling", "Labor Type": "Seasonal"},
])

st.set_page_config(page_title="Maize Loan ROI Calculator -EEH IWOYI", layout="wide")
st.title("🌽 Maize Production Loan & ROI Calculator")

# --- Inputs ---
st.sidebar.header("Input Parameters")
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

# --- Editable Work Plan ---
st.subheader("📋 Editable Work Plan")
editable_plan = st.data_editor(workplan, use_container_width=True, num_rows="dynamic")

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

# --- Cash Flow Tracker ---
st.subheader("💸 Cash Flow Overview")
total_income = st.number_input("Expected Total Income from Maize Sales (MWK)", value=800000, step=10000)

# Sample costs per task
cost_map = {
    "Land Preparation": 60000,
    "Planting": 30000,
    "Fertilizer Application": 40000,
    "Weeding": 20000,
    "Pest & Disease Control": 15000,
    "Harvesting": 25000,
    "Post-Harvest Handling": 10000
}

cashflow_data = []
for i, row in editable_plan.iterrows():
    activity = row["Activity"]
    week = i + 1
    cost = cost_map.get(activity, 0)
    income = total_income if activity == "Post-Harvest Handling" else 0
    cashflow_data.append({
        "Week": f"Week {week}",
        "Cost": cost,
        "Income": income,
        "Net Flow": income - cost
    })

cf_df = pd.DataFrame(cashflow_data)

# Line chart style with bar overlay
st.write("### Weekly Cash Flow Summary")
fig = px.bar(cf_df, x="Week", y=["Cost", "Income"], barmode="group", title="Farm Cash Flow per Week")
st.plotly_chart(fig, use_container_width=True)

# Net Flow Line Chart
fig2 = px.line(cf_df, x="Week", y="Net Flow", markers=True, title="Net Cash Flow Over Time")
fig2.update_traces(line=dict(color="green", width=3))
st.plotly_chart(fig2, use_container_width=True)

# --- Activity Timeline (Gantt Style) ---
st.subheader("📆 Farm Activity Timeline (Gantt Style)")
timeline_data = []
start_date = datetime.date.today()

activity_durations = {row['Activity']: row['End Week'] - row['Start Week'] + 1 for _, row in editable_plan.iterrows()}
for i, row in editable_plan.iterrows():
    activity = row["Activity"]
    duration = activity_durations.get(activity, 1)
    start = start_date + datetime.timedelta(weeks=i*1)  # space by 1 week per activity
    end = start + datetime.timedelta(weeks=duration)
    timeline_data.append({
        "Task": activity,
        "Start": start,
        "Finish": end,
        "Type": row["Labor Type"]
    })

timeline_df = pd.DataFrame(timeline_data)

fig3 = px.timeline(
    timeline_df,
    x_start="Start",
    x_end="Finish",
    y="Task",
    color="Type",
    title="Farm Activity Timeline"
)

fig3.update_yaxes(autorange="reversed")
st.plotly_chart(fig3, use_container_width=True)

# --- Export Work Plan as CSV ---
download_csv = editable_plan.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Work Plan (CSV)", data=download_csv, file_name="farm_work_plan.csv", mime='text/csv')

import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import datetime
import requests

# --- CONFIG ---
st.set_page_config(page_title="🌽 Maize ROI & Farm Management Tool", layout="wide")
st.markdown("""
    <style>
    .sidebar .sidebar-content { background-color: #f0f2f6; padding: 20px; border-radius: 8px; }
    .stButton>button { background-color: #1a936f; color: white; font-weight: bold; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- Weather API Integration ---
def get_weather(location):
    api_key = 'your_api_key_here'  # Replace with your own OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

# --- SIDEBAR INPUTS ---
st.sidebar.title("🛠️ Farm Setup & Cost Inputs")
farm_size = st.sidebar.number_input("Farm Size (Acres)", value=5, min_value=1)
bags = st.sidebar.slider("Expected Yield (Bags of 50kg)", 50, 300, 150)
price_per_bag = st.sidebar.slider("Market Price per Bag (MWK)", 30000, 100000, 60000, step=1000)
loan_type = st.sidebar.selectbox("Loan Repayment Type", ["Bullet Repayment", "Installments (2x)"])
include_insurance = st.sidebar.checkbox("Include Crop Insurance (5%)", value=True)

# --- Weather Section ---
location = st.sidebar.text_input("Enter Farm Location", "Lilongwe")
if location:
    weather_data = get_weather(location)

    if weather_data["cod"] == 200:
        st.sidebar.header(f"Weather Forecast for {location}")
        st.sidebar.write(f"Temperature: {weather_data['main']['temp']}°C")
        st.sidebar.write(f"Humidity: {weather_data['main']['humidity']}%")
        st.sidebar.write(f"Wind Speed: {weather_data['wind']['speed']} m/s")
        st.sidebar.write(f"Weather: {weather_data['weather'][0]['description'].capitalize()}")
    else:
        st.sidebar.error("Location not found.")
else:
    st.sidebar.info("Enter a farm location to get weather updates.")

# --- Labor Cost Settings ---
st.sidebar.subheader("💼 Labor Cost Settings")
labor_costs = {
    "Tractor": st.sidebar.number_input("Tractor Cost/Acre (MWK)", value=30000, min_value=0),
    "Casual": st.sidebar.number_input("Casual Labor Cost/Day (MWK)", value=2000, min_value=0),
    "Seasonal": st.sidebar.number_input("Seasonal Labor Cost/Day (MWK)", value=2500, min_value=0)
}

# --- Additional Expenses Section ---
st.sidebar.subheader("📊 Additional Expenses")
irrigation_cost = st.sidebar.number_input("Irrigation Costs (MWK)", value=0, min_value=0)
equipment_maintenance = st.sidebar.number_input("Equipment Maintenance (MWK)", value=0, min_value=0)

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
total_expenses = total_labor_cost + irrigation_cost + equipment_maintenance

# --- Financial Summary ---
st.header("💵 Financial Overview")
budget = 4452000
processing_fee = 0.055 * budget
interest_rate = 0.022 if loan_type == "Bullet Repayment" else 0.044
interest = interest_rate * budget
insurance = 0.05 * budget if include_insurance else 0
total_loan_repayment = budget + processing_fee + interest + insurance + total_expenses
revenue = bags * price_per_bag
profit = revenue - total_loan_repayment

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"MWK {revenue:,.0f}")
col2.metric("Total Loan Repayment", f"MWK {total_loan_repayment:,.0f}")
col3.metric("Profit", f"MWK {profit:,.0f}")

# --- Interactive Graph ---
st.subheader("📊 Revenue vs. Expenses")
fig = px.bar(
    x=["Revenue", "Total Loan Repayment", "Expenses"],
    y=[revenue, total_loan_repayment, total_expenses],
    labels={'x': 'Category', 'y': 'Amount (MWK)'},
    title="Maize Revenue and Loan Repayment vs. Expenses"
)
st.plotly_chart(fig)

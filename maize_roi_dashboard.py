import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import requests

# --- CONFIG --- 
st.set_page_config(page_title="🌽 Maize ROI & Farm Management Tool", layout="wide")

# --- SIDEBAR INPUTS ---
st.sidebar.title("🛠️ Farm Setup & Cost Inputs")

# Real-time price fetching - Replace with actual API or mock values
def get_real_time_prices():
    # Placeholder for the API call
    maize_price = 85000  # Average retail price per 50 kg bag (in MWK)
    fertilizer_price = 25000  # Price per 50 kg bag of fertilizer (in MWK)
    seed_price = 12000  # Price per kg of seed (in MWK)
    
    # You would typically use an API like the following to get live data:
    # response = requests.get("API_URL")
    # data = response.json()
    # maize_price = data['maize_price']
    # fertilizer_price = data['fertilizer_price']
    # seed_price = data['seed_price']
    
    return maize_price, fertilizer_price, seed_price

maize_price, fertilizer_price, seed_price = get_real_time_prices()

# User Inputs (Optional: Allow users to enter custom prices or use real-time data)
use_real_time_prices = st.sidebar.checkbox("Use Real-Time Prices", value=True)

if use_real_time_prices:
    st.sidebar.write(f"🌽 **Maize Price (50 kg bag)**: MWK {maize_price}")
    st.sidebar.write(f"💼 **Fertilizer Price (50 kg bag)**: MWK {fertilizer_price}")
    st.sidebar.write(f"🌱 **Seed Price (per kg)**: MWK {seed_price}")
else:
    maize_price = st.sidebar.number_input("Market Price per 50 kg Bag of Maize (MWK)", value=85000)
    fertilizer_price = st.sidebar.number_input("Fertilizer Price per 50 kg Bag (MWK)", value=25000)
    seed_price = st.sidebar.number_input("Seed Price per kg (MWK)", value=12000)

# --- FARMING DETAILS ---
st.title("🌽 Maize ROI & Mega Farm Planner")
st.header("📋 Farm Setup & Financial Overview")

# Expected yield and farm size
farm_size = st.sidebar.number_input("Farm Size (Acres)", value=5, min_value=1)
bags = st.sidebar.slider("Expected Yield (Bags of 50kg)", 50, 300, 150)

# Financial Calculation using real-time data
total_revenue = bags * maize_price
fertilizer_cost = (farm_size * 2) * fertilizer_price  # Assume 2 bags per acre
seed_cost = farm_size * seed_price  # Assume 1 kg of seed per acre

total_costs = fertilizer_cost + seed_cost
profit = total_revenue - total_costs

# --- DISPLAY FINANCIAL SUMMARY ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"MWK {total_revenue:,}")
col2.metric("Total Costs (Fertilizer + Seed)", f"MWK {total_costs:,}")
col3.metric("Profit", f"MWK {profit:,}")

# --- OPTIONAL: Allow the user to adjust and save custom farm plan ---
st.subheader("💼 Custom Work Plan (Editable)")
work_plan = pd.DataFrame({
    "Activity": ["Land Preparation", "Planting", "Fertilizer Application", "Harvesting"],
    "Start Week": [1, 2, 3, 5],
    "End Week": [2, 3, 4, 6],
    "Labor Cost (MWK)": [10000, 15000, 20000, 30000]
})
editable_plan = st.data_editor(work_plan, use_container_width=True, num_rows="dynamic")

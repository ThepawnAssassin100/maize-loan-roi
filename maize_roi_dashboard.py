import streamlit as st
import pandas as pd

# Function to load and prepare editable plan data
def load_editable_plan():
    # Assuming you load editable_plan from a CSV or another data source
    # For example: editable_plan = pd.read_csv("editable_plan.csv")
    editable_plan = pd.DataFrame({
        'Activity': ['Plowing', 'Planting', 'Irrigation', 'Harvesting'],
        'Start Week': [1, 2, 5, 8],
        'End Week': [2, 4, 6, 10]
    })
    return editable_plan

# Check and clean column names to ensure no extra spaces or incorrect casing
def clean_column_names(df):
    df.columns = df.columns.str.strip()  # Remove any leading or trailing spaces
    return df

# Load and clean the data
editable_plan = load_editable_plan()
editable_plan = clean_column_names(editable_plan)

# Ensure that the necessary columns exist
required_columns = ['Activity', 'Start Week', 'End Week']
if not all(col in editable_plan.columns for col in required_columns):
    st.error(f"Missing required columns: {set(required_columns) - set(editable_plan.columns)}")
else:
    # Calculate activity durations
    try:
        editable_plan['Duration'] = editable_plan['End Week'] - editable_plan['Start Week'] + 1
        activity_durations = dict(zip(editable_plan['Activity'], editable_plan['Duration']))
        
        # Display the activity durations
        st.write("Activity Durations:")
        st.write(activity_durations)

        # Optional: Display the editable plan data
        st.write("Editable Plan:")
        st.write(editable_plan)
    except Exception as e:
        st.error(f"Error in calculating durations: {str(e)}")

import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="pysynch Central Analytics", page_icon="⚡", layout="wide"
)

st.title("⚡ pysynch Central Analytics Dashboard")
st.markdown(
    "Real-time aggregated multi-branch intelligence for **pyterOS** merchants."
)

# Sidebar for store selection
st.sidebar.header("Branch Control")
selected_branch = st.sidebar.selectbox(
    "Select Branch",
    [
        "All Branches (Aggregated)",
        "Coffee Shop Branch",
        "Clothing Store Branch",
    ],
)

# Top metric cards
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue (Today)", "₱14,850.00", "+12% vs yesterday")
col2.metric("Active Branches", "2 Connected", "Sync Active")
col3.metric("Low Stock Items", "3 Items", "Requires Restock")

st.divider()

st.subheader("📈 Live Sales Overview Across Branches")
chart_data = pd.DataFrame({
    "Hour": ["8 AM", "10 AM", "12 PM", "2 PM", "4 PM", "6 PM"],
    "Coffee Shop": [1200, 3400, 5600, 4100, 3800, 4500],
    "Clothing Store": [500, 1500, 3200, 2800, 4200, 5100],
})
st.line_chart(chart_data.set_index("Hour"))

st.subheader("📦 Inventory Status & COGS Alert")
inventory_data = pd.DataFrame({
    "Product": [
        "Caramel Macchiato Beans",
        "Matcha Powder",
        "Denim Jacket (M)",
        "Cotton T-Shirt (L)",
    ],
    "Branch": ["Coffee Shop", "Coffee Shop", "Clothing Store", "Clothing Store"],
    "Stock Left": [15, 8, 42, 3],
    "Status": ["Low Stock", "Critical", "Normal", "Critical Restock"],
})
st.dataframe(inventory_data, use_container_width=True)

import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.set_page_config(
    page_title="pysynch Central Analytics", page_icon="⚡", layout="wide"
)

st.title("⚡ pysynch Central Analytics Dashboard")
st.markdown("Real-time aggregated multi-branch intelligence for **pyterOS** merchants.")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

@st.cache_resource
def get_gsheet_client():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=SCOPES
    )
    return gspread.authorize(creds)

@st.cache_data(ttl=30)  # Refresh every 30 seconds
def load_sales():
    client = get_gsheet_client()
    sheet = client.open("pyterOS_Sales").sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data) if data else pd.DataFrame(
        columns=["Order ID", "Date", "Customer", "Product", "Amount", "Status"]
    )

# Sidebar
st.sidebar.header("☁️ pysynch Cloud Portal")
if st.sidebar.button("🔄 Refresh Now"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.caption("Auto-refreshes every 30 seconds.")

# Load data
try:
    df_sales = load_sales()
    connected = True
except Exception as e:
    st.error(f"Could not connect to cloud database: {e}")
    df_sales = pd.DataFrame()
    connected = False

# Metrics
total_revenue = pd.to_numeric(df_sales["Amount"], errors="coerce").sum() if not df_sales.empty else 0.0
pro_sales = df_sales[df_sales["Product"].str.contains("Pro", na=False)] if not df_sales.empty else pd.DataFrame()

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Revenue", f"₱{total_revenue:,.2f}")
col2.metric("📦 Total Orders", len(df_sales))
col3.metric("⭐ Pro Purchases", len(pro_sales))
col4.metric("☁️ Cloud Status", "🟢 Live" if connected else "🔴 Offline")

st.divider()

if not df_sales.empty:
    # Filter options
    col_filter, col_search = st.columns([1, 2])
    with col_filter:
        products = ["All"] + sorted(df_sales["Product"].dropna().unique().tolist())
        selected = st.selectbox("Filter by Product", products)
    with col_search:
        search = st.text_input("Search by Customer / Order ID")

    filtered = df_sales.copy()
    if selected != "All":
        filtered = filtered[filtered["Product"] == selected]
    if search:
        filtered = filtered[
            filtered.apply(lambda r: search.lower() in str(r).lower(), axis=1)
        ]

    st.subheader("📈 Live Sales Transactions")
    st.dataframe(
        filtered.sort_values(by="Order ID", ascending=False),
        use_container_width=True,
    )

    # Pro purchases highlighted
    if not pro_sales.empty:
        st.subheader("⭐ Pro Purchases")
        st.dataframe(pro_sales, use_container_width=True)
else:
    st.info("No sales data yet. Pro purchases from the app will appear here automatically.")

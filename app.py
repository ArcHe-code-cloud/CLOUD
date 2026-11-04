import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="pysynch Central Analytics", page_icon="⚡", layout="wide"
)

st.title("⚡ pysynch Central Analytics Dashboard")
st.markdown(
    "Real-time aggregated multi-branch intelligence for **pyterOS** merchants."
)

# Sidebar: File Uploader for live cloud sync without Git
st.sidebar.header("☁️ pysynch Cloud Portal")
uploaded_file = st.sidebar.file_uploader(
    "Upload Store Excel Ledger (.xlsx)", type=["xlsx"]
)

if uploaded_file is not None:
  # Read the uploaded Excel file directly into the live dashboard
  df_sales = pd.read_excel(uploaded_file, sheet_name="Sales")
  try:
    df_catalog = pd.read_excel(uploaded_file, sheet_name="Catalog")
  except Exception:
    df_catalog = pd.DataFrame()
  st.sidebar.success("Successfully synced active store database!")
else:
  # Default sample view if no file is uploaded yet
  st.sidebar.info(
      "Tip: Upload your local 'pyterOS_store_data.xlsx' here to view live"
      " store metrics."
  )
  df_sales = pd.DataFrame(columns=["Order ID", "Date", "Subtotal"])

total_revenue = df_sales["Subtotal"].sum() if not df_sales.empty else 0.0

# Live Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Live Total Revenue", f"₱{total_revenue:,.2f}", "Cloud Connected")
col2.metric("Sync Method", "Web Portal Upload", "Instant Refresh")
col3.metric(
    "Total Transactions",
    str(len(df_sales)) if not df_sales.empty else "0",
    "Recorded",
)

st.divider()

if not df_sales.empty:
  st.subheader("📈 Live Sales Transactions Log")
  st.dataframe(
      df_sales.sort_values(by="Order ID", ascending=False),
      use_container_width=True,
  )
else:
  st.info(
      "Awaiting store data. Use the sidebar to upload your store's Excel"
      " ledger."
  )

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="pysynch Central Analytics", page_icon="⚡", layout="wide"
)

st.title("⚡ pysynch Central Analytics Dashboard")
st.markdown(
    "Real-time aggregated multi-branch intelligence for **pyterOS** merchants."
)


# Auto-refresh data cache every 5 seconds for live sync
@st.cache_data(ttl=5)
def load_live_sales():
  try:
    df_sales = pd.read_excel("pyterOS_store_data.xlsx", sheet_name="Sales")
    return df_sales
  except Exception:
    return pd.DataFrame()


df_sales = load_live_sales()
total_revenue = (
    df_sales["Subtotal"].sum() if not df_sales.empty else 0.0
)

# Live Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Live Total Revenue", f"₱{total_revenue:,.2f}", "Live Cloud Sync")
col2.metric("Sync Engine", "pysynch Active", "Auto-Refresh: 5s")
col3.metric(
    "Total Orders",
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
      "No transactions found in database. Complete an order in pyterOS desktop"
      " to update!"
  )

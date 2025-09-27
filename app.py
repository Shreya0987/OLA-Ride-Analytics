import streamlit as st
import pandas as pd
import sqlite3
# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="OLA Ride Analytics", layout="wide")

# ------------------ SESSION STATE ------------------
if "show_dashboard" not in st.session_state:
    st.session_state.show_dashboard = False

# ------------------ COVER PAGE ------------------
if not st.session_state.show_dashboard:
    st.markdown(
        """
        <style>
        .cover {
            text-align: center;
            padding: 80px 20px;
            background: linear-gradient(135deg, #36D1DC, #5B86E5);
            border-radius: 15px;
            color: white;
        }
        .cover h1 {
            font-size: 3em;
            font-weight: bold;
        }
        .cover p {
            font-size: 1.3em;
        }
        </style>
        <div class="cover">
            <h1>🚖 OLA Ride Analytics Dashboard</h1>
            <p>Data-driven insights for smarter urban mobility.</p>
            <p>Explore ride volumes, cancellations, revenue, and ratings — all in one place.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("👉 Start Analytics"):
        st.session_state.show_dashboard = True
        st.rerun()

# ------------------ DASHBOARD SECTION ------------------
else:
    st.title("📊 OLA Ride Analytics")

    # Load Data
    @st.cache_data
    def load_data():
        return pd.read_csv(r"C:\Users\Shreya Ghosal\Downloads\ola_cleaned.csv")

    df = load_data()

    # SQL Explorer
    conn = sqlite3.connect(":memory:")
    df.to_sql("rides", conn, index=False, if_exists="replace")

    st.subheader("🔍 Run SQL Queries")
    query = st.text_area("Enter your SQL query:", "SELECT * FROM rides LIMIT 5;")

    if st.button("Run Query"):
        try:
            result = pd.read_sql(query, conn)
            st.dataframe(result, use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")

    # Filters
    st.sidebar.header("Filters")
    vehicle_type = st.sidebar.multiselect(
        "Select Vehicle Type", options=df["vehicle_type"].unique(), default=df["vehicle_type"].unique()
    )
    payment_method = st.sidebar.multiselect(
        "Select Payment Method", options=df["payment_method"].unique(), default=df["payment_method"].unique()
    )
    search_customer = st.sidebar.text_input("Search Customer ID:")

    filtered_df = df[
        (df["vehicle_type"].isin(vehicle_type)) &
        (df["payment_method"].isin(payment_method))
    ]
    if search_customer:
        filtered_df = filtered_df[filtered_df["customer_id"].astype(str).str.contains(search_customer)]

    st.subheader("📋 Filtered Data")
    st.dataframe(filtered_df, use_container_width=True)

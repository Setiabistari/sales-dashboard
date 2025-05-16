
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Executive Sales Dashboard", layout="wide")

st.title("📈 Executive Sales Dashboard")

# Upload CSV
uploaded_file = st.file_uploader("Upload your weekly CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Filters
    st.sidebar.header("Filters")
    entity = st.sidebar.multiselect("KJTS Entity", df['KJTS_Entity'].unique())
    stage = st.sidebar.multiselect("Stage", df['Stage'].unique())
    team_member = st.sidebar.multiselect("Team Member", df['Team_member'].unique())

    filtered_df = df.copy()
    if entity:
        filtered_df = filtered_df[filtered_df['KJTS_Entity'].isin(entity)]
    if stage:
        filtered_df = filtered_df[filtered_df['Stage'].isin(stage)]
    if team_member:
        filtered_df = filtered_df[filtered_df['Team_member'].isin(team_member)]

    # Metrics
    total_expected_revenue = filtered_df['Expected_Revenue'].sum()
    total_won_value = filtered_df.loc[filtered_df['Stage'] == 'Won', 'Expected_Revenue'].sum()
    total_opportunities = len(filtered_df)
    total_wins = len(filtered_df[filtered_df['Stage'] == 'Won'])
    win_rate = (total_wins / total_opportunities * 100) if total_opportunities else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Expected Revenue", f"RM {total_expected_revenue:,.2f}")
    col2.metric("🏆 Total Won Value", f"RM {total_won_value:,.2f}")
    col3.metric("📄 Total Opportunities", total_opportunities)
    col4.metric("🎯 Win Rate", f"{win_rate:.2f}%")

    st.markdown("---")

    # Charts
    st.subheader("Expected Revenue by Stage")
    st.bar_chart(filtered_df.groupby('Stage')['Expected_Revenue'].sum())

    st.subheader("Expected Revenue by KJTS Entity")
    st.bar_chart(filtered_df.groupby('KJTS_Entity')['Expected_Revenue'].sum())

    st.subheader("Top 5 Customers by Expected Revenue")
    top_customers = filtered_df.groupby('Company_Name')['Expected_Revenue'].sum().nlargest(5)
    st.bar_chart(top_customers)

    st.subheader("Team Member Performance")
    st.bar_chart(filtered_df.groupby('Team_member')['Expected_Revenue'].sum())

    # Show Data Table
    st.subheader("📋 Filtered Data")
    st.dataframe(filtered_df)
else:
    st.info("📂 Please upload a CSV file to get started.")

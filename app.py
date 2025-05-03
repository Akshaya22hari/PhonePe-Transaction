import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import json 
import requests  

st.set_page_config(page_title="PhonePe Dashboard", layout="wide")

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Business Case Study"])

# ---------- Home Page ----------
if page == "Home":
    st.markdown("<h1 style='color:darkblue;'>PhonePe Dashboard</h1>", unsafe_allow_html=True)

    st.write("Welcome! Here's a map showing transaction amount by Indian state:")

        # Load and clean the CSV
    df = pd.read_csv("C:/Users/Aksha/OneDrive/Documents/Akshaya/GUVI/phonepe_dashboard/state_summary.csv")
    df['State'] = df['State'].str.strip().str.title()
    df['Transaction_amount'] = pd.to_numeric(df['Transaction_amount'], errors='coerce')

    # Standardize names for mapping
    state_name_map = {
        "Andaman & Nicobar Islands": "Andaman & Nicobar Islands",
        "Andhra-Pradesh": "Andhra Pradesh",
        "Arunachal-Pradesh": "Arunachal Pradesh",
        "Uttar-Pradesh": "Uttar Pradesh",
        "Jammu & Kashmir": "Jammu and Kashmir",
        "Telengana": "Telangana",
        "Delhi": "NCT of Delhi",
        "Pondicherry": "Puducherry",
        "Dadra And Nagar Haveli": "Dadra & Nagar Haveli",
        "Chattisgarh": "Chhattisgarh",
        "Orissa": "Odisha",
        "Tamil-Nadu": "Tamil Nadu",
        "Madhya-Pradesh": "Madhya Pradesh",
        "Jammu-&-Kashmir": "Jammu & Kashmir",
        "Himachal-Pradesh": "Himachal Pradesh",
        "West-Bengal": "West Bengal"
    }
    df["State"] = df["State"].replace(state_name_map)

    # GeoJSON from Plotly Gist
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    geojson_data = json.loads(requests.get(url).text)

    # Verify matching states
    geojson_states = [feature["properties"]["ST_NM"] for feature in geojson_data["features"]]
    df = df[df["State"].isin(geojson_states)]  # keep only matching

    # Choropleth map
    fig = px.choropleth(
        df,
        geojson=geojson_data,
        featureidkey='properties.ST_NM',
        locations='State',
        color='Transaction_amount',
        color_continuous_scale='Blues',
        title="Total Transaction Amount by State"
    )

    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig, use_container_width=True)

# ---------- Business Case Study ----------
elif page == "Business Case Study":

# 1.Category-wise Analysis (Transaction_type)

    st.markdown("<h1 style='color:darkblue;'>Business Case Study</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:crimson;'>1. Decoding Transaction Dynamics on PhonePe</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:green;'>A. Category-wise Analysis — Transaction Type</h3>", unsafe_allow_html=True)
        # Load and prepare data
    @st.cache_data
    def load_data():
        df = pd.read_csv("category_summary.csv")
        return df

    df = load_data()

    # Metric selection
    metric = st.radio(
        " Select Metric to Visualize:",
        ["Transaction_count", "Transaction_amount"],
        index=0,
        horizontal=True
    )

    # Donut chart
    fig = px.pie(
        df,
        names="Transaction_type",
        values=metric,
        title=f"{metric.replace('_', ' ').title()} by Transaction Type",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_traces(textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
#2. Identifying Growth or Decline — Year-wise State Comparison

    st.markdown("<h3 style='color:green;'>B. Identifying Growth or Decline — Year-wise State Comparison</h3>", unsafe_allow_html=True)

    # Load and prepare data
    @st.cache_data
    def load_data():
        df = pd.read_csv("pivot_table.csv")
        df_long = pd.melt(df, id_vars=["State"], 
                        value_vars=["2018", "2019", "2020", "2021", "2022", "2023", "2024"],
                        var_name="Year", value_name="Transaction_amount")
        df_long["Year"] = df_long["Year"].astype(str)
        df_long["Transaction_amount"] = pd.to_numeric(df_long["Transaction_amount"], errors="coerce")
        return df, df_long

    df_wide, df_long = load_data()

    # Year filter
    year_options = sorted(df_long["Year"].unique())
    selected_years = st.multiselect("Select Year(s) to Compare", year_options, default=year_options)

    # Filter based on selected years (only for chart)
    filtered_data = df_long[df_long["Year"].isin(selected_years)]

    # Bar Chart: State-wise comparison across selected years
    st.subheader("Transaction Amount by State and Year")
    fig5 = px.bar(
        filtered_data,
        x='State',
        y='Transaction_amount',
        color='Year',
        barmode='group',
        title="State-wise Transaction Amount (Year-wise)",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig5.update_layout(xaxis_tickangle=-45, height=500)
    st.plotly_chart(fig5, use_container_width=True)

#3.Brand Summary
    st.markdown("<h2 style='color:crimson;'>2. Device Dominance and User Engagement Analysis</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:green;'>A. Brand-wise User Distribution</h3>", unsafe_allow_html=True)
     # Load the brand summary CSV
    df_brand = pd.read_csv("brand_summary.csv")

    # Pie Chart using Plotly
    fig = px.pie(
        df_brand,
        names='User_type',
        values='User_count',
        title='Brand-wise User Share',
        hole=0.4,  # Set to 0 for full pie chart
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

#4. State Brand summary
    st.markdown("<h3 style='color:green;'>B. Brand-wise User Trends Across States</h3>", unsafe_allow_html=True)

     # Load and reshape data
    @st.cache_data
    def load_data():
        df = pd.read_csv("pivot_brand_state.csv")
        df_long = pd.melt(df, id_vars=["State"], var_name="User_type", value_name="User_count")
        df_long = df_long[df_long["User_count"] > 0]  # Remove zero values
        return df_long

    df_long = load_data()

    # Brand filter above chart (not in sidebar)
    all_brands = sorted(df_long["User_type"].unique())
    selected_brands = st.multiselect(
        "Select Brands to Compare:",
        options=all_brands,
        default=all_brands
    )

    # Filter based on brand selection
    filtered_df = df_long[df_long["User_type"].isin(selected_brands)]
    filtered_df = filtered_df.sort_values(["State", "User_type"])

    # Line chart
    st.subheader("Line Chart of User Count by State")
    fig = px.line(
        filtered_df,
        x="State",
        y="User_count",
        color="User_type",
        markers=True,
        title="User Count by Brand Across States"
    )
    fig.update_layout(xaxis_tickangle=-45, height=650)
    st.plotly_chart(fig, use_container_width=True)

#5.District-wise Transaction Summary

    st.markdown("<h2 style='color:crimson;'>3. Transaction Analysis for Market Expansion</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:green;'>A. District-wise Transaction Summary</h3>", unsafe_allow_html=True)

    # Load the data
    @st.cache_data
    def load_data():
        df = pd.read_csv("district_summary.csv")
        return df

    df = load_data()

    # State filter above chart
    states = sorted(df["State"].unique())
    selected_states = st.multiselect(
        " Select State(s) to View:",
        options=states,
        default=states
    )

    # Filter based on state selection
    filtered_df = df[df["State"].isin(selected_states)]

    # Bar chart: Transaction Amount by District
    st.subheader("District-wise Transaction Amount")
    fig = px.bar(
        filtered_df,
        x="District_Pincode",
        y="Transaction_amount",
        color="State",
        title="Transaction Amount by District",
        labels={"Transaction_amount": "Transaction Amount"},
        height=600
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

#6.State-wise User Engagement

    st.markdown("<h2 style='color:crimson;'>4.  User Engagement and Growth Strategy</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:green;'>A. State-wise User Engagement Analysis</h3>", unsafe_allow_html=True)

    # Load data
    @st.cache_data
    def load_data():
        return pd.read_csv("state_user_engagement.csv")

    df = load_data()

    # Metric selection
    metric = st.radio(
        "Select Metric to Visualize:",
        ["User_count", "User_amount", "Engagement_rate"],
        index=2,
        horizontal=True
    )

    # Sort for better visibility
    df_sorted = df.sort_values(metric, ascending=False)

    # Bar chart
    fig = px.bar(
        df_sorted,
        x="State",
        y=metric,
        title=f"{metric.replace('_', ' ').title()} by State",
        text=metric,
        color=metric,
        height=600
    )
    fig.update_layout(xaxis_tickangle=-45)
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')

    st.plotly_chart(fig, use_container_width=True)

#7.District-wise User Engagement
    st.markdown("<h3 style='color:green;'>B. District-wise User Engagement Analysis</h3>", unsafe_allow_html=True)

    # Load the data
    @st.cache_data
    def load_data():
        df = pd.read_csv("district_engagement.csv")
        return df

    df = load_data()
    df["State"] = df["State"].str.title()

    # Unique states for filter
    states = sorted(df["State"].unique())

    # Filter by state
    selected_states = st.multiselect(
        "Select State(s):",
        options=states,
        default=states,
        key="state_filter_district"
    )

    # Filter dataset
    filtered_df = df[df["State"].isin(selected_states)]

    # Metric selection
    metric = st.radio(
        "Select Metric:",
        options=["User_count", "User_amount", "Engagement_rate"],
        index=2,
        horizontal=True
    )

    # Sort by metric
    filtered_df = filtered_df.sort_values(metric, ascending=False)

    # Bar Chart
    st.subheader(f"{metric.replace('_', ' ').title()} by District")
    fig = px.bar(
        filtered_df,
        x="District_Pincode",
        y=metric,
        color="State",
        title=None,
        height=600
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

#8.State-Insurance summary

    st.markdown("<h2 style='color:crimson;'>5.   Insurance Engagement Analysis</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:green;'>A. Year-wise Insurance Distribution</h3>", unsafe_allow_html=True)

    # Load the data
    @st.cache_data
    def load_data():
        df = pd.read_csv("state_insurance_summary.csv")
        df = df.rename(columns={"State": "Year"})  # Rename for clarity
        return df

    df = load_data()

    # Metric selection
    metric = st.radio(
        "Select Metric to Display:",
        ["Insurance_count", "Insurance_amount"],
        index=0,
        horizontal=True
    )

    # Donut chart
    fig = px.pie(
        df,
        names="Year",
        values=metric,
        title=f"{metric.replace('_', ' ').title()} Distribution by Year",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textinfo='percent+label')

    st.plotly_chart(fig, use_container_width=True)

#9.Top Districts by User Count

    st.markdown("<h2 style='color:crimson;'>6.   User Registration Analysis</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:green;'>A. Top Districts by User Count</h3>", unsafe_allow_html=True)

    # Load data
    @st.cache_data
    def load_data():
        df = pd.read_csv("top_districts.csv")
        df["State"] = df["State"].str.title()
        return df

    df = load_data()

    # Sort by user count descending
    df_sorted = df.sort_values("User_count", ascending=True)  # for horizontal bar

    # Bar Chart
    fig = px.bar(
        df_sorted,
        x="User_count",
        y="District_Pincode",
        color="State",
        orientation="h",
        title="Top Districts by User Count",
        height=700
    )
    fig.update_layout(yaxis_title="District", xaxis_title="User Count")
    st.plotly_chart(fig, use_container_width=True)

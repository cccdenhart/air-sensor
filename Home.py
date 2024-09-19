from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
from supabase import Client, create_client


# Initialize connection to Supabase
def get_data(start_date: datetime, end_date: datetime):
    url: str = st.secrets["SUPABASE_POST_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)

    response = (
        supabase.table("sensor")
        .select("*")
        .gte("created_at", start_date)
        .lte("created_at", end_date)
        .order("created_at", desc=True)
        .limit(1000)
        .execute()
    )

    df = pd.DataFrame(response.data)

    df["created_at"] = (
        df["created_at"].apply(pd.to_datetime).dt.tz_convert("US/Pacific")
    )

    return df


st.title("Home Air Quality Report")

st.subheader("Filter Data")
default_start = datetime.now() - timedelta(days=3)

col1, col2, col3 = st.columns(3)
with col1:
    start_date = st.date_input("Start Date", value=default_start)
with col2:
    end_date = st.date_input("End Date", value=datetime.now())
with col3:
    location = st.selectbox("Location", options=["Kitchen", "Bedroom 3"])

if start_date > end_date:
    st.error("Start date must be before the end date.")
    st.stop()

if start_date > datetime.now().date() or end_date > datetime.now().date():
    st.error("You cannot select a time in the future.")
    st.stop()

st.subheader("Data")

df = get_data(start_date, end_date)

st.subheader("CO2 PPM")
st.line_chart(df, x="created_at", y=["co2_ppm"])

st.subheader("Temperature and Humidity")
st.line_chart(df, x="created_at", y=["temperature_c", "humidity_relative"])

st.subheader("Air Quality")

st.write("**Standard Measurements**")
standard_metrics = [c for c in df.columns if "standard" in c]
standard_metrics = sorted(standard_metrics, key=lambda x: int(x.split()[0][2:]))
st.line_chart(df, x="created_at", y=standard_metrics)

st.write("**Environment Measurements**")
env_metrics = [c for c in df.columns if "env" in c]
env_metrics = sorted(env_metrics, key=lambda x: int(x.split()[0][2:]))
st.line_chart(df, x="created_at", y=env_metrics)

st.write("**Particle Metrics**")
particle_metrics = [c for c in df.columns if "particle" in c]


def particle_metrics_sorter(pm: str):
    val_str = pm.split()[1][:-2]
    if val_str.startswith("0"):
        val_str = "0." + val_str[1:]
    return float(val_str)


particle_metrics = sorted(particle_metrics, key=particle_metrics_sorter)
st.line_chart(df, x="created_at", y=particle_metrics)

st.divider()

st.write(df)

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from supabase import Client, create_client


# Initialize connection to Supabase
def get_data():
    url: str = st.secrets["SUPABASE_POST_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)

    response = supabase.table('sensor').select('*').execute()

    df = pd.DataFrame(response.data)

    df["created_at"] = df["created_at"].apply(pd.to_datetime).dt.tz_convert('US/Pacific')

    return df


st.title("Home Air Quality Report")

df = get_data()

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
    breakpoint()
    return float(val_str)

particle_metrics = sorted(particle_metrics, key=particle_metrics_sorter) 
st.line_chart(df, x="created_at", y=particle_metrics)

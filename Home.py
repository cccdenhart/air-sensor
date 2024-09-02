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

    return df


st.title("Home Air Quality Report")

df = get_data()

st.subheader("CO2 PPM")
st.line_chart(df, x="created_at", y=["co2_ppm"])

st.subheader("Temperature and Humidity")
st.line_chart(df, x="created_at", y=["temperature_c", "humidity_relative"])

st.subheader("Air Quality")
st.line_chart(df, x="created_at", y=["pm10 standard", "pm25 standard", "pm100 standard"])
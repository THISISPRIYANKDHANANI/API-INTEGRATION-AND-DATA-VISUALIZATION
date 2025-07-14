import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# --- Config ---
API_KEY = "3d3f044481f34d8242ee62b0c5f5ffe3"
API_BASE = "https://api.openweathermap.org/data/2.5/weather"

# --- Function to fetch weather data ---
def fetch_weather(city, country_code=""):
    if country_code:
        query = f"{city},{country_code}"
    else:
        query = city

    url = f"{API_BASE}?q={query}&appid={API_KEY}&units=metric"
    res = requests.get(url)

    if res.status_code != 200:
        return None

    data = res.json()
    return {
        "City": data["name"],
        "Temperature (°C)": data["main"]["temp"],
        "Humidity (%)": data["main"]["humidity"],
        "Wind Speed (m/s)": data["wind"]["speed"],
        "Weather": data["weather"][0]["main"],
        "Description": data["weather"][0]["description"]
    }

# --- Visualization ---
def visualize_weather(df):
    with st.container():
        st.subheader("\U0001F4CA Weather Data Table")
        st.dataframe(df)

        with st.expander("📊 Expand to View Weather Charts"):
            col1, col2 = st.columns(2)

            with col1:
                fig_temp = px.bar(df, x="City", y="Temperature (°C)", color="Temperature (°C)", title="\U0001F321 Temperature by City")
                st.plotly_chart(fig_temp, use_container_width=True)

                fig_hum = px.bar(df, x="City", y="Humidity (%)", color="Humidity (%)", title="\U0001F4A7 Humidity by City")
                st.plotly_chart(fig_hum, use_container_width=True)

            with col2:
                fig_wind = px.bar(df, x="City", y="Wind Speed (m/s)", color="Wind Speed (m/s)", title="\U0001F32C Wind Speed by City")
                st.plotly_chart(fig_wind, use_container_width=True)

                fig_box = px.box(df, y="Temperature (°C)", title="\U0001F4E6 Temperature Distribution")
                st.plotly_chart(fig_box, use_container_width=True)

            st.divider()

            fig_pie = px.pie(df, names="Weather", title="\U000026C5 Weather Conditions Distribution")
            st.plotly_chart(fig_pie, use_container_width=True)

            fig_scatter = px.scatter(df, x="Temperature (°C)", y="Wind Speed (m/s)", color="City", size="Humidity (%)",
                                     title="\U0001F4C8 Temperature vs Wind Speed")
            st.plotly_chart(fig_scatter, use_container_width=True)

# --- Streamlit App ---
st.set_page_config("\U0001F324 Weather Dashboard", layout="wide")
st.title("\U0001F324 Multi-City Weather Visualization Dashboard")

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.write("Enter city names to visualize current weather conditions.")

with st.container():
    cities_input = st.text_area("Enter city names separated by commas (e.g., Mumbai, Delhi, New York):", "Mumbai, Delhi, Tokyo")

    if st.button("Fetch Weather Data"):
        city_list = [city.strip() for city in cities_input.split(",") if city.strip()]
        weather_data = []

        for city in city_list:
            data = fetch_weather(city)
            if data:
                weather_data.append(data)
            else:
                st.warning(f"\u274C Data not found for: {city}")

        if weather_data:
            df = pd.DataFrame(weather_data)
            visualize_weather(df)

import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ---------------- CONFIG ----------------
API_KEY = "e3f1905128c7cac8955e4adf25a2ade1"

st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌦️",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

.main {
    background: linear-gradient(
        135deg,
        #0f172a,
        #1e293b
    );
}

.weather-card {
    background: rgba(255,255,255,0.08);
    padding:20px;
    border-radius:20px;
    text-align:center;
    backdrop-filter: blur(12px);
    box-shadow: 0px 4px 25px rgba(0,0,0,0.25);
}

.metric {
    font-size:28px;
    color:white;
    font-weight:bold;
}

.label {
    color:#d1d5db;
    font-size:16px;
}

.title {
    text-align:center;
    color:white;
    font-size:50px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown(
    "<div class='title'>🌦️ Advanced Weather Dashboard</div>",
    unsafe_allow_html=True
)

city = st.text_input(
    "🔍 Search City",
    placeholder="Enter city name..."
)

# ---------------- WEATHER ----------------

if city:

    try:

        weather_url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"q={city}&appid={API_KEY}&units=metric"
        )

        weather = requests.get(weather_url).json()

        if weather["cod"] != 200:
            st.error("City not found")
            st.stop()

        lat = weather["coord"]["lat"]
        lon = weather["coord"]["lon"]

        temp = weather["main"]["temp"]
        humidity = weather["main"]["humidity"]
        pressure = weather["main"]["pressure"]
        wind = weather["wind"]["speed"]

        desc = weather["weather"][0]["description"]
        icon = weather["weather"][0]["icon"]

        icon_url = (
            f"https://openweathermap.org/img/wn/{icon}@4x.png"
        )

        # ---------------- AQI ----------------

        aqi_url = (
            f"https://api.openweathermap.org/data/2.5/air_pollution?"
            f"lat={lat}&lon={lon}&appid={API_KEY}"
        )

        aqi_data = requests.get(aqi_url).json()

        aqi = aqi_data["list"][0]["main"]["aqi"]

        aqi_map = {
            1: "Good 😊",
            2: "Fair 🙂",
            3: "Moderate 😐",
            4: "Poor 😷",
            5: "Very Poor ☠️"
        }

        st.image(icon_url, width=150)

        st.markdown(
            f"<h2 style='color:white;text-align:center'>{city.title()}</h2>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"<h3 style='color:#e2e8f0;text-align:center'>{desc.title()}</h3>",
            unsafe_allow_html=True
        )

        col1,col2,col3,col4,col5 = st.columns(5)

        with col1:
            st.metric(
                "🌡 Temperature",
                f"{temp} °C"
            )

        with col2:
            st.metric(
                "💧 Humidity",
                f"{humidity}%"
            )

        with col3:
            st.metric(
                "🌀 Pressure",
                f"{pressure} hPa"
            )

        with col4:
            st.metric(
                "💨 Wind",
                f"{wind} m/s"
            )

        with col5:
            st.metric(
                "🌿 Air Quality",
                aqi_map[aqi]
            )

        st.divider()

        # ---------------- FORECAST ----------------

        forecast_url = (
            f"https://api.openweathermap.org/data/2.5/forecast?"
            f"q={city}&appid={API_KEY}&units=metric"
        )

        forecast = requests.get(
            forecast_url
        ).json()

        forecast_data = []

        for item in forecast["list"]:

            forecast_data.append({
                "Date": item["dt_txt"],
                "Temperature": item["main"]["temp"]
            })

        df = pd.DataFrame(forecast_data)

        fig = px.line(
            df,
            x="Date",
            y="Temperature",
            title="📈 5-Day Temperature Forecast"
        )

        fig.update_layout(
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font_color="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.success(
            "Weather data loaded successfully."
        )

    except Exception as e:
        st.error(
            f"Error: {str(e)}"
        )

else:
    st.info(
        "Enter a city name to view weather details."
    )
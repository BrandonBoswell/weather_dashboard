

# shift-alt-f for formating


from datetime import datetime
import streamlit as st
import altair as alt
import pandas as pd
import requests
import json


# connect weather api

api_key = "2c328fb5de96478ab52223916263001"
api_endpoint = "https://api.weatherapi.com/v1"


fdays = 3


def forecast_data_raw(api_url):
    zip_code = str(99515)
    full_url = api_url + "/forecast.json?key=" + \
        api_key + "&q=" + zip_code + "&days=" + str(fdays)
    print(full_url)
    response = requests.get(full_url)

    if response.status_code == 200:
        forecast_data = response.json()

    else:
        print(f"Error: {response.status_code}")

    return (forecast_data)


forecast_dict = (forecast_data_raw(api_endpoint))


location = pd.DataFrame.from_dict(
    forecast_dict.get("location"), orient="index")


current_condition = pd.DataFrame.from_dict(
    forecast_dict.get("current"), orient="index")
current_condition.reset_index(inplace=True, drop=False)
current_condition.columns = ['Variables', 'Values']

forecast = pd.DataFrame.from_dict(
    forecast_dict.get("forecast"), orient="columns")


fc_day1 = pd.DataFrame.from_dict(
    forecast_dict["forecast"]["forecastday"][0]['day'], orient="index")
fc_day1.reset_index(inplace=True, drop=False)



hour_stats = []
for i in range(fdays):
    for m in range(24):
        k = forecast["forecastday"][i]['hour'][m]
        hour_stats.append(k)

hour_stats = pd.DataFrame.from_dict(hour_stats)


# transform data
# what data do I want to display on my dashboard? I should probably be mapping this out in canva


# Populate my dashboard

st.set_page_config(
    page_title="Anchorage Today",
    page_icon=" ",
    layout="wide"
)


"""
# Todays Weather in Anchorage!


"""
st.write(datetime.now())
""
""

"""
## 
"""

""
# create graphs with streamlit

with st.container(horizontal=True, gap="medium"):
    cols = st.columns(2, gap="large", width=500)

    with cols[0]:
        st.metric(
            "Current temperature",
            f"{current_condition.at[3, 'Values']}F",
            width="content"
        )

    with cols[1]:
        st.metric(
            "Max Temperature",
            f"{forecast_dict["forecast"]["forecastday"][0]['day']["maxtemp_f"]}F",
            width="content"
        )

    cols = st.columns(2, gap="medium", width=500)

    with cols[0]:
        st.metric(
            "Min Temperature",
            f"{forecast_dict["forecast"]["forecastday"][0]['day']["mintemp_f"]}F",
            width="content"
        )

    with cols[1]:
        st.metric(
            "Conditions",
            f"{current_condition.at[5, 'Values']['text']}",
            width="content"
        )

    cols = st.columns(2, gap="medium", width=500)

    with cols[0]:
        st.metric(
            "Cloud Cover %",
            f"{current_condition.at[15, 'Values']}",
            width="content"
        )

    with cols[1]:
        st.metric(
            "Humidity",
            f"{current_condition.at[14, 'Values']}",
            width="content"
        )

""
""

"""
## Forecasted Temperatures by Hour
"""
with st.container(border=True, height="content"):
    "### Temperature"

    st.altair_chart(
        alt.Chart(hour_stats)
        .mark_bar(width=10)
        .encode(
            alt.X("time", timeUnit='dayhours').title("Day & Hours"),
            alt.Y("temp_f").title("Temperature(F)"),
            color=alt.Color('max(temp_f)').scale(scheme="viridis")
        )

        .configure_legend(legendX=100, legendY=100, direction="vertical", gradientLength=100)
    )



# To run:
# C:\... \Python_Projects\weather_dash>python -m streamlit run weather_dashv1.py
#  To stop:
# ctrl+c

"""
============================================================

WEATHER DASHBOARD

============================================================
"""


from datetime import datetime
import streamlit as st
import pandas as pd
import requests
import json


## connect weather api

api_key = "2c328fb5de96478ab52223916263001"
api_endpoint = "https://api.weatherapi.com/v1"


def forecast_data_raw(api_url):
    zip_code = str(99515)
    fdays = str(2)
    full_url = api_url + "/forecast.json?key=" + api_key + "&q=" + zip_code + "&days=" + fdays
    print(full_url)
    response = requests.get(full_url)
    
    if response.status_code == 200:
        forecast_data = response.json()

    else:
        print(f"Error: {response.status_code}")

    return(forecast_data)

forecast_dict = (forecast_data_raw(api_endpoint))
#print(type(forecast_dict))

location = pd.DataFrame.from_dict(forecast_dict.get("location"), orient="index")
#print(location)

current_condition = pd.DataFrame.from_dict(forecast_dict.get("current"), orient="index")
#print(current_condition)

forecast = pd.DataFrame.from_dict(forecast_dict.get("forecast"), orient="columns")
#print(forecast)

fc_day1 = pd.DataFrame.from_dict(list(forecast_dict["forecast"]["forecastday"][0]['day'].items()))
print(fc_day1)
#for key, value in forecast_dict.items():
#    print(key, value)


#location = pd.DataFrame.from_dict(forecast_dict.items())
#print(location)

#df = pd.DataFrame(list(forecast_dict.items()), columns=['Key', 'Values'])
#print(df)
#location = pd.DataFrame(list(forecast_dict.items()), columns=['Key', 'Values'])







## transform data




## create graphs with streamlit


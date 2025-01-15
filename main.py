from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Tuple, List
import requests
from math import radians, sin, cos, sqrt, atan2
import polyline
from datetime import datetime, timedelta
import asyncio
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import matplotlib.pyplot as plt
from fastapi.responses import FileResponse

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"message": "Hello, World!"}

# ---------------------------------------------------------------------------------------


@app.post("/weather")
async def get_weather(data: dict):
    print("data", data)
    try:
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if latitude is None or longitude is None:
            raise HTTPException(status_code=400, detail="Latitude and Longitude are required")

        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m"
        }
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]

        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

        hourly_data = {
            "datetime": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            ),
            "temperature_2m": hourly_temperature_2m
        }
        hourly_dataframe = pd.DataFrame(data=hourly_data)

        plt.figure(figsize=(12, 6))
        plt.plot(
            hourly_dataframe["datetime"],
            hourly_dataframe["temperature_2m"],
            label="Hourly Temperature",
            marker='o',
            linestyle='-',
        )
        plt.xlabel("Date")
        plt.ylabel("Temperature (°C)")
        plt.title(f"Hourly Temperature Over Time\n(Lat: {latitude}, Lon: {longitude})")
        plt.grid(True)
        plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.DayLocator())
        plt.xticks(rotation=45)
        plt.legend()

        # Save the plot
        plot_filename = "weather_plot_with_points.png"
        plt.savefig(plot_filename, bbox_inches='tight')
        plt.close()

        return FileResponse(plot_filename)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)

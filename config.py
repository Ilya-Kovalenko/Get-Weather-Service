import os

WEATHERAPI_NOW_URL = (
    "https://api.weatherapi.com/v1/current.json?q={},{}"
    + f"&key={os.getenv('WEATHERAPI_API_KEY')}"
)
WEATHERAPI_FORECAST_URL = (
    "https://api.weatherapi.com/v1/forecast.json?q={},{}&days=10&aqi=no&alerts=no"
    + f"&key={os.getenv('WEATHERAPI_API_KEY')}"
)

OPEN_METEO_NOW_URL = (
    "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}"
    "&current=temperature_2m,precipitation"
)
OPEN_METEO_FORECAST_URL = (
    "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}"
    "&hourly=temperature_2m,precipitation&forecast_days=10"
)

OPENCAGEDATA_URL = (
    "https://api.opencagedata.com/geocode/v1/json?q={},{}&no_annotations=1"
    + f"&key={os.getenv('OPENCAGEDATA_API_KEY')}"
)

API_NINJAS_URL = "https://api.api-ninjas.com/v1/geocoding?city={}&country={}"

API_NINJAS_API_KEY = os.getenv("API_NINJAS_API_KEY")

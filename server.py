from datetime import date, datetime, timedelta, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from weather_api import get_forecast_weather, get_now_weather

app = FastAPI()


class WeatherData(BaseModel):
    country: str
    city: str
    when: datetime | None = None


@app.post("/get_now/")
async def get_now(weather_data: WeatherData) -> dict:
    result = await get_now_weather(weather_data.city, weather_data.country)

    return result


@app.post("/get_forecast/")
async def get_forecast(weather_data: WeatherData) -> dict:
    check_data = datetime.combine(date.today(), datetime.min.time())
    check_data = check_data.replace(tzinfo=timezone.utc)
    weather_data.when = weather_data.when.replace(tzinfo=timezone.utc)

    if weather_data.when is None:
        raise HTTPException(status_code=400, detail="No date and time provided")
    elif weather_data.when < check_data:
        raise HTTPException(
            status_code=400, detail="Date and time must not be earlier than today"
        )
    elif weather_data.when - check_data > timedelta(days=10):
        raise HTTPException(
            status_code=400,
            detail="Date and time must be no later than 10 days from today",
        )

    result = await get_forecast_weather(
        weather_data.city, weather_data.country, weather_data.when
    )

    return result

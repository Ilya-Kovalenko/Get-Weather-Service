from abc import ABC
from datetime import datetime, timezone

import httpx

from config import (OPEN_METEO_FORECAST_URL, OPEN_METEO_NOW_URL,
                    WEATHERAPI_FORECAST_URL, WEATHERAPI_NOW_URL)


class BaseApi(ABC):
    async def get_now_data(
        self, latitude: float, longitude: float
    ) -> tuple[float, bool] | None:
        pass

    async def get_forecast_data(
        self, latitude: float, longitude: float, when: datetime
    ) -> tuple[float, bool] | None:
        pass

    @staticmethod
    async def fetch_url(url) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

            return response.json()


class WeatherapiApi(BaseApi):
    def __init__(self):
        self.now_url = WEATHERAPI_NOW_URL
        self.forecast_url = WEATHERAPI_FORECAST_URL

    async def get_now_data(
        self, latitude: float, longitude: float
    ) -> tuple[float, bool] | None:
        try:
            response_json = await self.fetch_url(
                self.now_url.format(latitude, longitude)
            )
            temp_celsium = response_json["current"]["temp_c"]
            is_precipitation = bool(response_json["current"]["precip_mm"])

            return temp_celsium, is_precipitation

        except:
            return None

    async def get_forecast_data(
        self, latitude: float, longitude: float, when: datetime
    ) -> tuple[float, bool] | None:
        try:
            response_json = await self.fetch_url(
                self.forecast_url.format(latitude, longitude)
            )

            when_str = when.strftime("%Y-%m-%d")

            forecast_day = response_json["forecast"]["forecastday"]

            forecast_time = list(filter(lambda x: x["date"] == when_str, forecast_day))[
                0
            ]["hour"]

            delta = []
            for el in forecast_time:
                datetime_el = datetime.strptime(el["time"], "%Y-%m-%d %H:%M")
                datetime_el = datetime_el.replace(tzinfo=timezone.utc)

                delta.append(abs(when - datetime_el))

            min_delta_index = delta.index(min(delta))

            result = forecast_time[min_delta_index]
            temp_celsium = result["temp_c"]
            is_precipitation = bool(result["precip_mm"])

            return temp_celsium, is_precipitation

        except:
            return None


class OpenMeteoApi(BaseApi):
    def __init__(self):
        self.now_url = OPEN_METEO_NOW_URL
        self.forecast_url = OPEN_METEO_FORECAST_URL

    async def get_now_data(
        self, latitude: float, longitude: float
    ) -> tuple[float, bool] | None:
        try:
            response_json = await self.fetch_url(
                self.now_url.format(latitude, longitude)
            )
            temp_celsium = response_json["current"]["temperature_2m"]
            is_precipitation = bool(response_json["current"]["precipitation"])

            return temp_celsium, is_precipitation

        except:
            return None

    async def get_forecast_data(
        self, latitude: float, longitude: float, when: datetime
    ) -> tuple[float, bool] | None:
        try:
            response_json = await self.fetch_url(
                self.forecast_url.format(latitude, longitude)
            )

            forecast_time = [
                datetime.strptime(i, "%Y-%m-%dT%H:%M")
                for i in response_json["hourly"]["time"]
            ]
            delta = []
            for el in forecast_time:
                el = el.replace(tzinfo=timezone.utc)

                delta.append(abs(when - el))

            min_delta_index = delta.index(min(delta))

            if response_json["hourly"]["temperature_2m"][min_delta_index] is None:
                return None

            temp_celsium = response_json["hourly"]["temperature_2m"][min_delta_index]
            is_precipitation = bool(
                response_json["hourly"]["precipitation"][min_delta_index]
            )

            return temp_celsium, is_precipitation

        except:
            return None

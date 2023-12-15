import asyncio
from datetime import datetime

import httpx
from fastapi import HTTPException

from api_class_module import OpenMeteoApi, WeatherapiApi
from config import API_NINJAS_API_KEY, API_NINJAS_URL, OPENCAGEDATA_URL


async def get_now_weather(city: str, country: str) -> dict:
    latitude, longitude = await get_coordinates(city, country)

    api_classes = (WeatherapiApi(), OpenMeteoApi())

    return await get_now_data_from_api(latitude, longitude, api_classes)


async def get_now_data_from_api(
    latitude: float, longitude: float, api_classes: tuple[WeatherapiApi, OpenMeteoApi]
) -> (float, bool):
    tasks = [api.get_now_data(latitude, longitude) for api in api_classes]

    responses = await asyncio.gather(*tasks)

    if all(el is None for el in responses):
        raise HTTPException(status_code=503, detail="Connection to weather api error")

    else:
        responses = list(filter(lambda x: x is not None, responses))
        result = {
            "temp_celsium": str(sum(item[0] for item in responses) / len(responses)),
            "is_precipitation": bool(sum(item[1] for item in responses)),
        }
        return result


async def get_forecast_weather(city: str, country: str, when: datetime) -> dict:
    latitude, longitude = await get_coordinates(city, country)

    api_classes = (WeatherapiApi(), OpenMeteoApi())

    return await get_forecast_data_from_api(latitude, longitude, when, api_classes)


async def get_forecast_data_from_api(
    latitude: float, longitude: float, when: datetime, api_classes: tuple[WeatherapiApi, OpenMeteoApi]
) -> (float, bool):
    tasks = [api.get_forecast_data(latitude, longitude, when) for api in api_classes]

    responses = await asyncio.gather(*tasks)

    if all(el is None for el in responses):
        raise HTTPException(status_code=503, detail="Connection to weather api error")

    else:
        responses = list(filter(lambda x: x is not None, responses))

        result = {
            "temp_celsium": str(sum(item[0] for item in responses) / len(responses)),
            "is_precipitation": bool(sum(item[1] for item in responses)),
        }
        return result


async def get_coordinates(city: str, country: str) -> (float, float):
    api_url = OPENCAGEDATA_URL.format(city, country)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            response_json = response.json()

            return (
                response_json["results"][0]["geometry"]["lat"],
                response_json["results"][0]["geometry"]["lng"],
            )
    except:
        try:
            api_url = API_NINJAS_URL.format(city, country)

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    api_url,
                    headers={"X-Api-Key": API_NINJAS_API_KEY},
                )
                response_json = response.json()

                if not response_json:
                    raise HTTPException(status_code=404, detail="City not found")

                return (
                    response_json[0]["latitude"],
                    response_json[0]["longitude"],
                )

        except httpx.ConnectError:
            raise HTTPException(
                status_code=503, detail="Connection to geocoding api error"
            )

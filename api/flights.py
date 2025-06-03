import httpx
from config import config


async def search_flights(origin: str, way: bool, destination: str, departure_at: str ):
    """
    Get prices for dates from Travelpayouts API
    
    Args:
        origin (str): Origin IATA code (e.g., 'MOW' for Moscow)
        
    Returns:
        dict: API response with flight prices
    """
    url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
    params = {
        "origin": origin,
        "destination": destination,
        "departure_at": departure_at,
        "one_way": way,
        "token": config.API_TOKEN
    }

    print(params)
    print('------')
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        # print(response.json())
        return response.json()

async def get_locations_by_city_name(city_name: str) -> list:
    url = "https://autocomplete.travelpayouts.com/places2"
    params = {
        "locale": "ru",
        "types[]": ["airport", "city"],
        "term": city_name
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(f"Ошибка запроса к API: {e}")
        return []  # <--- возвращаем всегда список

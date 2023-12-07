import aiohttp
import asyncio
PARKING_LOT_ID = '20'
SERVER_URL = 'https://ut-parking-2b4e7c471d76.herokuapp.com'

async def send_request(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            return response.status == 200

async def send_increase():
    """Asynchronously sends a request to increase parking lot capacity."""
    return await send_request(f'{SERVER_URL}/increase/{PARKING_LOT_ID}', {'amount': 1})

async def send_decrease():
    """Asynchronously sends a request to decrease parking lot capacity."""
    return await send_request(f'{SERVER_URL}/decrease/{PARKING_LOT_ID}', {'amount': 1})
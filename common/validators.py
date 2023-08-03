from aiohttp.web import Request

from common import base
from common.exceptions import EmptyJsonData, WrongJsonData


async def validate_client_amount_request(request: Request) -> dict:
    if request.body_exists:
        request_data = await request.json()
    else:
        raise EmptyJsonData
    for currency in request_data:
        if currency.upper() not in base.CURRENCIES or not isinstance(request_data[currency], (int, float)):
            raise WrongJsonData
    return request_data

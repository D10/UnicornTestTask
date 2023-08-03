from typing import Union, Optional
import json

import aiohttp

from common.base import logger


async def base_get_request(url: str) -> Optional[dict]:
    async with aiohttp.ClientSession() as session:
        logger.debug(f'request to {url}')
        response = await session.get(url)
        response_text = await response.text()
        if response.status == 200:
            response_json = json.loads(response_text)
            logger.debug(f'response from {url} === {response_json}')
            return response_json
        logger.debug(f'Unsuccessful request to {url}! Response === {response_text}')
        raise aiohttp.ClientResponseError


def bool_check(value: Union[bool, str]):
    if type(value) is bool:
        return value
    return True if value.lower() in ('true', 'yes', 'y') else False

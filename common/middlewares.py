import json
from typing import Callable, Awaitable

from aiohttp import web

from common.exceptions import UnicornBaseException
from common.base import logger


@web.middleware
async def error_handler(
        request: web.Request,
        handler: Callable[[web.Request], Awaitable[web.Response]]
):
    try:
        resp = await handler(request)
    except UnicornBaseException as exc:
        logger.error(f'Error response from {request.url}. Message: {exc.msg}')
        return web.Response(text=json.dumps({'status': 'error', 'message': exc.msg}), status=exc.status)
    except Exception as exc:
        logger.error(f'Critical error from {request.url}. Message {exc}')
    else:
        return resp


@web.middleware
async def modify_header(
        request: web.Request,
        handler: Callable[[web.Request], Awaitable[web.Response]]
):
    resp = await handler(request)
    resp.content_type = 'text/plain'
    return resp

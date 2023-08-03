import json

from aiohttp import web

from common import base
from common.middlewares import error_handler, modify_header
from common.client_data_worker import ClientDataWorker
from common.validators import validate_client_amount_request
from common.exceptions import MissedCurrencyError, WrongCurrencyError

app = web.Application(middlewares=[error_handler, modify_header])
routes = web.RouteTableDef()

data_worker = ClientDataWorker()


@routes.post('/amount/set')
async def set_new_client_amount(request: web.Request) -> web.Response:
    request_data = await validate_client_amount_request(request)
    await data_worker.set_new_client_amount(request_data)
    return web.Response(text=json.dumps({'status': 'ok'}))


@routes.post('/modify')
async def modify_client_amount(request: web.Request) -> web.Response:
    request_data = await validate_client_amount_request(request)
    await data_worker.modify_client_amount(request_data)
    return web.Response(text=json.dumps({'status': 'ok'}))


@routes.get('/amount/get')
async def get_client_amount(request: web.Request) -> web.Response:
    client_amount = await data_worker.get_client_amount()
    return web.Response(text=json.dumps(client_amount))


@routes.get('/{currency_name}/get')
async def get_client_currency_balance(request: web.Request) -> web.Response:
    currency_name: str = request.match_info.get('currency_name')

    if not currency_name:
        raise MissedCurrencyError

    currency_name = currency_name.upper()

    if currency_name not in base.CURRENCIES:
        raise WrongCurrencyError

    currency_balance = await data_worker.get_client_currency_balance(currency_name)
    return web.Response(text=json.dumps({'value': currency_balance}))


if __name__ == '__main__':
    app.add_routes(routes)
    web.run_app(app, host=base.HOST, port=base.PORT)

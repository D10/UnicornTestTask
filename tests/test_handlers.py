import json

import pytest
from unittest.mock import AsyncMock

from app import (get_client_currency_balance,
                 get_client_amount,
                 set_new_client_amount,
                 modify_client_amount)

from common.client_data_worker import ClientDataWorker

from tests.data.handlers_data import (GET_CURRENCY_BALANCE,
                                      GET_CLIENT_AMOUNT,
                                      SET_NEW_CLIENT_AMOUNT,
                                      MODIFY_CLIENT_AMOUNT)
from tests.data.mock_data import CLIENT_BALANCE, EXCHANGE_RATES

from tests.utils.fake_request import FakeRequest

ClientDataWorker.get_client_balance = AsyncMock(return_value=CLIENT_BALANCE)
ClientDataWorker.get_exchange_rates = AsyncMock(return_value=EXCHANGE_RATES)
ClientDataWorker._set_client_balance = AsyncMock(return_value='ok')


@pytest.mark.asyncio
@pytest.mark.parametrize('test_input,expected', GET_CURRENCY_BALANCE)
async def test_get_currency_balance(test_input, expected):
    test_request = FakeRequest(**test_input)

    if error := expected.get('error'):
        with pytest.raises(error):
            await get_client_currency_balance(test_request)
    else:
        response = await get_client_currency_balance(test_request)
        response_json = json.loads(response.text)
        assert response_json == expected.get('response')


@pytest.mark.asyncio
@pytest.mark.parametrize('expected', GET_CLIENT_AMOUNT)
async def test_get_client_amount(expected):
    test_request = FakeRequest()

    response = await get_client_amount(test_request)
    response_json = json.loads(response.text)
    assert response_json == expected.get('response')


@pytest.mark.asyncio
@pytest.mark.parametrize('test_input,expected', SET_NEW_CLIENT_AMOUNT)
async def test_set_new_client_amount(test_input, expected):
    test_request = FakeRequest(**test_input)

    if error := expected.get('error'):
        with pytest.raises(error):
            await set_new_client_amount(test_request)
    else:
        response = await set_new_client_amount(test_request)
        response_json = json.loads(response.text)
        assert response_json == expected.get('response')


@pytest.mark.asyncio
@pytest.mark.parametrize('test_input,expected', MODIFY_CLIENT_AMOUNT)
async def test_modify_client_amount(test_input, expected):
    test_request = FakeRequest(**test_input)

    if error := expected.get('error'):
        with pytest.raises(error):
            await set_new_client_amount(test_request)
    else:
        response = await modify_client_amount(test_request)
        response_json = json.loads(response.text)
        assert response_json == expected.get('response')

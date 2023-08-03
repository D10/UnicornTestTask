import asyncio
import os.path
import time

from common.client_data_worker import ClientDataWorker
from common.base import logger
from common import base

data_worker = ClientDataWorker()


def get_update_time() -> (float, float):
    base_currency_file = f'{base.DATA_DIRECTORY}/{base.EXCHANGE_RATES_DIRECTORY}/{base.BASE_CURRENCY.lower()}.csv'
    client_balance_file = f'{base.DATA_DIRECTORY}/{base.CLIENT_BALANCE_FILENAME}'

    return os.path.getmtime(base_currency_file), os.path.getmtime(client_balance_file)


async def main():
    period = base.DEFAULT_PERIOD * 60
    timestamp = 0

    currency_file_last_update, client_balance_last_update = get_update_time()

    while True:
        currency_file_update_time, client_balance_update_time = get_update_time()

        if (
                time.time() - timestamp >= period or
                currency_file_update_time > currency_file_last_update or
                client_balance_update_time > client_balance_last_update
        ):
            amount_data = await data_worker.get_client_amount()

            logger.info(amount_data)

            currency_file_last_update = currency_file_update_time
            client_balance_last_update = client_balance_update_time
            timestamp = time.time()


if __name__ == '__main__':
    asyncio.run(main())

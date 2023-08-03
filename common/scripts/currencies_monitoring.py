import asyncio

import argparse
import logging
import time

from common import base
from common.client_data_worker import ClientDataWorker
from common.utils import bool_check, base_get_request

logger = base.logger

parser = argparse.ArgumentParser(description="script for balance monitoring")

parser.add_argument('--period', dest='period', type=int, default=base.DEFAULT_PERIOD)
parser.add_argument('--debug', dest='debug', type=str, default=base.DEBUG)

for currency in base.CURRENCIES:
    parser.add_argument(f'--{currency.lower()}', dest=currency.lower(), type=float, default=0.0)


class CurrenciesMonitoring(ClientDataWorker):

    def __init__(
            self,
            period: float,
            current_balance: dict,
            debug: bool = False
    ):
        self.period = period
        self.debug = bool_check(debug)
        self.current_balance = current_balance

        self.base_currency = base.BASE_CURRENCY

        if self.debug:
            logger.setLevel(logging.DEBUG)

        base.CURRENCIES.remove(self.base_currency)

    async def get_base_exchange_rates(self) -> dict:
        exchange_rates = await base_get_request(base.EXCHANGES_DATA_URL)

        base_exchange_rates = {}

        for currency in base.CURRENCIES:
            exchange_rate = exchange_rates['Valute'].get(currency)
            if exchange_rate:
                base_exchange_rate = exchange_rate['Nominal'] / exchange_rate['Value']
                base_exchange_rates[currency] = base_exchange_rate
            else:
                logger.warning(f'Currency {currency} is not found in exchange rates!')

        return base_exchange_rates

    async def calculate_exchage_rates(self) -> dict[str: dict]:
        base_exchage_rates = await self.get_base_exchange_rates()

        exchange_rates = {}

        for exchange_rate in base_exchage_rates:
            exchange_rates[exchange_rate] = {}
            exchange_rates[exchange_rate][self.base_currency] = round(1 / base_exchage_rates[exchange_rate], 2)

        for exchange_rate in exchange_rates:
            for calc_rate in exchange_rates:
                if exchange_rate == calc_rate:
                    continue
                exchange_rates[exchange_rate][calc_rate] = round(
                    exchange_rates[exchange_rate][self.base_currency] / exchange_rates[calc_rate][self.base_currency],
                    2
                )

        exchange_rates[self.base_currency] = base_exchage_rates

        return exchange_rates

    async def update_exchange_rates(self):
        exchange_rates = await self.calculate_exchage_rates()
        await self._set_exchange_rates(exchange_rates)

        logger.info('Successfully updated exchange rates')

    async def write_client_balance(self):
        client_balance = await self.get_client_balance()
        income_balance = {key: round(value, 2) for key, value in self.current_balance.items() if value}
        client_balance.update(income_balance)
        await self.set_new_client_amount(client_balance)

    async def main(
            self,
    ):
        logger.info('Start balance monitoring script')

        period = self.period * 60
        timestamp = 0

        await self.write_client_balance()

        while True:
            if time.time() - timestamp >= period:
                await self.update_exchange_rates()
                timestamp = time.time()


if __name__ == '__main__':
    args = parser.parse_args()
    current_balance = {currency: getattr(args, currency.lower()) for currency in base.CURRENCIES}

    monitoring = CurrenciesMonitoring(
        args.period,
        current_balance,
        args.debug
    )

    asyncio.run(
        monitoring.main()
    )

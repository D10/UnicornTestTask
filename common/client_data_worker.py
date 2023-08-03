import aiofiles
from aiocsv import AsyncDictReader, AsyncDictWriter

from common import base
from common.templates.data_reader import DataReader


class ClientDataWorker(DataReader):

    async def _read_csv(self, path: str):
        rows = []
        async with aiofiles.open(path, mode='r', encoding='utf-8', newline='') as csvfile:
            async for row in AsyncDictReader(csvfile, delimiter=','):
                row = {key: float(value) for key, value in row.items()}
                rows.append(row)
        return rows

    async def _write_csv(self, path: str, fieldnames: list, data: dict):
        async with aiofiles.open(path, mode='w', encoding='utf-8', newline='') as csvfile:
            writer = AsyncDictWriter(csvfile, fieldnames)
            await writer.writeheader()
            await writer.writerow(data)
    
    async def _set_client_balance(self, client_balance: dict):
        client_balance = {key: round(value, 2) for key, value in client_balance.items()}
        await self._write_csv(
            f'{base.DATA_DIRECTORY}/{base.CLIENT_BALANCE_FILENAME}',
            list(client_balance),
            client_balance
        )
    
    async def _set_exchange_rates(self, exchange_rates: dict):
        for exchange_rate in exchange_rates:
            exchange_rate_data = {key: round(value, 2) for key, value in exchange_rates[exchange_rate].items()}
            await self._write_csv(
                f'{base.DATA_DIRECTORY}/{base.EXCHANGE_RATES_DIRECTORY}/{exchange_rate.lower()}.csv',
                list(exchange_rate_data.keys()),
                exchange_rate_data
            )

    async def get_exchange_rate(self, currency: str) -> dict:
        exchange_rates = await self._read_csv(
            f'{base.DATA_DIRECTORY}/{base.EXCHANGE_RATES_DIRECTORY}/{currency.lower()}.csv'
        )
        return exchange_rates[0] if exchange_rates else {}

    async def get_exchange_rates(self) -> dict:
        exchange_rates = {}

        for currency in base.CURRENCIES:
            exchange_rate = await self.get_exchange_rate(currency)
            exchange_rates[currency] = exchange_rate

        return exchange_rates
    
    async def get_client_balance(self) -> dict:
        client_balance = await self._read_csv(f'{base.DATA_DIRECTORY}/{base.CLIENT_BALANCE_FILENAME}')
        return client_balance[0] if client_balance else {}

    async def get_client_currency_balance(self, currency: str) -> float:
        client_balance = await self.get_client_balance()
        return client_balance[currency.upper()]

    async def get_client_amount(self) -> dict[str: dict]:
        exchange_rates = await self.get_exchange_rates()
        client_balance = await self.get_client_balance()

        currencies_sum = {}

        for currency_balance in client_balance:
            currency_sum = client_balance[currency_balance]
            for convert_balance in client_balance:
                if currency_balance == convert_balance:
                    continue
                currency_sum += exchange_rates.get(convert_balance, {}).get(currency_balance, 0.0) * \
                                client_balance.get(convert_balance, 0.0)
            currencies_sum[currency_balance] = currency_sum

        showing_exchanges = {}

        for showing_exchange in base.SHOWING_EXCHANGE_RATES:
            prime, convert = showing_exchange.upper().split('-')
            showing_exchanges[showing_exchange] = exchange_rates.get(prime, {}).get(convert, 0.0)

        return {
            'balance': client_balance,
            'exchange_rates': showing_exchanges,
            'currencies_sum': currencies_sum
        }

    async def set_new_client_amount(self, balance_values: dict):
        client_balance = await self.get_client_balance()
        for balance_value in balance_values:
            client_balance[balance_value.upper()] = float(balance_values[balance_value])
        
        await self._set_client_balance(client_balance)
    
    async def modify_client_amount(self, balance_values: dict):
        client_balance = await self.get_client_balance()
        for balance_value in balance_values:
            client_balance[balance_value.upper()] += float(balance_values[balance_value])

        await self._set_client_balance(client_balance)

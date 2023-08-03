import logging

DEBUG = False

HOST = '0.0.0.0'
PORT = 8080

DATA_DIRECTORY = 'data'
EXCHANGE_RATES_DIRECTORY = 'exchange_rates'
CLIENT_BALANCE_FILENAME = 'current_balance.csv'

EXCHANGES_DATA_URL = 'https://www.cbr-xml-daily.ru/daily_json.js'

DEFAULT_PERIOD = 1

CURRENCIES = [
    'RUB',
    'USD',
    'EUR'
]

BASE_CURRENCY = 'RUB'

SHOWING_EXCHANGE_RATES = (
    'usd-rub',
    'eur-rub',
    'usd-eur'
)

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler('logs/log.log', 'a', 'utf-8')],
    format="LEVEL===%(levelname)s TIMESTAMP===%(asctime)s TEXT===%(message)s"
)
logging.getLogger('asyncio').setLevel(logging.WARNING)
logging.getLogger('aiohttp').setLevel(logging.WARNING)
logger = logging.getLogger('my_logger')

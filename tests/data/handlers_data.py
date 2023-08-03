from common.exceptions import (MissedCurrencyError,
                               WrongCurrencyError,
                               EmptyJsonData,
                               WrongJsonData)


GET_CURRENCY_BALANCE = [
    (
        {
            'match_info': {'currency_name': 'usd'}
        },
        {
            'response': {'value': 100}
        }
    ),
    (
        {
            'match_info': {'some': 'test'}
        },
        {
            'error': MissedCurrencyError
        }
    ),
    (
        {
            'match_info': {'currency_name': 'kzt'}
        },
        {
            'error': WrongCurrencyError
        }
    ),
]

GET_CLIENT_AMOUNT = [
    (
        {
            'response': {
                'balance': {
                    'EUR': 100,
                    'RUB': 100,
                    'USD': 100
                },
                'currencies_sum': {
                    'EUR': 192.0,
                    'RUB': 19577.0,
                    'USD': 211.0
                },
                'exchange_rates': {
                    'eur-rub': 101.93,
                    'usd-eur': 0.91,
                    'usd-rub': 92.84}
            }
        }
    )
]

SET_NEW_CLIENT_AMOUNT = [
    (
        {
            'body': {
                'usd': 40,
                'rub': 200
            }
        },
        {
            'response': {'status': 'ok'}
        }
    ),
    (
        {
            'body': {}
        },
        {
            'error': EmptyJsonData
        }
    ),
    (
        {
            'body': {
                'usd': 200,
                'kzt': 500
            }
        },
        {
            'error': WrongJsonData
        }
    )
]

MODIFY_CLIENT_AMOUNT = [
    (
        {
            'body': {
                'rub': 10,
                'eur': -40
            }
        },
        {
            'response': {'status': 'ok'}
        }
    ),
    (
        {
            'body': {}
        },
        {
            'error': EmptyJsonData
        }
    ),
    (
        {
            'body': {
                'usd': 200,
                'kzt': 500
            }
        },
        {
            'error': WrongJsonData
        }
    )
]

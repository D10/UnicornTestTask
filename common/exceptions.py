from abc import ABC


class UnicornBaseException(Exception, ABC):
    msg = None
    status = 400


class MissedCurrencyError(UnicornBaseException):
    msg = 'Missed currency name!'


class WrongCurrencyError(UnicornBaseException):
    msg = 'Wrong currency name!'


class EmptyJsonData(UnicornBaseException):
    msg = 'Json data is empty!'


class WrongJsonData(UnicornBaseException):
    msg = 'Wrong json data!'

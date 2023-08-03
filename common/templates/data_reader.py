from abc import ABC, abstractmethod


class DataReader(ABC):

    @abstractmethod
    async def _read_csv(self, path: str):
        pass

    @abstractmethod
    async def _write_csv(self, path: str, fieldnames: list, data: dict):
        pass

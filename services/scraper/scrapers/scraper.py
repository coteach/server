from abc import ABC, ABCMeta, abstractmethod

from models.plan import Plan


class Scraper(ABC):
    def __init__(self, origin_id: str):
        assert isinstance(origin_id, str)
        self.origin_id = origin_id

    @classmethod
    @abstractmethod
    async def scrape(self) -> [Plan]:
        return NotImplemented

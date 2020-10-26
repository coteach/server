import hashlib
from abc import ABC, ABCMeta, abstractmethod

from models.plan import Plan, PlanFormat


class Scraper(ABC):
    def __init__(self, origin_id: str):
        assert isinstance(origin_id, str)
        self.origin_id = origin_id

    @classmethod
    @abstractmethod
    async def scrape(self) -> [Plan]:
        return NotImplemented

    @classmethod
    def _get_unique_path(self, path: str, index: int) -> str:
        return path + "#" + str(index)

    @classmethod
    def _hash_id(self, unique_path: str) -> str:
        return hashlib.md5(unique_path.encode("utf-8")).hexdigest()

    @classmethod
    def _get_format_from_extension(self, name: str) -> PlanFormat:
        return {
            ".doc": PlanFormat.DOC,
            ".docx": PlanFormat.DOC,
            ".odt": PlanFormat.DOC,
            ".ppt": PlanFormat.PPT,
            ".pptx": PlanFormat.PPT,
            ".pdf": PlanFormat.PDF,
            ".wmv": PlanFormat.VIDEO,
            ".mp4": PlanFormat.VIDEO,
        }.get(name.lower(), PlanFormat.NONE)

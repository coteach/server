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

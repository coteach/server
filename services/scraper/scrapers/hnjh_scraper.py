import asyncio

from models.plan import Plan, PlanFormat
from .scraper import Scraper


class HNJHScraper(Scraper):
    async def scrape(self) -> [Plan]:
        page = "http://www.hnjh.tyc.edu.tw/xoops/uploads/tadnews/file/nsn_7054_4.pdf"

        plan = Plan(
            id=self._hash_id(page),
            origin_id=self.origin_id,
            title="各領域教案彙編",
            page=page,
            formats=[PlanFormat.PDF],
        )
        return [plan]

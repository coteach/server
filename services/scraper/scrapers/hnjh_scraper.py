import asyncio

from models.plan import Plan, PlanFormat
from .scraper import Scraper


class HNJHScraper(Scraper):
    async def get_plans(self) -> [Plan]:
        plan = Plan(
            origin_id=self.origin_id,
            name="各領域教案彙編",
            page="http://www.hnjh.tyc.edu.tw/xoops/uploads/tadnews/file/nsn_7054_4.pdf",
            formats=[PlanFormat.PDF],
        )
        plan.title = plan.name
        return [plan]

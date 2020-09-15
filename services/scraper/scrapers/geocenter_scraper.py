import asyncio
from typing import Final

from models.plan import Plan, PlanFormat
from .scraper import Scraper

MAIN_URL: Final[str] = "https://sites.google.com/view/geocenter/教學資源"


class GeocenterScraper(Scraper):
    async def get_plans(self) -> [Plan]:
        plan1 = Plan(
            origin_id=self.origin_id,
            name="「泰」Men「菲」常女？─外籍勞工之性別分工",
            page=MAIN_URL,
            formats=[PlanFormat.PDF],
        )
        plan1.title = plan1.name

        plan2 = Plan(
            origin_id=self.origin_id,
            name="她與他的校園空間",
            page=MAIN_URL,
            formats=[PlanFormat.PDF],
        )
        plan2.title = plan2.name

        return [plan1, plan2]

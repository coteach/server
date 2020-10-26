import asyncio
from typing import Final

from models.plan import Plan, PlanFormat
from .scraper import Scraper

MAIN_URL: Final[str] = "https://sites.google.com/view/geocenter/教學資源"


class GeocenterScraper(Scraper):
    async def scrape(self) -> [Plan]:
        plan1 = Plan(
            id=self._hash_id(self._get_unique_path(MAIN_URL, 1)),
            origin_id=self.origin_id,
            title="「泰」Men「菲」常女？─外籍勞工之性別分工",
            page=MAIN_URL,
            formats=[PlanFormat.PDF],
        )

        plan2 = Plan(
            id=self._hash_id(self._get_unique_path(MAIN_URL, 2)),
            origin_id=self.origin_id,
            title="她與他的校園空間",
            page=MAIN_URL,
            formats=[PlanFormat.PDF],
        )

        return [plan1, plan2]

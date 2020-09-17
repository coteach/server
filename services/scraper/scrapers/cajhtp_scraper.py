import asyncio
import itertools
from collections import ChainMap
from typing import Final

import requests
from bs4 import BeautifulSoup, ResultSet

from models.plan import Plan, PlanFormat
from .scraper import Scraper

MAIN_URL: Final[str] = "http://www.cajh.tp.edu.tw/tech/"


class CAJHTPScraper(Scraper):
    async def scrape(self) -> [Plan]:
        document = await self._get_document(MAIN_URL)
        plans = self._parse(MAIN_URL, document)
        return plans

    async def _get_document(self, url: str) -> BeautifulSoup:
        response = requests.get(url)
        response.encoding = "utf-8"

        return BeautifulSoup(response.text, "html.parser")

    def _parse(self, url: str, document: BeautifulSoup) -> [Plan]:
        tages = document.select("td")
        plans = []
        for tag in tages:
            name = tag.find("h3").text

            if "示例" in name:
                break

            plan = Plan(
                origin_id=self.origin_id,
                name=name,
                page=url,
                formats=[PlanFormat.HTML],
                description=tag.find("p").text.replace("\r\n                  ", ";"),
            )
            plan.title = plan.name

            plans.append(plan)

        return plans

import asyncio
import itertools
import os
from collections import ChainMap
from typing import Final

import requests
from bs4 import BeautifulSoup, ResultSet
from models.plan import Plan, PlanFormat

from .scraper import Scraper

MAIN_URL: Final[str] = "https://guide.hcc.edu.tw/p/405-1142-224146,c3962.php"


class HCCScraper(Scraper):
    async def scrape(self) -> [Plan]:
        document = await self._get_document(MAIN_URL)
        plans = self._parse(MAIN_URL, document)
        return plans

    async def _get_document(self, url: str) -> BeautifulSoup:
        response = requests.get(url)
        response.encoding = "utf-8"

        return BeautifulSoup(response.text, "html.parser")

    def _parse(self, url: str, document: BeautifulSoup) -> [Plan]:
        tags = document.select(".mptattach a")
        plans = []
        for index, tag in enumerate(tags):
            name, extension = os.path.splitext(tag.text)

            plan = Plan(
                id=self._get_unique_path(MAIN_URL, index),
                origin_id=self.origin_id,
                title=name,
                page=url,
                formats=[self._get_format_from_extension(extension)],
            )

            plans.append(plan)

        return plans

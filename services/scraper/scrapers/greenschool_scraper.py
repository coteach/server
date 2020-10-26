import asyncio
import itertools
from typing import Final

import requests
from bs4 import BeautifulSoup, ResultSet

from models.plan import Plan, PlanFormat

from .scraper import Scraper

MAIN_URL: Final[str] = "https://www.greenschool.moe.edu.tw/gs2/resource/teach.aspx"


class GreenSchoolScraper(Scraper):
    async def scrape(self) -> [Plan]:
        response = await self._get_response()
        document = self._get_document(response)
        cookies = dict(response.cookies)
        start = 1
        stop = self._get_total_page(document) + 1

        tasks = [
            self._get_plans(cookies, document, page) for page in range(start, stop)
        ]

        plans = await asyncio.gather(*tasks)

        return list(itertools.chain(*plans))

    async def _get_plans(
        self, cookies: dict, document: BeautifulSoup, page: int
    ) -> [Plan]:
        document = await self._post(cookies, document, page)
        plans = await asyncio.gather(
            *[
                self._parse(tag, self._get_id(page, index))
                for index, tag in enumerate(self._get_list_group(document))
            ]
        )

        return list(plans)

    async def _post(
        self, cookies: dict, document: BeautifulSoup, page: int
    ) -> BeautifulSoup:
        get_tag = lambda name: document.find("input", {"name": name})

        tags = [
            document.find("input", {"name": "__VIEWSTATE"}),
            document.find("input", {"name": "__VIEWSTATE"}),
            document.find("input", {"name": "__RequestVerificationToken"}),
            document.find("input", {"name": "__VIEWSTATEGENERATOR"}),
            document.find("input", {"name": "__EVENTVALIDATION"}),
        ]

        payload = {
            **{
                "__EVENTTARGET": "ctl00$ctl00$ctl00$body$main$main$ucTeachResource$ucPager$btnQuery",
                "ctl00$ctl00$ctl00$body$main$main$ucTeachResource$ucPager$tbCurrentPage": page,
            },
            **dict((tag.get("name"), tag.get("value")) for tag in tags),
        }

        response = requests.post(MAIN_URL, payload, cookies=cookies)

        return self._get_document(response)

    async def _parse(self, tag: ResultSet, id: str) -> [Plan]:
        anchor_tag = tag.find("a")

        plan = Plan(
            id=id,
            origin_id=self.origin_id,
            title=anchor_tag.text,
            description=tag.contents[2].strip(),
            page=self._get_href(anchor_tag),
            formats=self._get_formats(anchor_tag),
            tags=[tag.find("span").text],
        )

        return plan

    async def _get_response(self) -> requests.Response:
        response = requests.get(MAIN_URL)
        response.encoding = "utf-8"

        return response

    def _get_document(self, response: requests.Response) -> BeautifulSoup:
        return BeautifulSoup(response.text, "html.parser")

    def _get_total_page(self, document: BeautifulSoup) -> int:
        return int(document.select_one("#ucTeachResource_ucPager_lblTotalPage").text)

    def _get_list_group(self, document: BeautifulSoup) -> ResultSet:
        return document.select(".list-group-item")

    def _get_href(self, tag: ResultSet) -> str:
        return tag.get("href")

    def _get_title(self, tag: ResultSet) -> str:
        return tag.get("title")

    def _get_formats(self, tag: ResultSet) -> [PlanFormat]:
        format = PlanFormat.HTML

        if "youtube" in self._get_href(tag):
            format = PlanFormat.VIDEO
        elif "pdf" in self._get_href(tag):
            format = PlanFormat.PDF

        return [format]

    def _get_id(self, page: int, index: int) -> str:
        return self._hash_id(self._get_unique_path(MAIN_URL, page * 100 + index))

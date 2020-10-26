import asyncio
import itertools
from collections import ChainMap
from typing import Final

import requests
from bs4 import BeautifulSoup, ResultSet

from models.plan import Plan, PlanFormat
from .scraper import Scraper

HOME_URL: Final[str] = "http://www.cshs.ntct.edu.tw"
MAIN_URL: Final[str] = (
    HOME_URL + "/editor_model/u_editor_v1.asp?id={24EFC3E4-4286-4080-841D-8F9389C6212E}"
)


class CSHSScraper(Scraper):
    async def scrape(self):
        page_links = await self._get_page_links(MAIN_URL)
        plans = await asyncio.gather(*[self._get_plans(url) for url in page_links])

        return list(itertools.chain(*plans))

    async def _get_page_links(self, url: str):
        document = await self._get_document(url)
        tags = document.select(".C-tableA3 a")
        pages = map(lambda tag: self._get_href(tag), tags)

        return list(pages)

    async def _get_plans(self, url: str) -> [Plan]:
        documents = await self._sort_page(url)
        plans = await asyncio.gather(
            *[self._parse(url, document) for url, document in documents.items()]
        )

        return list(itertools.chain(*plans))

    async def _sort_page(self, url: str) -> dict:
        document = await self._get_document(url)
        result = {url: document}

        if not self._is_download_page(document):
            return {}

        is_category_pages, download_pages = self._get_category_pages(document)
        if is_category_pages:
            ducments = await asyncio.gather(
                *[self._sort_page(page) for page in download_pages]
            )
            return dict(ChainMap(*ducments))

        hasNextPage, downloadPage = self._get_next_page(document)
        if hasNextPage:
            result[downloadPage] = await self._get_document(downloadPage)

        return result

    async def _get_document(self, url: str) -> BeautifulSoup:
        response = requests.get(url)
        response.encoding = "utf-8"

        return BeautifulSoup(response.text, "html.parser")

    def _get_href(self, tag: ResultSet) -> str:
        return tag.get("href")

    def _is_download_page(self, soup: BeautifulSoup) -> bool:
        breadcrumb = soup.select("#way a")[3].text

        return "教案" in breadcrumb and "下載" in breadcrumb

    def _get_category_pages(self, soup: BeautifulSoup) -> (bool, [str]):
        tags = soup.select(".title-A01d a")
        pages = list(map(lambda tag: HOME_URL + tag.get("href"), tags))

        return len(pages) > 0, pages

    def _get_next_page(self, document: BeautifulSoup) -> (bool, str):
        next_tag = document.select_one("a:contains('下一頁')")
        page = ""

        if next_tag != None:
            href = self._get_href(next_tag)
            if href[0] == "/":
                page = HOME_URL + href

        return page != "", page

    async def _parse(self, url: str, document: BeautifulSoup) -> [Plan]:
        tags = document.select(".C-tableA2, .C-tableA3")
        plans = []
        for index, tag in enumerate(tags):
            plan = Plan(
                id=self._hash_id(self._get_unique_path(url, index)),
                origin_id=self.origin_id,
                title=tag.findAll("td")[2].text,
                page=url,
                formats=[PlanFormat.PDF],
            )

            plans.append(plan)

        return plans

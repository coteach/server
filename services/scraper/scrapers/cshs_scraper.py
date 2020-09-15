import asyncio
import itertools
from collections import ChainMap
from typing import Final

import requests
from bs4 import BeautifulSoup, ResultSet

from models.plan import Plan, PlanFormat

HOME_URL: Final[str] = "http://www.cshs.ntct.edu.tw"
MAIN_URL: Final[str] = (
    HOME_URL + "/editor_model/u_editor_v1.asp?id={24EFC3E4-4286-4080-841D-8F9389C6212E}"
)


class CSHSScraper:
    def __init__(self, origin_id: str):
        assert isinstance(origin_id, str)
        self.origin_id = origin_id

    async def get_plans(self) -> [Plan]:
        page_links = await self._get_page_links(MAIN_URL)
        documents = await self._get_documents(page_links)
        plans = [self._parse(url, document) for url, document in documents.items()]
        return list(itertools.chain(*plans))

    async def _get_page_links(self, url: str):
        document = await self._get_document(url)
        tages = document.select(".C-tableA3 a")
        pages = map(lambda tag: self._get_href(tag), tages)

        return list(pages)

    async def _get_documents(self, downloadPages: str) -> dict:
        table_rows = await asyncio.gather(
            *[self._sort_page(page) for page in downloadPages]
        )
        return dict(ChainMap(*table_rows))

    async def _sort_page(self, url: str) -> dict:
        document = await self._get_document(url)
        result = {url: document}

        if not self._is_download_page(document):
            return {}

        is_category_pages, download_pages = self._get_category_pages(document)
        if is_category_pages:
            return await self._get_documents(download_pages)

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
        tages = soup.select(".title-A01d a")
        pages = list(map(lambda tag: HOME_URL + tag.get("href"), tages))

        return len(pages) > 0, pages

    def _get_next_page(self, document: BeautifulSoup) -> (bool, str):
        next_tag = document.select_one("a:contains('下一頁')")
        page = ""

        if next_tag != None:
            href = self._get_href(next_tag)
            if href[0] == "/":
                page = HOME_URL + href

        return page != "", page

    def _parse(self, url: str, document: BeautifulSoup) -> [Plan]:
        tages = document.select(".C-tableA2, .C-tableA3")
        plans = []
        for tag in tages:
            plan = Plan(
                origin_id=self.origin_id,
                name=tag.findAll("td")[2].text,
                page=url,
                formats=[PlanFormat.PDF],
            )
            plan.title = plan.name

            plans.append(plan)

        return plans

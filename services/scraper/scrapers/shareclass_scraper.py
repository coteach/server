import asyncio
import itertools
import json
from typing import Final

import requests

from models.plan import Plan, PlanFormat

from .scraper import Scraper
from .shareclass_response import *

HOME_URL: Final[str] = "https://www.shareclass.org"
MAIN_URL: Final[str] = "https://www.shareclass.org/course/search/?page="


class ShareClassScraper(Scraper):
    async def scrape(self) -> [Plan]:
        response = await self._get_response(1)
        start = 1
        stop = response.page_info.last_page + 1

        tasks = [self._get_plans(page) for page in range(start, stop)]
        plans = await asyncio.gather(
            *tasks,
        )

        return list(itertools.chain(*plans))

    async def _get_plans(self, page: int):
        response = await self._get_response(page)
        plans = await asyncio.gather(
            *[self._parse(course, page) for course in response.course_list]
        )
        return list(itertools.chain(*plans))

    async def _get_response(self, page: int) -> ShareClassResponse:
        response = requests.get(MAIN_URL + str(page))
        response.encoding = "utf-8"

        data = json.loads(response.text)
        return ShareClassResponse.from_dict(data)

    async def _parse(self, course: Course, page) -> [Plan]:
        meta = course.meta
        plan = Plan(
            origin_id=self.origin_id,
            name=meta.name,
            page=HOME_URL + meta.course_page_link,
            formats=self._get_formats(course.materials),
            writers=[meta.author.name],
            description=meta.intro,
            grades=course.grades,
            subject=self._get_subject(course.units, page),
        )
        plan.title = plan.name
        return [plan]

    def _get_formats(self, materials: List[List[Union[int, str]]]):
        FORMATS: Final[dict] = {
            "application/doc": PlanFormat.DOC,
            "application/docx": PlanFormat.DOC,
            "application/pdf": PlanFormat.PDF,
            "video": PlanFormat.VIDEO,
            "application/ppt": PlanFormat.PPT,
            "application/pptx": PlanFormat.PPT,
        }

        formats = [FORMATS[material[2]] for material in materials]
        return list(set(formats))

    def _get_subject(self, units: list, page):
        if units:
            return units[0][0]
        else:
            return None

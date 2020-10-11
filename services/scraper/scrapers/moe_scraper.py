# https://mlearn.moe.gov.tw/TeachingPlan/PartData?key=10450
import asyncio
from bs4 import BeautifulSoup, NavigableString
from models.plan import Plan
from scrapers.scraper import Scraper
from util.logger import logger
from util.session import Session


class MoeScraper(Scraper):
    async def scrape(self) -> [Plan]:
        self.session = Session()
        start = 10314
        end = self.getLast()+1

        plans = await asyncio.gather(
            *[self.job(x) for x in range(start, end)]
        )

        return list(filter(None,plans))

    async def job(self, id) -> Plan:
        def func(type):
            url = f"https://mlearn.moe.gov.tw/{type}/PartData?key={str(id)}"
            soup = BeautifulSoup(self.session.request("GET", url).content, 'html.parser')
            title = soup.select_one("div.container.mt-3 h2")
            if title is None:
                return url,soup,None
            return url,soup,title

        url,soup,title=func("TeachingPlan")
        if title is None:
            url,soup,title=func("TopicArticle")
        if title is None:
            logger.warning(url + " is None because not find title")
            return None

        logger.info("GET data: "+url)
        p = self.parser(soup, title.text, url)
        p.name = "TeachingPlan/PartData?key=" + str(id)
        return p

    def parser(self, soup, title, url):
        tags = []
        writers = []
        subjects = []
        formats = set()
        for tagEle in soup.select(
                "div.container.mt-3 div.d-flex.flex-column.mb-3 div"):
            tagStr = tagEle.text.split('：')

            if tagStr[0] == "科目分類":
                subjects.append(tagStr[1])
            elif tagStr[0] == "作者":
                writers.append(tagStr[1])
            elif tagStr[0] in ["教學指引", "教學媒體", "學習單"]:
                formats.add(self._get_format_from_extension('.'+tagEle.select_one(
                    "a").text.replace("檔案", "").lower()))
            elif tagStr[0] == "上架日期":
                pass
            else:
                tags.append(tagStr[0]+":"+tagStr[1])

        for tag in soup.select("div.container.mt-3 a.badge.badge-pill.badge-info.mb-3"):
            tags.append('網路'+":"+tag.text)

        grades = []
        for tag in soup.select("div.container.mt-3 a.badge.badge-pill.badge-success.mb-3"):
            try:
                grades += self.audience_parser(tag.text)
            except KeyError as e:
                pass

        content = ""
        img = ""
        for section in soup.select_one("div.d-flex.justify-content-end.border-bottom.mb-3").next_siblings:
            if type(section) is not NavigableString:
                imgEle = section.select_one("img")
                if imgEle is not None and len(img) == 0:
                    img = imgEle['src']
            content += str(section)

        return Plan(
            origin_id=self.origin_id,
            title=title,
            writers=writers,
            tags=list(tags),
            page=url,
            grades=grades,
            subjects=subjects,
            formats=list(formats),
            description=content,
            img=img
        )

    def audience_parser(self, content):
        return {
            "國小": [x for x in range(1, 7)],
            "國中": [x for x in range(7, 10)],
            "高中": [x for x in range(10, 13)],
        }[content]

    def getLast(self):
        url = "https://mlearn.moe.gov.tw/"
        soup = BeautifulSoup(self.session.request(
            "GET", url).content, 'html.parser')
        href = soup.select_one(
            ".col-lg-4.d-flex.flex-column.justify-content-between.h-100 a")['href']
        key = "/PartData?key="
        return int(href[href.index(key)+len(key):])

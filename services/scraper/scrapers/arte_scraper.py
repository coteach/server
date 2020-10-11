#  from https://ed.arte.gov.tw/ch/content/m_design_content_1.aspx?AE_SNID=465
from datetime import datetime
from queue import Queue

from bs4 import BeautifulSoup
# from html2text import html2text
import os

from models.plan import Plan, PlanFormat
from scrapers.scraper import Scraper
from util.logger import logger
from util.session import Session
import asyncio


class ArteScraper(Scraper):
    async def scrape(self) -> [Plan]:
        self.session = Session()
        start = 1
        end = self.getLast()+1
        plans = await asyncio.gather(
            *[self.job(x) for x in range(start, end)]
        )

        return list(filter(None,plans))

    async def job(self, id):
        url = "https://ed.arte.gov.tw/ch/content/m_design_content.aspx?AE_SNID=" + \
            str(id)
        res = self.session.request("GET", url)
        if res is None:
            logger.warning(url + " is None")
            return None
        soup = BeautifulSoup(res.content, 'html.parser')
        title = soup.select_one(
            "div.title_wrapper h3.animate.title-c1.title_icon_news").text
        if len(title) == 0:
            logger.warning(url + " is None because not find title")
            return None
        logger.info("GET data: " + url)

        p = self.parser(soup, title, url)
        p.name = "m_design_content.aspx?AE_SNID=" + str(id)
        return p

    def parser(self, soup, title, url):
        tags = []
        grades = []
        writers = []
        subjects = []
        for tag in soup.select(
                "div.author-date div.column.one-second.column_column span.f_c3.title_icon_chevron.m_left_10"):
            tag = tag.text.split(':')
            for content in tag[1].split('.'):
                if len(content) == 0:
                    continue
                content = content.strip()
                if tag[0] == "教學設計者":
                    writers.append(content)
                elif tag[0] == "適用對象":
                    grades.append(self.audience_parser(content))
                elif tag[0] == "學習領域":
                    subjects.append(content)
                else:
                    tags.append(tag[0].strip()+":" + content)

        content = ""
        for section in soup.select("div.entry-content div.the_content_wrapper"):
            for section2 in section.contents:
                # content += html2text(str(section2))
                content += str(section2)

        formats = set()
        for a in soup.select('div.column.one.author-box div.desc-wrapper div.desc a'):
            formats.add(self._get_format_from_extension(os.path.splitext(a['href'])[1]))

        return Plan(
            origin_id=self.origin_id,
            title=title,
            writers=writers,
            tags=list(tags),
            page=url,
            grades=grades,
            subjects=subjects,
            formats=list(formats),
            # description=content
        )

    def audience_parser(self, content):
        return {
            "高中三年級": 12,
            "高中二年級": 11,
            "高中一年級": 10,
            "國中三年級": 9,
            "國中二年級": 8,
            "國中一年級": 7,
            "小學六年級": 6,
            "小學五年級": 5,
            "小學四年級": 4,
            "小學三年級": 3,
            "小學二年級": 2,
            "小學一年級": 1
        }[content]

    def getLast(self):
        l = []
        for i in [1, 2, 3]:
            url = "https://ed.arte.gov.tw/ch/content/m_design_list_%d.aspx" % i
            soup = BeautifulSoup(self.session.request(
                "GET", url).content, 'html.parser')
            href = soup.select_one(
                ".post-title .entry-title-c1.title_icon_news a")['href']
            l.append(int(href.replace("m_design_content_%d.aspx?AE_SNID=" % i, "")))
        return max(l)

# https://sportsbox.sa.gov.tw/material/detail/301
from bs4 import BeautifulSoup, NavigableString
import os
from models.plan import Plan
from scrapers.scraper import Scraper
from util.logger import logger
from util.session import Session
import asyncio

class SportsboxScraper(Scraper):
    async def scrape(self) -> [Plan]:
        self.session = Session()
        start = 1
        end = self.getLast()+1

        plans = await asyncio.gather(
            *[self.job(x) for x in range(start, end)]
        )

        return list(filter(None,plans))

    async def job(self, id):
        url = "https://sportsbox.sa.gov.tw/material/detail/" + str(id)
        res = self.session.request("GET", url)
        if res is None:
            logger.warning(url + " is None")
            return None
        soup = BeautifulSoup(res.content, 'html.parser')
        title = soup.select_one("div.article_titleBox div.h4")
        if title is None:
            logger.warning(url + " is None because not find title")
            return None
        logger.info("GET data: " + url)
        p = self.parser(soup, title.text, url)
        p.name = "/material/detail/" + str(id)
        return p

    def parser(self, soup, title, url):
        fileInContent = True
        grades = []
        tags = []
        formats = set()
        for infoRow in soup.select(
                "div.right_dataBox.box_shadow.b_radius div.row.infoRow div.col-12"):
            # tags, grades
            for tagEle in infoRow.select("div.article_tag.rounded"):
                try:
                    grades += self.audience_parser(tagEle.text)
                except KeyError as e:
                    pass
                else:
                    tags.append("運動:" + tagEle.text)

            # formats
            # 舊版網頁會將formats放在article_box
            eles = infoRow.select(
                "div.row.no-gutters.article_box_file div.col.file_name a")
            for a in eles:
                if fileInContent:
                    fileInContent = False
                formats.add(self._get_format_from_extension(os.path.splitext(a.text)[1]))

        # tags, writers
        # 舊版網頁會有些tags放在editBox
        writers = set()
        # https://stackoverflow.com/questions/4188933/how-do-i-select-the-innermost-element
        for p in soup.select('div.editBox p'):
            if not fileInContent:
                key = None
                for strong in p.select("strong"):  # id 1~223
                    if "：" in strong.text:
                        arr = strong.text.split("：")
                        key = arr[0].replace("\u3000", "")
                        if key in ["作者", "姓名"]:
                            v = arr[1].strip()
                            if v.endswith("、"):
                                writers.add(v[:-1])
                            else:
                                writers = writers.union(set(v.split("、")))
                        elif key in ["獎項", "教案名稱"]:
                            tags.append(key+":" + arr[1])
                    elif key in ["作者", "姓名"]:
                        writers.add(strong.text.replace("、", ""))

            # 223~229 作者藏在內文
            # 231~301 file In Content
            # TODO
            # else: # https://sportsbox.sa.gov.tw/material/detail/231
                # print("file In Content")
                # after=p.select_one("span strong a").next_siblings

        img = ""
        content = soup.select_one("div.article_contentBox div.editBox").text
        # for section in soup.select_one("div.d-flex.justify-content-end.border-bottom.mb-3").next_siblings:
        #     # print(str(section))
        #     if type(section) is not NavigableString:
        #         imgEle=section.select_one("img")
        #         if imgEle is not None and len(img)==0:
        #             img=imgEle['src']
        #     content += str(section)

        return Plan(
            origin_id=self.origin_id,
            title=title,
            writers=list(writers),
            tags=list(tags),
            page=url,
            grades=grades,
            subjects=["體育"],
            formats=list(formats),
            description=content,
            img=img
        )

    def audience_parser(self, content):
        return {
            "1-2年級": [1, 2],
            "3-4年級": [3, 4],
            "5-6年級": [5, 6],
            "7-9年級": [7, 8, 9],
            "10-12年級": [10, 11, 12],
        }[content]

    def getLast(self):
        l = []
        for id in [10, 11, 12, 13]:
            url = "https://sportsbox.sa.gov.tw/material/list/" + str(id)
            res = self.session.request("GET", url)
            if res is None:
                logger.warning(url + " is None")
                return
            soup = BeautifulSoup(res.content, 'html.parser')
            href = soup.select_one(
                "div.itemBox.unit3_v.rounded.box_shadow.itemCard a")['href']
            l.append(int(href.replace("/material/detail/", "")))
        return max(l)

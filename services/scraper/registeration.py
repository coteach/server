from enum import Enum, auto
from typing import Final

from models.plan_origin import PlanOrigin
from scrapers.cajhtp_scraper import CAJHTPScraper
from scrapers.cshs_scraper import CSHSScraper, Scraper
from scrapers.hnjh_scraper import HNJHScraper


class Origin(Enum):
    # 國立竹山高級中學
    CSHS = auto()
    # 桃園市立興南國民中學
    HNJH = auto()
    # 108科技領域資訊科技新課綱與素養導向資源分享
    CAJHTP = auto()

    def create_scraper(self) -> Scraper:
        return scraper_factory[self]()


scraper_factory: Final[dict] = {
    Origin.CSHS: lambda: CSHSScraper(Origin.CSHS.name),
    Origin.HNJH: lambda: HNJHScraper(Origin.HNJH.name),
    Origin.CAJHTP: lambda: CAJHTPScraper(Origin.CAJHTP.name),
}


Origins: Final[PlanOrigin] = [
    PlanOrigin(
        id=Origin.CSHS.name,
        name="國立竹山高級中學 > 教學資源下載",
        url="http://www.cshs.ntct.edu.tw/editor_model/u_editor_v1.asp?id={24EFC3E4-4286-4080-841D-8F9389C6212E}",
        logo="http://www.cshs.ntct.edu.tw/mediafile/1449/news_editor/254/pic/0001.bmp",
    ),
    PlanOrigin(
        id=Origin.HNJH.name,
        name="桃園市立興南國民中學",
        url="http://www2.hnjh.tyc.edu.tw/index.php",
        logo="https://upload.wikimedia.org/wikipedia/zh/d/d4/Hsing_Nan_Junior_High_Schoo_Logol.gif",
    ),
    PlanOrigin(
        id=Origin.CAJHTP.name,
        name="108科技領域資訊科技新課綱與素養導向資源分享",
        url="http://www.cajh.tp.edu.tw/tech/",
        logo="http://www.cajh.tp.edu.tw/tech/img/profile.jpg",
    ),
]

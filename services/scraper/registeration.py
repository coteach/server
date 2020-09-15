from enum import Enum, auto
from typing import Final

from models.plan_origin import PlanOrigin
from scrapers.cshs_scraper import CSHSScraper, Scraper


class Origin(Enum):
    # 國立竹山高級中學
    CSHS = auto()

    def create_scraper(self) -> Scraper:
        return scraper_factory[self]()


scraper_factory: Final[dict] = {
    Origin.CSHS: lambda: CSHSScraper(Origin.CSHS.name),
}


Origins: Final[PlanOrigin] = [
    PlanOrigin(
        id=Origin.CSHS.name,
        name="國立竹山高級中學 > 教學資源下載",
        url="http://www.cshs.ntct.edu.tw/editor_model/u_editor_v1.asp?id={24EFC3E4-4286-4080-841D-8F9389C6212E}",
        logo="http://www.cshs.ntct.edu.tw/mediafile/1449/news_editor/254/pic/0001.bmp",
    ),
]

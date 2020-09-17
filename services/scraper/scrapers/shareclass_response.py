from enum import Enum
from dataclasses import dataclass
from typing import Any, List, Optional, Union, TypeVar, Type, cast, Callable


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


@dataclass
class Author:
    link: str
    avatar_url: str
    name: str

    @staticmethod
    def from_dict(obj: Any) -> "Author":
        assert isinstance(obj, dict)
        link = from_str(obj.get("link"))
        avatar_url = from_str(obj.get("avatar_url"))
        name = from_str(obj.get("name"))
        return Author(link, avatar_url, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["link"] = from_str(self.link)
        result["avatar_url"] = from_str(self.avatar_url)
        result["name"] = from_str(self.name)
        return result


@dataclass
class Meta:
    count_of_download: int
    count_of_collect: int
    id: str
    intro: str
    privacy_level: int
    course_page_link: str
    name: str
    author: Author
    count_of_view: int
    upload_time: str
    count_of_comment: int

    @staticmethod
    def from_dict(obj: Any) -> "Meta":
        assert isinstance(obj, dict)
        count_of_download = from_int(obj.get("count_of_download"))
        count_of_collect = from_int(obj.get("count_of_collect"))
        id = from_str(obj.get("id"))
        intro = from_str(obj.get("intro"))
        privacy_level = from_int(obj.get("privacy_level"))
        course_page_link = from_str(obj.get("course_page_link"))
        name = from_str(obj.get("name"))
        author = Author.from_dict(obj.get("author"))
        count_of_view = from_int(obj.get("count_of_view"))
        upload_time = from_str(obj.get("upload_time"))
        count_of_comment = from_int(obj.get("count_of_comment"))
        return Meta(
            count_of_download,
            count_of_collect,
            id,
            intro,
            privacy_level,
            course_page_link,
            name,
            author,
            count_of_view,
            upload_time,
            count_of_comment,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["count_of_download"] = from_int(self.count_of_download)
        result["count_of_collect"] = from_int(self.count_of_collect)
        result["id"] = from_str(self.id)
        result["intro"] = from_str(self.intro)
        result["privacy_level"] = from_int(self.privacy_level)
        result["course_page_link"] = from_str(self.course_page_link)
        result["name"] = from_str(self.name)
        result["author"] = to_class(Author, self.author)
        result["count_of_view"] = from_int(self.count_of_view)
        result["upload_time"] = from_str(self.upload_time)
        result["count_of_comment"] = from_int(self.count_of_comment)
        return result


@dataclass
class Course:
    # related_junyi_video_id: str
    grades: List[int]
    meta: Meta
    has_viewed: bool
    is_collected: bool
    units: List[Optional[str]]
    materials: List[List[Union[int, str]]]
    community: List[Any]
    search_result: None

    @staticmethod
    def from_dict(obj: Any) -> "CourseList":
        assert isinstance(obj, dict)
        # related_junyi_video_id = from_str(obj.get("related_junyi_video_id"))
        grades = from_list(from_int, obj.get("grades"))
        meta = Meta.from_dict(obj.get("meta"))
        has_viewed = from_bool(obj.get("has_viewed"))
        is_collected = from_bool(obj.get("is_collected"))
        units = from_list(
            lambda x: from_list(lambda x: from_union([from_none, from_str], x), x),
            obj.get("units"),
        )
        materials = from_list(
            lambda x: from_list(lambda x: from_union([from_int, from_str], x), x),
            obj.get("materials"),
        )
        community = from_list(lambda x: x, obj.get("community"))
        search_result = from_none(obj.get("search_result"))
        return Course(
            # related_junyi_video_id,
            grades,
            meta,
            has_viewed,
            is_collected,
            units,
            materials,
            community,
            search_result,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        # result["related_junyi_video_id"] = from_str(self.related_junyi_video_id)
        result["grades"] = from_list(from_int, self.grades)
        result["meta"] = to_class(Meta, self.meta)
        result["has_viewed"] = from_bool(self.has_viewed)
        result["is_collected"] = from_bool(self.is_collected)
        result["units"] = from_list(
            lambda x: from_list(lambda x: from_union([from_none, from_str], x), x),
            self.units,
        )
        result["materials"] = from_list(
            lambda x: from_list(lambda x: from_union([from_int, from_str], x), x),
            self.materials,
        )
        result["community"] = from_list(lambda x: x, self.community)
        result["search_result"] = from_none(self.search_result)
        return result


@dataclass
class CurrentQueryParams:
    page: int

    @staticmethod
    def from_dict(obj: Any) -> "CurrentQueryParams":
        assert isinstance(obj, dict)
        page = int(from_str(obj.get("page")))
        return CurrentQueryParams(page)

    def to_dict(self) -> dict:
        result: dict = {}
        result["page"] = from_str(str(self.page))
        return result


@dataclass
class PageInfo:
    # has_previous_page: bool
    last_page: int
    # previous_page_num: int
    # has_next_page: bool
    # current_page: int
    # next_page_num: int

    @staticmethod
    def from_dict(obj: Any) -> "PageInfo":
        assert isinstance(obj, dict)
        # has_previous_page = from_bool(obj.get("has_previous_page"))
        last_page = from_int(obj.get("last_page"))
        # previous_page_num = from_int(obj.get("previous_page_num"))
        # has_next_page = from_bool(obj.get("has_next_page"))
        # current_page = from_int(obj.get("current_page"))
        # next_page_num = from_int(obj.get("next_page_num"))
        return PageInfo(
            # has_previous_page,
            last_page,
            # previous_page_num,
            # has_next_page,
            # current_page,
            # next_page_num,
        )

    # def to_dict(self) -> dict:
    #     result: dict = {}
    #     result["has_previous_page"] = from_bool(self.has_previous_page)
    #     result["last_page"] = from_int(self.last_page)
    #     result["previous_page_num"] = from_int(self.previous_page_num)
    #     result["has_next_page"] = from_bool(self.has_next_page)
    #     result["current_page"] = from_int(self.current_page)
    #     result["next_page_num"] = from_int(self.next_page_num)
    #     return result


@dataclass
class ShareClassResponse:
    # total_search_count: int
    course_list: List[Course]
    # current_query_params: CurrentQueryParams
    page_info: PageInfo

    @staticmethod
    def from_dict(obj: Any) -> "Course":
        # assert isinstance(obj, dict)
        # total_search_count = from_int(obj.get("total_search_count"))
        course_list = from_list(Course.from_dict, obj.get("course_list"))
        # current_query_params = CurrentQueryParams.from_dict(
        #     obj.get("current_query_params")
        # )
        page_info = PageInfo.from_dict(obj.get("page_info"))
        return ShareClassResponse(
            # total_search_count,
            course_list,
            # current_query_params,
            page_info,
        )

    # def to_dict(self) -> dict:
    #     # result: dict = {}
    #     # result["total_search_count"] = from_int(self.total_search_count)
    #     # result["course_list"] = from_list(
    #     #     lambda x: to_class(CourseList, x), self.course_list
    #     # )
    #     # result["current_query_params"] = to_class(
    #     #     CurrentQueryParams, self.current_query_params
    #     # )
    #     result["page_info"] = to_class(PageInfo, self.page_info)
    #     return result


def course_from_dict(s: Any) -> ShareClassResponse:
    return ShareClassResponse.from_dict(s)


def course_to_dict(x: ShareClassResponse) -> Any:
    return to_class(ShareClassResponse, x)

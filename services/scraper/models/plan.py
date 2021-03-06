import json
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Callable, List, Optional, Type, TypeVar, cast

T = TypeVar("T")


class PlanFormat(Enum):
    NONE = auto()
    DOC = auto()
    HTML = auto()
    PDF = auto()
    PPT = auto()
    XLS = auto()
    VIDEO = auto()


def from_str(x: Any) -> str:
    assert isinstance(x, str)
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


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_enum(x: Any) -> str:
    assert isinstance(x, Enum)
    return x.name


def to_enum(x: Any) -> Enum:
    assert isinstance(x, str)
    return PlanFormat[x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Plan:
    id: Optional[str] = None
    origin_id: Optional[str] = None
    title: Optional[str] = None
    page: Optional[str] = None
    formats: Optional[List[PlanFormat]] = None
    writers: Optional[List[str]] = None
    description: Optional[str] = None
    grades: Optional[List[int]] = None
    subjects: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    img: Optional[str] = None
    removed: bool = False

    @staticmethod
    def from_dict(obj: Any) -> "Plan":
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        origin_id = from_union([from_str, from_none], obj.get("origin_id"))
        title = from_union([from_str, from_none], obj.get("title"))
        page = from_union([from_str, from_none], obj.get("page"))
        formats = from_union(
            [lambda x: from_list(to_enum, x), from_none], obj.get("formats")
        )
        writers = from_union(
            [lambda x: from_list(from_str, x), from_none], obj.get("writers")
        )
        description = from_union([from_str, from_none], obj.get("description"))
        grades = from_union(
            [lambda x: from_list(from_int, x), from_none], obj.get("grades")
        )
        subjects = from_union(
            [lambda x: from_list(from_str, x), from_none], obj.get("subjects")
        )
        tags = from_union(
            [lambda x: from_list(from_str, x), from_none], obj.get("tags")
        )
        img = from_union([from_str, from_none], obj.get("img"))
        removed = obj.get("removed")
        return Plan(
            id,
            origin_id,
            title,
            page,
            formats,
            writers,
            description,
            grades,
            subjects,
            tags,
            img,
            removed,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_str, from_none], self.id)
        result["origin_id"] = from_union([from_str, from_none], self.origin_id)
        result["title"] = from_union([from_str, from_none], self.title)
        result["page"] = from_union([from_str, from_none], self.page)
        result["formats"] = from_union(
            [lambda x: from_list(from_enum, x), from_none], self.formats
        )
        result["writers"] = from_union(
            [lambda x: from_list(from_str, x), from_none], self.writers
        )
        result["description"] = from_union([from_str, from_none], self.description)
        result["grades"] = from_union(
            [lambda x: from_list(from_int, x), from_none], self.grades
        )
        result["subjects"] = from_union(
            [lambda x: from_list(from_str, x), from_none], self.subjects
        )
        result["tags"] = from_union(
            [lambda x: from_list(from_str, x), from_none], self.tags
        )
        result["img"] = from_union([from_str, from_none], self.img)
        result["removed"] = self.removed
        return result

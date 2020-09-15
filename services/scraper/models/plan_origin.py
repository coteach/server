from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class PlanOrigin:
    id: str
    name: str
    url: str
    logo: str

    @staticmethod
    def from_dict(obj: Any) -> "PlanOrigin":
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        name = from_str(obj.get("name"))
        url = from_str(obj.get("url"))
        logo = from_str(obj.get("logo"))
        return PlanOrigin(id, name, url, logo)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["name"] = from_str(self.name)
        result["url"] = from_str(self.url)
        result["logo"] = from_str(self.logo)
        return result

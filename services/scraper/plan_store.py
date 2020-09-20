import json
import os
from enum import Enum, auto
from string import Template
from typing import Final

from models.plan import Plan
from models.plan_origin import PlanOrigin

PATH: Final[str] = "outputs/$file_name.json"


class PlanStore:
    _iswriting: bool

    @classmethod
    async def read_original_plans(cls, file_name: str) -> dict:
        path = cls.get_path(file_name)
        if not os.path.isfile(path):
            return {}

        with open(path) as file:
            data = json.load(file)
            plans = [Plan.from_dict(dict) for dict in data]
            return {plan.name: plan for plan in plans}

    @classmethod
    async def write_original_plans(cls, file_name: str, plans: [Plan]) -> str:
        json_string = json.dumps([plan.to_dict() for plan in plans], ensure_ascii=False)
        with open(cls.get_path(file_name), "w") as file:
            file.write(json_string)

        return json_string

    @classmethod
    async def open_plans_file(cls) -> str:
        cls._iswriting = False
        with open(cls.get_path("plans"), "w") as file:
            file.write("[")

    @classmethod
    async def write_plans(cls, json_string: str) -> str:
        with open(cls.get_path("plans"), "a") as file:
            if cls._iswriting:
                file.write(",")
            else:
                cls._iswriting = True
            file.write(json_string[1:-1])

    @classmethod
    async def close_plans_file(cls) -> str:
        with open(cls.get_path("plans"), "a") as file:
            file.write("]")

    @classmethod
    async def write_origin(cls, origins: [PlanOrigin]):
        with open(cls.get_path("origin"), "w") as file:
            data = [origin.to_dict() for origin in origins]
            json.dump(data, file, ensure_ascii=False)

    @classmethod
    def get_path(cls, file_name: str) -> str:
        return Template(PATH).substitute(file_name=file_name)

import json
import os
from string import Template
from typing import Final

from models.plan import Plan
from models.plan_origin import PlanOrigin

PATH: Final[str] = "outputs/$file_name.json"


class PlanStore:
    @classmethod
    async def read(cls, file_name: str) -> dict:
        path = cls.get_path(file_name)
        if not os.path.isfile(path):
            return {}

        with open(path) as file:
            data = json.load(file)
            plans = [Plan.from_dict(dict) for dict in data]
            return {plan.name: plan for plan in plans}

    @classmethod
    async def write(cls, file_name: str, plans: [Plan]):
        with open(cls.get_path(file_name), "w") as file:
            data = [plan.to_dict() for plan in plans]
            json.dump(data, file, ensure_ascii=False)

    @classmethod
    async def write_origin(cls, origins: [PlanOrigin]):
        with open(cls.get_path("origin"), "w") as file:
            data = [origin.to_dict() for origin in origins]
            json.dump(data, file, ensure_ascii=False)

    @classmethod
    def get_path(cls, file_name: str):
        return Template(PATH).substitute(file_name=file_name)

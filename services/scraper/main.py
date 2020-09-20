import asyncio

from models.plan import Plan
from plan_store import PlanStore
from registeration import *


async def update_files():
    await PlanStore.open_plans_file()
    await asyncio.gather(
        *[update_file(value) for value in Origin], update_origin_file()
    )
    await PlanStore.close_plans_file()



async def update_file(origin: Origin):
    plans = await merge_plans(origin)
    json_string = await PlanStore.write_original_plans(origin.name, plans)
    await PlanStore.write_plans(json_string)


async def merge_plans(origin: Origin) -> [Plan]:
    scraper = origin.create_scraper()
    scraper_task = asyncio.create_task(scraper.scrape())
    file_plans = await PlanStore.read_original_plans(origin.name)
    web_plans = await scraper_task

    for web_plan in web_plans:
        if web_plan.name not in file_plans.keys():
            file_plans[web_plan.name] = web_plan

    return file_plans.values()


async def update_origin_file():
    await PlanStore.write_origin(Origins)


asyncio.run(update_files())

import asyncio

from plan_store import PlanStore
from registeration import *


async def update_files():
    await asyncio.gather(
        *[update_file(value) for value in Origin], update_origin_file()
    )


async def update_file(orgin: Origin):
    scraper = orgin.create_scraper()
    scraper_task = asyncio.create_task(scraper.scrape())
    file_plans = await PlanStore.read(orgin.name)
    web_plans = await scraper_task

    for web_plan in web_plans:
        if web_plan.name not in file_plans.keys():
            file_plans[web_plan.name] = web_plan

    await PlanStore.write(orgin.name, file_plans.values())


async def update_origin_file():
    await PlanStore.write_origin(Origins)


asyncio.run(update_files())

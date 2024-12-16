from nonebot import require
from plugins.nonebot_plugin_myGame.person import personMap

scheduler = require("nonebot_plugin_apscheduler").scheduler

@scheduler.scheduled_job("interval", minutes=1)
async def check_last_sent():
    # 遍历所有绑定的 bot 实例
    for person in personMap.values():
        await person.training(False)
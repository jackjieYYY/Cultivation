from nonebot.adapters.onebot.v11 import Bot

from plugins.nonebot_plugin_myGame.person import Person
from plugins.nonebot_plugin_myGame import botPersonMap

from nonebot import get_driver

driver = get_driver()

# 监听连接事件
@driver.on_bot_connect
async def handle_bot_connect(bot: Bot):
    """机器人连接时触发"""
    # 创建一个新的 Person 实例，并绑定到全局字典
    person = Person(bot)
    botPersonMap[bot.self_id] = person
    print(f"Bot {bot.self_id} connected and assigned to a Person instance")

# 监听断开事件
@driver.on_bot_disconnect
async def handle_bot_disconnect(bot: Bot):
    """机器人断开连接时触发"""
    # 从全局字典中移除对应的 Person 实例
    if bot.self_id in botPersonMap:
        del botPersonMap[bot.self_id]
        print(f"Bot {bot.self_id} disconnected and removed from bot_person_map")
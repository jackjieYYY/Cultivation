from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot import on_message
from nonebot.rule import Rule
import time
from plugins.nonebot_plugin_myGame.consts import MY_PRIVATE_GROUP_ID, TARGET_KEYWORDS
from plugins.nonebot_plugin_myGame.person import Person

# 创建一个群消息的监听器
group_message_handler = on_message(
    rule=Rule(lambda event: isinstance(event, GroupMessageEvent) and event.group_id == MY_PRIVATE_GROUP_ID),
    priority=5,
    block=False
)

@group_message_handler.handle()
async def handle_group_message(bot: Bot, event: GroupMessageEvent):
    person = Person.getPerson(bot.self_id)
    if not person:
        return
    message_content = str(event.message)
    if TARGET_KEYWORDS not in message_content:
        return
    await person.training()
    return
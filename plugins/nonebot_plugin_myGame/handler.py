from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot import on_message
from nonebot.rule import Rule
from plugins.nonebot_plugin_myGame.consts import MY_PRIVATE_GROUP_ID
from plugins.nonebot_plugin_myGame.data import getPerson

group_message_handler = on_message(
    rule=Rule(lambda event: isinstance(event, GroupMessageEvent) and event.group_id == MY_PRIVATE_GROUP_ID),
    priority=5,
    block=False
)

@group_message_handler.handle()
async def handle_group_message(bot: Bot, event: GroupMessageEvent):
    person = getPerson(bot.self_id)
    if not person:
        return
    await person.receive(str(event.message))
    return
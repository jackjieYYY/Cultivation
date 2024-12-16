import nonebot
from fastapi import FastAPI
from nonebot.adapters.onebot.v11 import MessageSegment
from plugins.nonebot_plugin_myGame.consts import TARGET_MAIN_GROUP_ID, TARGET_USER_ID

print("api loading")


app: FastAPI = nonebot.get_app()

@app.post("/api/updateName")
async def custom_api():
    # 获取 NoneBot 中的 Bot 实例
    bots = nonebot.get_bots()
    
    if not bots:
        return {"error": "No bot is currently connected"}
    
    bot = list(bots.values())[0]  # 假设只有一个 bot 实例
    
    # 构造消息，包含 @ 的效果
    message = MessageSegment.at(TARGET_USER_ID) + " 修仙改名"
    
    try:
        # 向目标群发送消息
        await bot.send_group_msg(group_id=TARGET_MAIN_GROUP_ID, message=message)
        return {"success": True, "message": "Message sent successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/directLeap")
async def custom_api():
    # 获取 NoneBot 中的 Bot 实例
    bots = nonebot.get_bots()
    if not bots:
        return {"error": "No bot is currently connected"}
    
    bot = list(bots.values())[0]  # 假设只有一个 bot 实例
    
    # 构造消息，包含 @ 的效果
    message = MessageSegment.at(TARGET_USER_ID) + " 直接突破"
    try:
        # 向目标群发送消息
        await bot.send_group_msg(group_id=TARGET_MAIN_GROUP_ID, message=message)
        return {"success": True, "message": "Message sent successfully"}
    except Exception as e:
        return {"error": str(e)}
        
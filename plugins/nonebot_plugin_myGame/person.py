import datetime
from typing import Optional
from nonebot.adapters.onebot.v11 import Bot, MessageSegment
import time
from typing import Dict
from plugins.nonebot_plugin_myGame.consts import  TARGET_USER_ID,MY_PRIVATE_GROUP_ID



personMap: Dict[int, "Person"] = {}

class Person:
    def __init__(self,bot: Bot) -> None:
        self.signInTimestamp: Optional[int] = 0
        self.bot = bot
        self.lastTrainingTimestamp: int = 0
        
    @staticmethod
    def getPerson(botSelfId: int) -> Optional["Person"]:
        """通过 bot.self_id 获取对应的 Person 实例

        Args:
            botSelfId (int): bot 的 self_id

        Returns:
            Optional[Person]: 对应的 Person 实例，若不存在则返回 None
        """
        return personMap.get(botSelfId)
    
    def signIn(self) -> None:
        """记录当前时间为签到时间戳"""
        self.signInTimestamp = int(datetime.now().timestamp())  

    async def training(self,ignoreTimeDiff: bool = True) -> None:
        if self.lastTrainingTimestamp == -1:
            return
        currentTime = time.time()
        if ignoreTimeDiff or currentTime - self.lastTrainingTimestamp > 80:
            replyMessage = MessageSegment.at(TARGET_USER_ID) + " 修炼"
            await self.bot.send_group_msg(group_id=MY_PRIVATE_GROUP_ID, message=replyMessage)
            self.lastTrainingTimestamp = currentTime
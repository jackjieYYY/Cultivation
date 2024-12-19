from enum import Enum
import time
from typing import List
from nonebot.adapters.onebot.v11 import MessageSegment

from plugins.nonebot_plugin_myGame.consts import TARGET_USER_ID


class TaskType(Enum):
    SIGNIN = 0
    PARTYSIGNIN = 1
    TRAINING = 2


class Task:
    def __init__(self, taskType: TaskType) -> None:
        self.type = taskType
        self.createAt = time.time()

    def command(self):
        if self.type == TaskType.SIGNIN:
            return MessageSegment.at(TARGET_USER_ID) + " 修仙签到"
        if self.type == TaskType.PARTYSIGNIN:
            return MessageSegment.at(TARGET_USER_ID) + " 宗门丹药领取"
        if self.type == TaskType.TRAINING:
            return MessageSegment.at(TARGET_USER_ID) + " 修炼"

    def completedKeyWords(self) -> List[str]:
        if self.type == TaskType.SIGNIN:
            return ["贪心的人","签到成功"]
        if self.type == TaskType.PARTYSIGNIN:
            return ["道友已经","道友成功"]
        if self.type == TaskType.TRAINING:
            return ["本次修炼增加"]
        return []
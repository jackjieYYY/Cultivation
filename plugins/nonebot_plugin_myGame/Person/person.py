import datetime
from typing import List, Optional
from nonebot.adapters.onebot.v11 import Bot, MessageSegment
import time

from plugins.nonebot_plugin_myGame.Person.state import StateMachine, State
from plugins.nonebot_plugin_myGame.Person.task import Task, TaskType
from plugins.nonebot_plugin_myGame.consts import MY_PRIVATE_GROUP_ID


class Person:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.state = StateMachine()
        self.taskList: List[Task] = []
        self.privateGroup = MY_PRIVATE_GROUP_ID

    async def init(self) -> None:
        self.state.setState(State.INITIALIZING)
        signInTask = Task(TaskType.SIGNIN)
        self.taskList.append(signInTask)
        await self.send(signInTask.command())
        time.sleep(3)
        partySignInTask = Task(TaskType.PARTYSIGNIN)
        self.taskList.append(partySignInTask)
        await self.send(partySignInTask.command())
        while True:
            time.sleep(3)
            if len(self.taskList) == 0:
                await self.startTraining()
                return

    async def send(self, message) -> None:
        await self.bot.send_group_msg(group_id=self.privateGroup, message=message)
        
    async def receive(self, message: str) -> None:
        # 遍历任务列表，检查并移除匹配的任务
        for task in self.taskList[:]:  # 创建副本以安全地修改列表
            if any(keyword in message for keyword in task.completedKeyWords()):
                print(f"Task completed: {task.type}")
                self.taskList.remove(task)
    
    async def startTraining(self) -> None:
        self.state.setState(State.TRAINING)
        trainTask = Task(TaskType.TRAINING)
        await self.send(trainTask.command())
        self.taskList.append(trainTask)

    async def training(self) -> None:
        if self.state != State.TRAINING:
            return
        trainTask = Task(TaskType.TRAINING)
        self.taskList.append(trainTask)
        await self.send(trainTask.command())

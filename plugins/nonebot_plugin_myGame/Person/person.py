import asyncio
import json
import threading
import time
from typing import List
from nonebot.adapters.onebot.v11 import Bot

from plugins.nonebot_plugin_myGame.Person.state import StateMachine, State
from plugins.nonebot_plugin_myGame.Person.task import Task, TaskType
from plugins.nonebot_plugin_myGame.consts import MY_PRIVATE_GROUP_ID


class Person:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.stateMerchine = StateMachine()
        self.taskList: List[Task] = []
        self.privateGroup = MY_PRIVATE_GROUP_ID
        self.nextInitTimestamp: int = 0
        self.lastTrainingTimestamp: int = 0
        self.load()
        asyncio.create_task(self.init())

    async def init(self) -> None:
        if time.time() < self.nextInitTimestamp:
            self.stateMerchine.setState(State.TRAINING)
            await self.training()
            return
        self.stateMerchine.setState(State.INITIALIZING)
        signInTask = Task(TaskType.SIGNIN)
        partySignInTask = Task(TaskType.PARTYSIGNIN)
        self.taskList.append(signInTask)
        await asyncio.sleep(1)
        self.taskList.append(partySignInTask)
        await self.send(signInTask.command())
        await asyncio.sleep(3)
        await self.send(partySignInTask.command())
        while True:
            await asyncio.sleep(3)
            if len(self.taskList) == 0:
                self.nextInitTimestamp = int(time.time() + 12 * 60 * 60)
                self.save()
                self.stateMerchine.setState(State.TRAINING)
                await self.training()
                return

    async def send(self, message) -> None:
        await self.bot.send_group_msg(group_id=self.privateGroup, message=message)

    async def receive(self, message: str) -> None:
        # 遍历任务列表，检查并移除匹配的任务
        for task in self.taskList[:]:  # 创建副本以安全地修改列表
            if any(keyword in message for keyword in task.completedKeyWords()):
                print(f"Task completed: {task.type}")
                self.taskList.remove(task)
                if task.type == TaskType.TRAINING:
                    await self.training()

    async def training(self) -> None:
        if not self.stateMerchine.isState(State.TRAINING):
            return
        trainTask = Task(TaskType.TRAINING)
        currentTime = time.time()
        if len(self.taskList) == 0:
            self.taskList.append(trainTask)
            await self.send(trainTask.command())
            self.lastTrainingTimestamp = currentTime
            return
        if currentTime - self.lastTrainingTimestamp > 80:
            await self.send(trainTask.command())
            self.lastTrainingTimestamp = currentTime
            return

    def load(self):
        if self.bot is None:
            return
        filePath = f"{self.bot.self_id}.json"
        try:
            with open(filePath, "r") as f:
                data = json.load(f)
            self.from_dict(data)
        except FileNotFoundError:
            pass

    def save(self):
        if self.bot is None:
            return
        filePath = f"{self.bot.self_id}.json"
        with open(filePath, "w") as f:
            json.dump(self.to_dict(), f)

    def to_dict(self):
        return {"nextInitTimestamp": self.nextInitTimestamp}

    def from_dict(self, data):
        self.nextInitTimestamp = data.get("nextInitTimestamp", 0)

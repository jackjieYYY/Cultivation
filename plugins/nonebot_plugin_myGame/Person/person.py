import asyncio
import threading
from typing import List
from nonebot.adapters.onebot.v11 import Bot
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
        threading.Thread(target=self._run_init_in_thread).start()
        
    def _run_init_in_thread(self) -> None:
        """在多线程中运行异步协程"""
        asyncio.run(self.init())  # 启动事件循环并运行异步方法
        
    async def init(self) -> None:
        self.state.setState(State.INITIALIZING)
        signInTask = Task(TaskType.SIGNIN)
        # partySignInTask = Task(TaskType.PARTYSIGNIN)
        self.taskList.append(signInTask)
        time.sleep(3)
        # self.taskList.append(partySignInTask)
        self.send(signInTask.command())
        time.sleep(3)
        # await self.send(partySignInTask.command())
        while True:
            print("start to wait")
            time.sleep(3)
            print(len(self.taskList))
            if len(self.taskList) == 0:
                self.state.setState(State.TRAINING)
                await self.training()
                return

    async def send(self, message) -> None:
        await self.bot.send_group_msg(group_id=self.privateGroup, message=message)
        
    async def receive(self, message: str) -> None:
        print(message)
        # 遍历任务列表，检查并移除匹配的任务
        for task in self.taskList[:]:  # 创建副本以安全地修改列表
            if any(keyword in message for keyword in task.completedKeyWords()):
                print(f"Task completed: {task.type}")
                self.taskList.remove(task)

    async def training(self) -> None:
        if self.state != State.TRAINING:
            return
        trainTask = Task(TaskType.TRAINING)
        self.taskList.append(trainTask)
        await self.send(trainTask.command())

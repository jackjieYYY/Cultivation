from enum import Enum


class State(Enum):
    INITIALIZING = 0  # 初始化状态
    IDLE = 1  # 闲置状态 -》做悬赏任务
    TRAINING = 2  # 修炼状态
    EXPLORING = 3  # 探索状态


class StateMachine:
    def __init__(self):
        self.currentState = State.INITIALIZING

    def setState(self, state: State):
        self.currentState = state

    def isState(self, state: State) -> bool:
        return self.currentState == state

    def nextState(self):
        if self.currentState == State.EXPLORING:
            self.currentState = State.IDLE
        else:
            self.currentState = State((self.currentState.value + 1) % len(State))
        return self.currentState

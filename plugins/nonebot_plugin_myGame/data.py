from typing import Dict, Optional

from plugins.nonebot_plugin_myGame.Person.person import Person

personMap: Dict[int, "Person"] = {}

def getPerson(botSelfId: int) -> Optional["Person"]:
    """通过 bot.self_id 获取对应的 Person 实例

    Args:
        botSelfId (int): bot 的 self_id

    Returns:
        Optional[Person]: 对应的 Person 实例，若不存在则返回 None
    """
    return personMap.get(botSelfId)
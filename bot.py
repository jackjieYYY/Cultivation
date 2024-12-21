import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBotV11Adapter
from nonebot.adapters.console import Adapter as ConsoleAdapter
from nonebot.config import Config

config = Config(host='0.0.0.0')
nonebot.init()

driver = nonebot.get_driver()
# driver.register_adapter(ConsoleAdapter)
driver.register_adapter(OneBotV11Adapter)
nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.run(host='0.0.0.0', port=9000)

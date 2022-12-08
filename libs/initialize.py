import os
from logging import getLogger
from pathlib import Path

import dotenv

from libs.design.singleton import SingletonMeta
from libs.hidden import Normal

logger = getLogger("django")


class InitTrigger(metaclass=SingletonMeta):
    """setting外部变量初始化,单例模式保存状态以防二次初始化"""

    def __init__(self, env_file: Path):
        self.trigger_map = {}
        self.env_file = env_file
        self.is_ok = True

    def init_env_variables(
        self,
        key: str,
        generator_key_func: callable,
        hidden: bool = True,
        force_update: bool = False,
    ) -> str:
        """初始化环境变量

        Args:
            key (str): 关键字
            generator_key_func (callable): 初始化方法
            hidden (bool, optional): 是否脱敏信息. Defaults to True.
            force_update (bool, optional): 是否强制更新. Defaults to False.


        Returns:
            str: 初始化关键字变量结果
        """
        if (data := self.trigger_map.get(key)) and not force_update:
            return data

        logger.debug(f"开始初始化环境变量 {key}")
        dotenv.load_dotenv(dotenv_file := self.env_file.absolute())
        if force_update or not (data := os.getenv(key, "").strip()):
            dotenv.set_key(dotenv_file, key, generator_key_func())
            logger.debug(f"{key} 生成成功,并写入文件: {dotenv_file}")
        else:
            logger.debug(f"{key}已存在 { Normal(data) if hidden else data } ,跳过")
        self.trigger_map[key] = data
        return data

    def init_env_file(self, generator_file_func: callable) -> bool:
        """初始化环境文件,请确认您在setting内执行

        Args:
            generator_file_func (callable): 初始化方法

        Returns:
            bool: 环境文件生成结果
        """

        if self.trigger_map.get(str(generator_file_func)):
            return
        if generator_file_func():
            logger.debug(f"{generator_file_func} 初始化成功")
            return True
        return False

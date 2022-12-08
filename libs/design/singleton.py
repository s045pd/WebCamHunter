import logging
import os
from threading import Lock
from typing import Callable

logger = logging.getLogger("singleton")


class SingletonMeta(type):
    """
    线程安全单例模式，带健康检查
    """

    _instances = {}
    _lock: Lock = Lock()
    _health_code = "is_health"

    def __call__(cls, *args, **kwargs):
        action_str = "[=]reuse"
        with cls._lock:
            pid = os.getpid()

            if not (old_instance := cls._instances.get(cls, None)):
                cls._instances[cls] = super().__call__(*args, **kwargs)
                action_str = "[+]init"
            elif hasattr(old_instance, cls._health_code):
                health_status = getattr(old_instance, cls._health_code)
                if isinstance(health_status, Callable) and (
                    check_result := health_status()
                ):
                    pass
                elif check_result:
                    pass
                else:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
                    action_str = "[^]rebuild"
                    logger.info = logger.warning

        logger.info(f"[{cls}]{action_str} instance:  {id(cls._instances[cls])}({pid})")
        return cls._instances[cls]

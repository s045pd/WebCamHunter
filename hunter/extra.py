import logging
from pathlib import Path

import colorlog
from django.core.management.utils import get_random_secret_key

from libs.initialize import InitTrigger

BASE_VERBOSE_PRETTY = "%(log_color)s%(levelname)s[%(asctime)s]%(blue)s%(filename)s%(white)s:%(cyan)s%(lineno)s\t%(log_color)s%(message)s"

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(BASE_VERBOSE_PRETTY))
logger = logging.getLogger("django")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

BASE_DIR = Path(__file__).resolve().parent.parent

for _ in [
    VOL_DIR := (BASE_DIR / "vol"),
    DB_DIR := (VOL_DIR / "db"),
    LOGS_DIR := (VOL_DIR / "log"),
    SSL_KEY_DIR := (VOL_DIR / "ssl"),
]:
    _.mkdir(parents=True, exist_ok=True)

DEFAULT_ENV_FILE = BASE_DIR / ".env" 
PUBLIC_KEY_FILE = SSL_KEY_DIR / "public.key"
PRIVATE_KEY_FILE = SSL_KEY_DIR / "private.key"
TriggerInstance = InitTrigger(DEFAULT_ENV_FILE)
SECRET_KEY = TriggerInstance.init_env_variables(
    "DJANGO_SECRET_KEY", get_random_secret_key
) 
AES_SECRET_KEY = SECRET_KEY.ljust(32)[:32].encode("utf8")

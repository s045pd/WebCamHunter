from dataclasses import dataclass
from ipaddress import IPv4Address
from math import ceil, floor


@dataclass
class Normal:
    """
    clean senstive data
    """

    key: str
    max_left: int = 2
    mex_right: int = 2
    raise_error: bool = False

    def __post_init__(self):
        if not self.key or not isinstance(self.key, str):
            return
        try:
            old_key = self.key
            self.format()
            assert old_key != self.key
        except Exception as e:
            if self.raise_error:
                raise e
            self.key = self.replace(self.key)

    def format(self) -> None:
        self.key = self.replace(self.key)

    def replace(self, text: str) -> str:
        return text[: self.mex_right] + "*" * 3 + text[-1 * self.max_left :]

    def __str__(self) -> str:
        return str(self.key)

    def __repr__(self) -> str:
        return repr(self.key)

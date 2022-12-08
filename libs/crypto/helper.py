from abc import ABCMeta, abstractmethod
from json import dumps, loads
from logging import getLogger
from pathlib import Path

from libs.crypto import AESCipher, RSACipher
from libs.process import run_cmd

logger = getLogger("django")


class Crypto(metaclass=ABCMeta):
    def __init__(self, private_key_path: Path, public_key_path: Path):
        self.private_key = private_key_path.absolute()
        self.public_key = public_key_path.absolute()

    @abstractmethod
    def gen(self) -> None:
        pass


class InternalCrypto(Crypto):
    """
    服务器密钥生成
    """

    def gen(self):
        """
        通过命令行生成密钥
        """

        logger.debug("开始初始化RSA密钥对")
        gen_public_key = lambda: run_cmd(
            f"openssl rsa -in {self.private_key} -pubout -out {self.public_key}"
        )

        if not self.private_key.exists():
            logger.debug("私钥不存在, 开始生成")
            run_cmd(f"openssl genrsa -out {(self.private_key)} 2048")
            gen_public_key()
            logger.debug(f"私钥生成成功 {self.private_key}")
        else:
            logger.debug(f"私钥已存在 {self.private_key}")

        if not self.public_key.exists():
            logger.debug("公钥不存在, 开始生成")
            gen_public_key()
            logger.debug(f"公钥生成成功 {self.public_key}")
        else:
            logger.debug(f"公钥已存在 {self.public_key}")


class ExternalCrypto(Crypto):
    """
    外部公钥
    """

    def __init__(self, public_key_path: Path):
        self.public_key = public_key_path.absolute()

    def gen(self, content: str) -> None:
        """
        保存密钥方法
        """
        logger.debug(f"开始保存公钥")
        with self.public_key.open("w") as file:
            file.write(content)
        logger.debug(f"外部公钥保存成功 {self.public_key}")


def signature_and_encryption(
    data: dict,
    aes_secret: str,
    internal_private_key: bytes,
    external_public_key: bytes,
) -> dict:
    """签名并加密数据,用于客户端发送请求至服务器

    Args:
        data (dict): 数据内容
        aes_secret (str): aes_key
        internal_private_key (bytes): 内部私钥字节串
        external_public_key (bytes): 外部公钥字节串

    Returns:
        dict: 结果内容
    """
    data |= {"sign": RSACipher(internal_private_key).sign(dumps(data)).decode()}
    return {
        "crypto_data": AESCipher(aes_secret).encrypt(dumps(data)).decode(),
        "cipher_secret": RSACipher(external_public_key).encrypt(aes_secret).decode(),
    }


def decryption(
    cipher_data: dict,
    internal_private_key: bytes,
) -> dict:
    """验签并解密数据,用于服务端解析客户端数据

    Args:
        cipher_data (dict): 加密数据
        internal_private_key (bytes): 内部私钥

    Returns:
        dict: 解密数据
    """

    if set(cipher_data.keys()) != {"crypto_data", "cipher_secret"}:
        return False
    aes_secret = (
        RSACipher(internal_private_key).decrypt(cipher_data["cipher_secret"]).decode()
    )
    return loads(AESCipher(aes_secret).decrypt(cipher_data["crypto_data"]))


def verify(
    data: dict,
    external_public_key: bytes,
) -> bool:
    """验证数据是否被篡改

    Args:
        data (dict): 解密结果数据
        external_public_key (bytes): 外部公钥

    Returns:
        _type_: 是否被篡改
    """

    sign = data.pop("sign")
    return RSACipher(external_public_key).verify_sign(dumps(data), sign)


def decryption_and_verify(
    cipher_data: dict,
    internal_private_key: bytes,
    external_public_key: bytes,
) -> dict:
    """验签并解密数据,用于服务端解析客户端数据

    Args:
        cipher_data (dict): 加密数据
        internal_private_key (bytes): 服务器私钥字节串
        external_public_key (bytes): agent公钥字节串

    Returns:
        dict: 结果内容
    """
    if verify(
        data := decryption(cipher_data, internal_private_key), external_public_key
    ):
        return data
    return {}

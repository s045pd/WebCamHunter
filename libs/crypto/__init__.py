from base64 import b64decode, b64encode
from pathlib import Path

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5

Random.atfork()


def s2b(data: str | bytes) -> bytes:
    """
    自动转bytes
    """
    return data.encode() if isinstance(data, str) else data


class RSACipher:
    def __init__(self, key: bytes):
        self.key = RSA.importKey(s2b(key))

    def encrypt(self, text: bytes) -> bytes:
        cipher = Cipher_pkcs1_v1_5.new(self.key)
        return b64encode(cipher.encrypt(s2b(text)))

    def decrypt(self, enc_text: bytes) -> bytes:
        random_generator = Random.new().read
        cipher = Cipher_pkcs1_v1_5.new(self.key)
        return cipher.decrypt(b64decode(s2b(enc_text)), random_generator)

    def sign(self, text: bytes) -> bytes:
        singer = Signature_pkcs1_v1_5.new(self.key)
        digest = SHA.new()
        digest.update(s2b(text))
        sign = singer.sign(digest)
        return b64encode(sign)

    def verify_sign(self, text: bytes, signature: bytes) -> bool:
        verifier = Signature_pkcs1_v1_5.new(self.key)
        digest = SHA.new()
        digest.update(s2b(text))
        return verifier.verify(digest, b64decode(s2b(signature)))


class AESCipher:
    def __init__(self, key: bytes):
        self.key = s2b(key)
        self.BLOCK_SIZE = 16

    def pad(self, data: bytes) -> bytes:
        return (
            data
            + (
                (self.BLOCK_SIZE - len(data) % self.BLOCK_SIZE)
                * chr(self.BLOCK_SIZE - len(data) % self.BLOCK_SIZE)
            ).encode()
        )

    def unpad(self, data: bytes) -> bytes:
        return data[: -ord(data[len(data) - 1 :])]

    def encrypt(self, raw: bytes) -> bytes:
        cipher = AES.new(self.key, AES.MODE_ECB)
        return b64encode(cipher.encrypt(self.pad(s2b(raw))))

    def decrypt(self, enc: bytes) -> bytes:
        enc = b64decode(s2b(enc))
        cipher = AES.new(self.key, AES.MODE_ECB)
        return self.unpad(cipher.decrypt(enc))

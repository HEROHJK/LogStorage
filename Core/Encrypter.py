import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pathlib import Path
from passwordKey import key, salt

class Encrypter:

    def encrypt(self, plaintext, password=key):
        pbkdf2 = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=1000, backend=default_backend()).derive(password.encode())
        b64 = base64.urlsafe_b64encode(pbkdf2)
        f = Fernet(b64)
        encData = f.encrypt(plaintext.encode())
        return encData.decode()

    def decrypt(self, ciphertext, password=key):
        pbkdf2 = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=1000, backend=default_backend()).derive(password.encode())
        b64 = base64.urlsafe_b64encode(pbkdf2)
        f = Fernet(b64)
        decData = f.decrypt(ciphertext.encode())
        return decData.decode()

    def readEncFile(self, filePath, password=key):
        data = Path(filePath).read_bytes()
        return self.decrypt(data.decode())

    def saveEncFile(self, filePath, data):
        if type(data) != bytes:
            data = data.encode()
        Path(filePath).write_bytes(data)

encrypter = Encrypter()
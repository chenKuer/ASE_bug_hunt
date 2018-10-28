import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

PAD = "X"

def key_to_store(key):
    return SHA256.new(key.encode()).hexdigest()

def key_hash(key):
    return SHA256.new(key.encode()).digest()

def encrypt(text, key):
    while len(text) % 16 != 0:
        text += PAD
    cipher = AES.new(key_hash(key))
    encrypted = cipher.encrypt(text.encode())
    return base64.b64encode(encrypted).decode()

def decrypt(text, key):
    cipher = AES.new(key_hash(key))
    plain = cipher.decrypt(base64.b64decode(text))
    return plain.decode().rstrip(PAD)
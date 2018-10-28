import base64
from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256

PADDING = "="

def key_to_store(key):
    return SHA256.new(key.encode()).hexdigest()

def key_hash(key):
    return SHA256.new(key.encode()).digest()

def encrypt(text, key):
    while len(text) % 16 != 0:
        text += PADDING
    cipher = AES.new(key_hash(key), AES.MODE_ECB)
    encrypted = cipher.encrypt(text.encode())
    return base64.b64encode(encrypted).decode()

def decrypt(text, key):
    cipher = AES.new(key_hash(key), AES.MODE_ECB)
    plain = cipher.decrypt(base64.b64decode(text))
    return plain.decode().rstrip(PADDING)
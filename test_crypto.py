import base64
from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256
from crypto_utils import *

PADDING = "="


def test_key_to_store():
    input = ["hello", ""]
    flag = 1
    for i in input:
        if key_to_store(i) == SHA256.new(i.encode()).hexdigest():
            flag = flag & 1
        else:
            flag = 0

    assert flag == 1

def test_key_hash():
    input = ["hello", ""]
    flag = 1
    for i in input:
        if key_hash(i) == SHA256.new(i.encode()).digest():
            flag = flag & 1
        else:
            flag = 0

    assert flag == 1

def test_encrypt():
    input = [("hello", "key"), ("hello2", ""), ("", "key"), ("","")]
    flag = 1
    for i in input:
        text, key = i[0], i[1]
        answer = encrypt(text, key)
        while len(text) % 16 != 0:
            text += PADDING
        cipher = AES.new(key_hash(key), AES.MODE_ECB)
        encrypted = cipher.encrypt(text.encode())
        if answer == base64.b64encode(encrypted).decode():
            flag = flag & 1
        else:
            flag = 0

    assert flag == 1

def test_decrypt():
    input = [("hello", "key"), ("hello2", ""), ("", "key"), ("","")]
    flag = 1
    for i in input:
        text, key = i[0], i[1]
        answer = encrypt(text, key)
        while len(text) % 16 != 0:
            text += PADDING
        cipher = AES.new(key_hash(key), AES.MODE_ECB)
        encrypted = cipher.encrypt(text.encode())
        encrypted = base64.b64encode(encrypted).decode()
        cipher = AES.new(key_hash(key), AES.MODE_ECB)
        plain = cipher.decrypt(base64.b64decode(encrypted))
        if i[0] == plain.decode().rstrip(PADDING):
            flag = flag & 1
        else:
            flag = 0
       
    assert flag == 1    
        
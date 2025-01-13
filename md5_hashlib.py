import hashlib

def md5_builtin(message):
    return hashlib.md5(message).hexdigest()
# print(448%512)
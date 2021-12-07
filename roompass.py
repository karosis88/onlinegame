import string
import random

syms = string.ascii_letters + '123456789'

def roompass():
    return ''.join(random.choice(syms) for i in range(5))


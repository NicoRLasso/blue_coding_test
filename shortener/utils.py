import string

# Characters used for Base62 encoding
BASE62_CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase

def base62_encode(number):
    base62 = []
    while number > 0:
        number, remainder = divmod(number, 62)
        base62.append(BASE62_CHARS[remainder])
    return ''.join(base62[::-1])

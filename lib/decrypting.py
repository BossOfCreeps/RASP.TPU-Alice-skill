import base64

from six import unichr


def decrypt(data, key):
    str_ = base64.b64decode(data).decode()
    new_str = ""
    for i in range(len(str_)):
        char = ord(str_[i]) ^ ord(key[i % len(key)])

        new_str += unichr(char)
    return new_str


if __name__ == '__main__':
    print(decrypt("0bfRh9CoEdG80KvQmNGz0IzRldG00YA=", "Pwi1FhXCNk4p-S72"))

import hashlib

"""
'file' = *path to file*
"""
files = {}


def main(file: str):
    buffer_size = 65536
    with open(file, 'rb') as opened_file:
        content = opened_file.read(buffer_size)
        sha256 = hashlib.sha256()
        sha256.update(content)
    print("{0}: {1}".format(sha256.name, sha256.hexdigest()))


if __name__ == "__main__":
    main(r"C:\Users\Ream Sadan\Desktop\test\stam.txt")

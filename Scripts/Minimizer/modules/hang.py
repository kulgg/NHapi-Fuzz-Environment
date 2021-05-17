from .badinput import badinput

class hang(badinput):
    def __init__(self, filepath, content, stdout=b"", stderr=b"", unique=False):
        super.__init__(filepath, content, stdout, stderr, unique)
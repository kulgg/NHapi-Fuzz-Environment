from .badinput import badinput

class crash(badinput):
    def __init__(self, filepath, content, stdout=b"", stderr=b"", unique=False, mintrace=b""):
        super.__init__(filepath, content, stdout, stderr, unique)
        self.mintrace = mintrace
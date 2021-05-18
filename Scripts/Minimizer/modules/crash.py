from modules.badinput import badinput

class crash(badinput):
    def __init__(self, filepath, content, stdout=b"", stderr=b"", mintrace=b""):
        super(crash, self).__init__(filepath, content, stdout, stderr)
        self.mintrace = mintrace
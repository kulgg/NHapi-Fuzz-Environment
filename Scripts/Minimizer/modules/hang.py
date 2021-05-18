from modules.badinput import badinput

class hang(badinput):
    def __init__(self, filepath, content, stdout=b"", stderr=b""):
        super(hang, self).__init__(filepath, content, stdout, stderr)
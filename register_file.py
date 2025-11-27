class RegisterFile:
    def __init__(self):
        self.r = [0] * 8

    def read(self, idx):
        return self.r[idx]

    def write(self, idx, val):
        self.r[idx] = val

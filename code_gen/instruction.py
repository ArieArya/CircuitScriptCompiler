class Instruction:
    def __init__(self, type, args):
        self.type = type.upper()
        self.args = args

    def __str__(self):
        return f'{self.type} {", ".join(self.args)}'

    def __repr__(self):
        return f'{self.type} {", ".join(self.args)}'

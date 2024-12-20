class Instruction:
    def __init__(self, instruction_type, args):
        self.instruction_type = instruction_type.upper()
        self.args = args

    def __str__(self):
        return f'{self.instruction_type} {", ".join(self.args)}'

    def __repr__(self):
        return f'{self.instruction_type} {", ".join(self.args)}'

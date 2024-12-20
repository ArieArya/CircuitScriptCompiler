class Optimizer:
    def __init__(self, ir):
        self.ir = ir
        # Apply in this order for the best results.
        self.optimizations = [
            self.copy_propagation,
            self.constant_propagation,
            self.constant_folding,
            self.dead_code_elimination,
        ]

    # TODO: Implement. This currently leaves the IR untouched.
    def copy_propagation(self):
        pass

    # TODO: Implement. This currently leaves the IR untouched.
    def constant_propagation(self):
        constant_vars = dict()

        for instr in self.ir:
            match instr.type:
                case 'LOAD' | 'MOV':
                    var, arg = instr.args
                    # A new constant was found.
                    if arg in ['0', '1']:
                        constant_vars[var] = arg
                    # The value is no longer a constant.
                    else:
                        constant_vars.pop(var, None)

                case 'AND' | 'OR' | 'XOR':
                    var, arg1, arg2 = instr.args
                    new_arg1 = constant_vars.get(arg1, arg1)
                    new_arg2 = constant_vars.get(arg2, arg2)
                    instr.args = (var, new_arg1, new_arg2)

                case 'NOT':
                    var, arg = instr.args
                    new_arg = constant_vars.get(arg, arg)
                    instr.args = (var, new_arg)

                case 'PRINT':
                    (arg,) = instr.args
                    new_arg = constant_vars.get(arg, arg)
                    instr.args = (new_arg,)

    # TODO: Implement. This currently leaves the IR untouched.
    def constant_folding(self):
        pass

    # TODO: Implement. This currently leaves the IR untouched.
    def dead_code_elimination(self):
        pass

    # Continuously apply optimizations until no more changes are made.
    def optimize(self):
        old_ir = None
        while self.ir != old_ir:
            old_ir = self.ir
            [f() for f in self.optimizations]  # Apply all optimizations.
        return self.ir

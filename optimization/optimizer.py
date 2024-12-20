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

    def copy_propagation(self):
        copy_vars = dict()

        for instr in self.ir:
            match instr.type:
                case 'LOAD' | 'MOV':
                    var, arg = instr.args
                    # A new copy-able variable was found.
                    if not _is_constant(arg):
                        copy_vars[var] = arg
                    # The value is no longer copy-able.
                    else:
                        copy_vars.pop(var, None)

                case 'AND' | 'OR' | 'XOR':
                    var, arg1, arg2 = instr.args
                    new_arg1 = copy_vars.get(arg1, arg1)
                    new_arg2 = copy_vars.get(arg2, arg2)
                    instr.args = (var, new_arg1, new_arg2)

                case 'NOT':
                    var, arg = instr.args
                    new_arg = copy_vars.get(arg, arg)
                    instr.args = (var, new_arg)

                case 'PRINT':
                    (arg,) = instr.args
                    new_arg = copy_vars.get(arg, arg)
                    instr.args = (new_arg,)

    def constant_propagation(self):
        constant_vars = dict()

        for instr in self.ir:
            match instr.type:
                case 'LOAD' | 'MOV':
                    var, arg = instr.args
                    # A new constant was found.
                    if _is_constant(arg):
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
        for instr in self.ir:
            match instr.type:
                case 'AND' | 'OR' | 'XOR':
                    var, arg1, arg2 = instr.args
                    if _is_constant(arg1) and _is_constant(arg2):
                        val = _apply_binary_op(instr.type, arg1, arg2)
                        instr.args = (var, str(val))
                        instr.type = 'MOV'

                case 'NOT':
                    var, arg = instr.args
                    if _is_constant(arg):
                        val = _apply_unary_op(instr.type, arg)
                        instr.args = (var, str(val))
                        instr.type = 'MOV'

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


def _is_constant(arg):
    return arg in ['0', '1']


def _apply_unary_op(type, arg):
    match type:
        case 'NOT':
            return int(not int(arg))


def _apply_binary_op(type, arg1, arg2):
    match type:
        case 'AND':
            return int(arg1) & int(arg2)
        case 'OR':
            return int(arg1) | int(arg2)
        case 'XOR':
            return int(arg1) ^ int(arg2)

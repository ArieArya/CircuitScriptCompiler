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
        pass

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

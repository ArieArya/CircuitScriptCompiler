from enum import Enum
from collections import defaultdict


class DFA:
    State = Enum('State', ['START', 'S1', 'S2', 'S3'])

    def __init__(self):
        self.ACCEPT_STATES = set([self.State.S1, self.State.S2, self.State.S3])

        self.δ = defaultdict(dict)
        self.δ[self.State.START] = {'x': self.State.S1, '=': self.State.S2, '1': self.State.S3}

    def has_transition(self, state, c):
        return c in self.δ[state]

    def transition(self, state, c):
        return self.δ[state][c]

    def accepts(self, state):
        return state in self.ACCEPT_STATES

from enum import Enum
from collections import defaultdict


class DFA:
    State = Enum(
        'State',
        [
            'START',
            'ERROR',
            'DIGIT',
            'OPERATOR_ASSIGN',
            'OPERATOR_EQUALITY',
            'WIRE1',
            'WIRE2',
            'WIRE3',
            'WIRE4',
            'AND1',
            'AND2',
            'AND3',
            'LPAREN',
            'RPAREN',
            'SEMICOLON',
        ],
    )

    def __init__(self):
        self.ACCEPT_STATES = set(
            [
                self.State.START,
                self.State.DIGIT,
                self.State.OPERATOR_ASSIGN,
                self.State.OPERATOR_EQUALITY,
                self.State.WIRE4,
                self.State.AND3,
                self.State.LPAREN,
                self.State.RPAREN,
                self.State.SEMICOLON,
            ]
        )

        self.δ = defaultdict(dict)
        self.δ[self.State.START] = {
            '$': self.State.ERROR,
            '0': self.State.DIGIT,
            '1': self.State.DIGIT,
            '=': self.State.OPERATOR_ASSIGN,
            'w': self.State.WIRE1,
            'a': self.State.AND1,
            '(': self.State.LPAREN,
            ')': self.State.RPAREN,
            ';': self.State.SEMICOLON,
        }
        self.δ[self.State.WIRE1] = {'i': self.State.WIRE2}
        self.δ[self.State.WIRE2] = {'r': self.State.WIRE3}
        self.δ[self.State.WIRE3] = {'e': self.State.WIRE4}
        self.δ[self.State.AND1] = {'n': self.State.AND2}
        self.δ[self.State.AND2] = {'d': self.State.AND3}
        self.δ[self.State.OPERATOR_ASSIGN] = {'=': self.State.OPERATOR_EQUALITY}

    def has_transition(self, state, c):
        return c in self.δ[state]

    def transition(self, state, c):
        if c in self.δ[state]:
            return self.δ[state][c]
        else:
            return self.State.ERROR

    def accepts(self, state):
        return state in self.ACCEPT_STATES

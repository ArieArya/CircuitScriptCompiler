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
            'COMMA',
            'IDENTIFIER',
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
                self.State.COMMA,
                self.State.IDENTIFIER,
            ]
        )

        self.δ = defaultdict(dict)
        self.δ[self.State.START] = {
            '$': self.State.ERROR,
            '0': self.State.DIGIT,
            '1': self.State.DIGIT,
            '=': self.State.OPERATOR_ASSIGN,
            '(': self.State.LPAREN,
            ')': self.State.RPAREN,
            ';': self.State.SEMICOLON,
            ',': self.State.COMMA,
            'a': self.State.AND1,
            'b': self.State.IDENTIFIER,
            'c': self.State.IDENTIFIER,
            'd': self.State.IDENTIFIER,
            'e': self.State.IDENTIFIER,
            'f': self.State.IDENTIFIER,
            'g': self.State.IDENTIFIER,
            'h': self.State.IDENTIFIER,
            'i': self.State.IDENTIFIER,
            'j': self.State.IDENTIFIER,
            'k': self.State.IDENTIFIER,
            'l': self.State.IDENTIFIER,
            'm': self.State.IDENTIFIER,
            'n': self.State.IDENTIFIER,
            'o': self.State.IDENTIFIER,
            'p': self.State.IDENTIFIER,
            'q': self.State.IDENTIFIER,
            'r': self.State.IDENTIFIER,
            's': self.State.IDENTIFIER,
            't': self.State.IDENTIFIER,
            'u': self.State.IDENTIFIER,
            'v': self.State.IDENTIFIER,
            'w': self.State.WIRE1,
            'x': self.State.IDENTIFIER,
            'y': self.State.IDENTIFIER,
            'z': self.State.IDENTIFIER,
        }
        self.δ[self.State.WIRE1] = {'i': self.State.WIRE2}
        self.δ[self.State.WIRE2] = {'r': self.State.WIRE3}
        self.δ[self.State.WIRE3] = {'e': self.State.WIRE4}
        self.δ[self.State.AND1] = {'n': self.State.AND2}
        self.δ[self.State.AND2] = {'d': self.State.AND3}
        self.δ[self.State.OPERATOR_ASSIGN] = {'=': self.State.OPERATOR_EQUALITY}
        self.δ[self.State.IDENTIFIER] = {
            'a': self.State.IDENTIFIER,
            'b': self.State.IDENTIFIER,
            'c': self.State.IDENTIFIER,
            'd': self.State.IDENTIFIER,
            'e': self.State.IDENTIFIER,
            'f': self.State.IDENTIFIER,
            'g': self.State.IDENTIFIER,
            'h': self.State.IDENTIFIER,
            'i': self.State.IDENTIFIER,
            'j': self.State.IDENTIFIER,
            'k': self.State.IDENTIFIER,
            'l': self.State.IDENTIFIER,
            'm': self.State.IDENTIFIER,
            'n': self.State.IDENTIFIER,
            'o': self.State.IDENTIFIER,
            'p': self.State.IDENTIFIER,
            'q': self.State.IDENTIFIER,
            'r': self.State.IDENTIFIER,
            's': self.State.IDENTIFIER,
            't': self.State.IDENTIFIER,
            'u': self.State.IDENTIFIER,
            'v': self.State.IDENTIFIER,
            'w': self.State.IDENTIFIER,
            'x': self.State.IDENTIFIER,
            'y': self.State.IDENTIFIER,
            'z': self.State.IDENTIFIER,
            '0': self.State.IDENTIFIER,
            '1': self.State.IDENTIFIER,
            '2': self.State.IDENTIFIER,
            '3': self.State.IDENTIFIER,
            '4': self.State.IDENTIFIER,
            '5': self.State.IDENTIFIER,
            '6': self.State.IDENTIFIER,
            '7': self.State.IDENTIFIER,
            '8': self.State.IDENTIFIER,
            '9': self.State.IDENTIFIER,
        }

    def has_transition(self, state, c):
        return c in self.δ[state]

    def transition(self, state, c):
        if c in self.δ[state]:
            return self.δ[state][c]
        else:
            return self.State.ERROR

    def accepts(self, state):
        return state in self.ACCEPT_STATES

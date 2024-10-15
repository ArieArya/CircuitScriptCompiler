from enum import Enum
from collections import defaultdict
import string


class DFA:
    def __init__(self):
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
                'WHITESPACE',
            ],
        )

        self.ACCEPT_STATES = set(
            [
                State.START,
                State.DIGIT,
                State.OPERATOR_ASSIGN,
                State.OPERATOR_EQUALITY,
                State.WIRE1,
                State.WIRE2,
                State.WIRE3,
                State.WIRE4,
                State.AND1,
                State.AND2,
                State.AND3,
                State.LPAREN,
                State.RPAREN,
                State.SEMICOLON,
                State.COMMA,
                State.IDENTIFIER,
                State.WHITESPACE,
            ]
        )
        δ = defaultdict(dict)

        def add_all(state, transitions, next_state):
            for c in transitions:
                if c not in δ[state]:
                    δ[state][c] = next_state

        lowercase_and_digits = string.ascii_lowercase + string.digits

        δ[State.START] = {
            '$': State.ERROR,
            '0': State.DIGIT,
            '1': State.DIGIT,
            '=': State.OPERATOR_ASSIGN,
            '(': State.LPAREN,
            ')': State.RPAREN,
            ';': State.SEMICOLON,
            ',': State.COMMA,
            ' ': State.WHITESPACE,
            '\n': State.WHITESPACE,
        }

        add_all(State.START, string.ascii_lowercase, State.IDENTIFIER)

        δ[State.START]['w'] = State.WIRE1
        δ[State.WIRE1] = {'i': State.WIRE2}
        add_all(State.WIRE1, lowercase_and_digits, State.IDENTIFIER)
        δ[State.WIRE2] = {'r': State.WIRE3}
        add_all(State.WIRE2, lowercase_and_digits, State.IDENTIFIER)
        δ[State.WIRE3] = {'e': State.WIRE4}
        add_all(State.WIRE3, lowercase_and_digits, State.IDENTIFIER)
        add_all(State.WIRE4, lowercase_and_digits, State.IDENTIFIER)

        δ[State.START]['a'] = State.AND1
        δ[State.AND1] = {'n': State.AND2}
        add_all(State.AND1, lowercase_and_digits, State.IDENTIFIER)
        δ[State.AND2] = {'d': State.AND3}
        add_all(State.AND2, lowercase_and_digits, State.IDENTIFIER)
        add_all(State.AND3, lowercase_and_digits, State.IDENTIFIER)

        δ[State.OPERATOR_ASSIGN] = {'=': State.OPERATOR_EQUALITY}

        add_all(State.IDENTIFIER, lowercase_and_digits, State.IDENTIFIER)

        δ[State.WHITESPACE][' '] = State.WHITESPACE

        DFA.State = State  # Make State an inner class.
        self.δ = δ

    def has_transition(self, state, c):
        return c in self.δ[state]

    def transition(self, state, c):
        if c in self.δ[state]:
            return self.δ[state][c]
        else:
            return self.State.ERROR

    def accepts(self, state):
        return state in self.ACCEPT_STATES

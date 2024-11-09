from enum import Enum
from collections import defaultdict
import string

class DFA:
    def __init__(self):
        # TODO: Make this work with keywords that share the same first letter.
        # TODO: Add `nand` after we do.
        self.KEYWORDS = ['wire', 'reg', 'and', 'or', 'not', 'xor', 'print', 'if']
        KEYWORD_STATES = []
        for keyword in self.KEYWORDS:
            for i in range(len(keyword)):
                KEYWORD_STATES.append(f'{keyword.upper()}{i}')

        # We define the enum locally first so we don't need to append `self` all the time.
        State = Enum(
            'State',
            [
                'START',
                'ERROR',
                'DIGIT',
                'OPERATOR_ASSIGN',
                'OPERATOR_EQUALITY',
                'LPAREN',
                'RPAREN',
                'SEMICOLON',
                'COMMA',
                'IDENTIFIER',
                'WHITESPACE',
            ]
            + KEYWORD_STATES,
        )

        self.ACCEPT_STATES = set(
            [
                State.START,
                State.DIGIT,
                State.OPERATOR_ASSIGN,
                State.OPERATOR_EQUALITY,
                State.LPAREN,
                State.RPAREN,
                State.SEMICOLON,
                State.COMMA,
                State.IDENTIFIER,
                State.WHITESPACE,
            ]
        )
        for state in KEYWORD_STATES:
            self.ACCEPT_STATES.add(State[state])

        δ = defaultdict(dict)

        def add_all(state, transitions, next_state):
            for c in transitions:
                if c not in δ[state]:
                    δ[state][c] = next_state

        LOWERCASE_AND_DIGITS = string.ascii_lowercase + string.digits
        LOWERCASE_AND_DIGITS_AND_UNDERSCORE = LOWERCASE_AND_DIGITS + '_'

        def add_keyword_states(keyword):
            n = len(keyword)

            first_state_str = f'{keyword.upper()}{0}'
            first_state = State[first_state_str]
            δ[State.START][keyword[0]] = first_state

            for i in range(n - 1):
                c = keyword[i + 1]
                state_str = f'{keyword.upper()}{i}'
                next_state_str = f'{keyword.upper()}{i + 1}'
                state = State[state_str]
                next_state = State[next_state_str]

                δ[state][c] = next_state
                add_all(state, LOWERCASE_AND_DIGITS_AND_UNDERSCORE, State.IDENTIFIER)

            last_state_str = f'{keyword.upper()}{n - 1}'
            last_state = State[last_state_str]
            add_all(last_state, LOWERCASE_AND_DIGITS_AND_UNDERSCORE, State.IDENTIFIER)

        δ[State.START] = {
            '0': State.DIGIT,
            '1': State.DIGIT,
            '(': State.LPAREN,
            ')': State.RPAREN,
            ';': State.SEMICOLON,
            ',': State.COMMA,
        }

        # Keywords.
        for keyword in self.KEYWORDS:
            add_keyword_states(keyword)

        # Operators.
        δ[State.START]['='] = State.OPERATOR_ASSIGN
        δ[State.OPERATOR_ASSIGN]['='] = State.OPERATOR_EQUALITY

        # Identifiers.
        add_all(State.START, string.ascii_lowercase + '_', State.IDENTIFIER)
        add_all(State.IDENTIFIER, LOWERCASE_AND_DIGITS_AND_UNDERSCORE, State.IDENTIFIER)

        # Whitespace.
        δ[State.START][' '] = State.WHITESPACE
        δ[State.WHITESPACE][' '] = State.WHITESPACE
        δ[State.START]['\n'] = State.WHITESPACE

        DFA.State = State  # Make State an inner class.
        self.δ = δ

    def transition(self, state, c):
        if c in self.δ[state]:
            return self.δ[state][c]
        else:
            return self.State.ERROR

    def accepts(self, state):
        return state in self.ACCEPT_STATES

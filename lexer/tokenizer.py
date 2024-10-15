from dfa import DFA
from enum import Enum


class Tokenizer:
    def __init__(self, source_code):
        self.dfa = DFA()
        self.src = source_code
        self.idx = 0
        self.length = len(self.src)

        Tokens = Enum(
            'Tokens',
            [
                'KEYWORD',
                'IDENTIFIER',
                'OPERATOR',
                'WHITESPACE',
                'DIGIT',
                'LPAREN',
                'RPAREN',
                'COMMA',
                'SEMICOLON',
            ],
        )

        self.state_to_token = {
            DFA.State.START: Tokens.WHITESPACE,
            DFA.State.DIGIT: Tokens.DIGIT,
            DFA.State.OPERATOR_ASSIGN: Tokens.OPERATOR,
            DFA.State.OPERATOR_EQUALITY: Tokens.OPERATOR,
            DFA.State.LPAREN: Tokens.LPAREN,
            DFA.State.RPAREN: Tokens.RPAREN,
            DFA.State.SEMICOLON: Tokens.SEMICOLON,
            DFA.State.COMMA: Tokens.COMMA,
            DFA.State.IDENTIFIER: Tokens.IDENTIFIER,
            DFA.State.WHITESPACE: Tokens.WHITESPACE,
        }

        for keyword in self.dfa.KEYWORDS:
            n = len(keyword)
            for i in range(n - 1):
                state_str = f'{keyword.upper()}{i}'
                state = DFA.State[state_str]

                # Partial keywords are considered as identifiers.
                self.state_to_token[state] = Tokens.IDENTIFIER

            last_state_str = f'{keyword.upper()}{n - 1}'
            last_state = DFA.State[last_state_str]
            self.state_to_token[last_state] = Tokens.KEYWORD

        self.Tokens = Tokens

    def tokenize(self):
        tokens = []
        errors = []

        while not self.eof(self.idx):
            lexeme, state = self.recognize_lexeme()
            if state == DFA.State.WHITESPACE:
                continue
            elif self.dfa.accepts(state):
                token = self.state_to_token[state]
                tokens.append((lexeme, token))
            else:
                errors.append((lexeme, self.idx - 1))

        print('Tokens:')
        for lexeme, token in tokens:
            print(f'{token} (Value = {repr(lexeme)})')

        print()

        print('Errors:')
        for lexeme, idx in errors:
            print(f'Error parsing {repr(lexeme)} at index {idx}.')

    def recognize_lexeme(self):
        state = DFA.State.START
        start = self.idx
        end = self.idx

        last_accept_state = None
        last_accept_end = end

        while not self.eof(end) and state != DFA.State.ERROR:
            state = self.dfa.transition(state, self.src[end])
            if self.dfa.accepts(state):
                last_accept_state = state
                last_accept_end = end
            end += 1

        next_idx = end if last_accept_state is None else last_accept_end + 1
        self.idx = next_idx  # Advance pointer.

        lexeme = self.src[start:next_idx]
        return lexeme, last_accept_state

    def eof(self, idx):
        return idx == self.length


tokenizer = Tokenizer('wire w1 = -1 = == ?&;')
tokenizer.tokenize()

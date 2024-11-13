from lexer.dfa import DFA
from lexer.enums import TokenClass


class Token:
    def __init__(self, token_class, lexeme):
        self.token_class = token_class
        self.lexeme = lexeme

    def __str__(self):
        return f'{self.token_class.name}("{self.lexeme}")'


class Tokenizer:
    def __init__(self, source_code):
        self.dfa = DFA()
        self.src = source_code
        self.idx = 0
        self.length = len(self.src)

        self.state_to_token_class = {
            DFA.State.START: TokenClass.WHITESPACE,
            DFA.State.DIGIT: TokenClass.DIGIT,
            DFA.State.OPERATOR_ASSIGN: TokenClass.OPERATOR,
            DFA.State.OPERATOR_EQUALITY: TokenClass.OPERATOR,
            DFA.State.LPAREN: TokenClass.LPAREN,
            DFA.State.RPAREN: TokenClass.RPAREN,
            DFA.State.SEMICOLON: TokenClass.SEMICOLON,
            DFA.State.COMMA: TokenClass.COMMA,
            DFA.State.IDENTIFIER: TokenClass.IDENTIFIER,
            DFA.State.WHITESPACE: TokenClass.WHITESPACE,
        }

        for keyword in self.dfa.KEYWORDS:
            n = len(keyword)
            for i in range(n - 1):
                state_str = f'{keyword.upper()}{i}'
                state = DFA.State[state_str]

                # Partial keywords are considered as identifiers.
                self.state_to_token_class[state] = TokenClass.IDENTIFIER

            last_state_str = f'{keyword.upper()}{n - 1}'
            last_state = DFA.State[last_state_str]
            self.state_to_token_class[last_state] = TokenClass.KEYWORD

    def tokenize(self):
        tokens = []
        errors = []

        while not self.eof(self.idx):
            lexeme, state = self.recognize_lexeme()
            if state == DFA.State.WHITESPACE:
                continue
            elif self.dfa.accepts(state):
                token_class = self.state_to_token_class[state]
                tokens.append(Token(token_class, lexeme))
            else:
                errors.append((lexeme, self.idx - 1))

        return tokens, errors

    def recognize_lexeme(self):
        state = DFA.State.START
        start = self.idx
        end = self.idx

        # Record last accepted state (if any) in case further searching isn't accepted.
        # This also implements maximal munch as a byproduct.
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

    def tokens_to_str(tokens):
        result = ''
        for token in tokens:
            result += f'{token}\n'
        return result

    def errors_to_str(errors):
        result = ''
        for lexeme, idx in errors:
            result += f'Error parsing {repr(lexeme)} at index {idx}.\n'
        return result

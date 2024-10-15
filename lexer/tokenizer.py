from dfa import DFA
import re


class Tokenizer:
    def __init__(self, source_code):
        source_code = re.sub(r'\s+', '', source_code)  # Remove all whitespace.

        self.dfa = DFA()
        self.src = source_code
        self.idx = 0
        self.length = len(self.src)

    def tokenize(self):
        while not self.eof(self.idx):
            lexeme, accepts = self.recognize_lexeme()
            if not accepts:
                print(f'Error parsing {repr(lexeme)}.')
                exit()
            else:
                print(lexeme)

    def recognize_lexeme(self):
        if self.eof(self.idx):
            return 'EOF', False

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
        return lexeme, self.dfa.accepts(last_accept_state)

    def eof(self, idx):
        return idx == self.length


tokenizer = Tokenizer('and == 1 === (wire)')
tokenizer.tokenize()

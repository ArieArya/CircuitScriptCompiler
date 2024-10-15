from dfa import DFA
import re


class Tokenizer:
    def __init__(self, source_code):
        source_code = re.sub(r'\s+', '', source_code)  # Remove all whitespace.

        self.EOF = '$'  # Sentinel node.
        self.dfa = DFA()
        self.src = source_code + self.EOF
        self.idx = 0

    def tokenize(self):
        while lexeme := self.recognize_lexeme():
            print(lexeme)

    def recognize_lexeme(self):
        state = DFA.State.START
        start = self.idx
        end = self.idx

        c = self.src[end]
        while c != self.EOF and self.dfa.has_transition(state, c):
            state = self.dfa.transition(state, c)
            end += 1
            c = self.src[end]

        self.idx = end  # Advance pointer.c

        value = self.src[start:end]
        return value if self.dfa.accepts(state) else None


tokenizer = Tokenizer('x = 1')
tokenizer.tokenize()

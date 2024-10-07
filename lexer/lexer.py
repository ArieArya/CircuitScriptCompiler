import re

# Constants
KEYWORDS = { 'wire', 'reg', 'lut', 'and', 'or', 'not', 'xor', 'nand', 'print', 'if'}
CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
CHAR_DIGITS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789"
DIGITS = "0123456789"
PUNCTUATIONS = "(){},;"
OPERATORS = "="

# States
START_STATE = "START"
IDENTIFIER_KEYWORD_STATE = "IDENTIFIER_KEYWORD"  # Combined since keyword can be a subset of identifier
FIRST_EQUAL_STATE = "FIRST_EQUAL"
SECOND_EQUAL_STATE = "SECOND_EQUAL"  # need an extra state for ==
INTLITERAL_STATE = "INTLITERAL"
FIRST_PUNCTUATION_STATE = "FIRST_PUNCTUATION"  # required to allow e.g. );
SECOND_PUNCTUATION_STATE = "SECOND_PUNCTUATION"
END_STATE = "END"

class State:
	def __init__(self, name):
		self.name = name
		self.transitions = {}

		# space / newline always goes back to start state
		self.add_transition(" ", START_STATE)
		self.add_transition("\n", START_STATE)
		# a None character indicates end of source code
		self.add_transition(None, END_STATE)

	def add_transition(self, input_char, next_state):
		self.transitions[input_char] = next_state

	def get_next_state(self, input_char):
		return self.transitions.get(input_char, None)  # if None, invalid transition

class StartState(State):
	def __init__(self):
		super().__init__(START_STATE)

		# initialize transitions 
		for letter in CHARS:
			self.add_transition(letter, IDENTIFIER_KEYWORD_STATE)
		for digit in DIGITS:
			self.add_transition(digit, INTLITERAL_STATE)
		for punct in PUNCTUATIONS:
			self.add_transition(punct, FIRST_PUNCTUATION_STATE)
		self.add_transition("=", FIRST_EQUAL_STATE)

class IdentifierAndKeywordState(State):
	def __init__(self):
		super().__init__(IDENTIFIER_KEYWORD_STATE) 

		# initialize transitions (can continue with letters, digits, underscores)
		for char in CHAR_DIGITS:
			self.add_transition(char, IDENTIFIER_KEYWORD_STATE)
		for punct in PUNCTUATIONS:
			self.add_transition(punct, FIRST_PUNCTUATION_STATE)

class IntLiteralState(State):
	def __init__(self):
		super().__init__(INTLITERAL_STATE)

		# initialize transitions (can continue with additional digits)
		for digit in DIGITS:
			self.add_transition(digit, INTLITERAL_STATE)
		for punct in PUNCTUATIONS:
			self.add_transition(punct, FIRST_PUNCTUATION_STATE)

class FirstEqualState(State):
	def __init__(self):
		super().__init__(FIRST_EQUAL_STATE)

		# intiialize transitions
		self.add_transition("=", SECOND_EQUAL_STATE)
		
class SecondEqualState(State):
	def __init__(self):
		super().__init__(SECOND_EQUAL_STATE)
		# No other transitions. Must go back to start state

class FirstPunctuationState(State):
	def __init__(self):
		super().__init__(FIRST_PUNCTUATION_STATE)
		
		# initialize transitions 
		for letter in CHARS:
			self.add_transition(letter, IDENTIFIER_KEYWORD_STATE)
		for digit in DIGITS:
			self.add_transition(digit, INTLITERAL_STATE)
		for punct in PUNCTUATIONS:
			self.add_transition(punct, SECOND_PUNCTUATION_STATE)

class SecondPunctuationState(State):
	def __init__(self):
		super().__init__(SECOND_PUNCTUATION_STATE)
		
		# initialize transitions 
		for letter in CHARS:
			self.add_transition(letter, IDENTIFIER_KEYWORD_STATE)
		for digit in DIGITS:
			self.add_transition(digit, INTLITERAL_STATE)

# Used for final (None) character
class EndState(State):
	def __init__(self):
		super().__init__(END_STATE)

class Token:
	def __init__(self, type, value):
		self.type = type
		self.value = value
	
	def __repr__(self):
		return f"Token({self.type}, {repr(self.value)})"

class Lexer:
	def __init__(self, source_code):
		self.source_code = source_code
		self.position = 0
		self.tokens = []
		self.cur_string = ""
		# initialize states
		self.states = {
			START_STATE: StartState(),
			IDENTIFIER_KEYWORD_STATE: IdentifierAndKeywordState(),
			INTLITERAL_STATE: IntLiteralState(),
			FIRST_EQUAL_STATE: FirstEqualState(),
			SECOND_EQUAL_STATE: SecondEqualState(),
			FIRST_PUNCTUATION_STATE: FirstPunctuationState(),
			SECOND_PUNCTUATION_STATE: SecondPunctuationState(),
			END_STATE: EndState(),
		}
		self.cur_state = self.states[START_STATE]

	def advance(self):
		next_char = self.current_char()
		next_state_name = self.cur_state.get_next_state(next_char)
		if next_state_name == None:
			raise Exception("Invalid next state detected. Crashing...")
		next_state = self.states[next_state_name] 

		# No state transition
		if next_state == self.cur_state:
			self.cur_string += next_char
		# State transitions
		else:  
			# For keywords / identifiers
			if self.cur_state.name == IDENTIFIER_KEYWORD_STATE:
				if self.cur_string in KEYWORDS:
					self.tokens.append(Token('KEYWORD', self.cur_string))
				else:
					self.tokens.append(Token('IDENTIFIER', self.cur_string))
			elif self.cur_state.name == INTLITERAL_STATE:
				self.tokens.append(Token('INTLITERAL', self.cur_string))
			elif self.cur_state.name == FIRST_PUNCTUATION_STATE or self.cur_state.name == SECOND_PUNCTUATION_STATE:
				self.tokens.append(Token('PUNCTUATION', self.cur_string))
			elif self.cur_state.name == FIRST_EQUAL_STATE or self.cur_state.name == SECOND_EQUAL_STATE:
				self.tokens.append(Token('OPERATOR', self.cur_string))
			# Move to the next character
			self.cur_string = self.current_char()
			self.cur_state = next_state

		# Increment position
		self.position += 1

	def current_char(self):
		# Return the current character or None if at the end
		if self.position >= len(self.source_code):
			return None
		return self.source_code[self.position]

	def tokenize(self):
		while self.current_char() != None:
			self.advance()
		self.advance()  # must do one final advance to tokenize final element
		return self.tokens
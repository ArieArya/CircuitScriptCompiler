from enum import Enum
from collections import defaultdict
import string

class DFA:
    def __init__(self):
		# List of keywords in the language being compiled
        self.KEYWORDS = ['wire', 'reg', 'and', 'or', 'not', 'xor', 'print']

		# Create unique state names for each character in each keyword
        KEYWORD_STATES = []
        for keyword in self.KEYWORDS:
            for i in range(len(keyword)):
                KEYWORD_STATES.append(f'{keyword.upper()}{i}')

        # Define the DFA states using an Enum
        # Includes basic states and dynamically generated keyword states
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

		# Set of states that are valid accepting states
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

		# Add all keyword states to the accepting states
        for state in KEYWORD_STATES:
            self.ACCEPT_STATES.add(State[state])

		# Transition function (δ) represented as a nested dictionary
        δ = defaultdict(dict)

		# Helper function to add multiple transitions for a given state
        def add_all(state, transitions, next_state):
            for c in transitions:
                if c not in δ[state]:
                    δ[state][c] = next_state

		# Define character sets for transitions
        LOWERCASE_AND_DIGITS = string.ascii_lowercase + string.digits
        LOWERCASE_AND_DIGITS_AND_UNDERSCORE = LOWERCASE_AND_DIGITS + '_'

		# Function to add states and transitions for each keyword
        def add_keyword_states(keyword):
            n = len(keyword)

			# Initial transition for the first character of the keyword
            first_state_str = f'{keyword.upper()}{0}'
            first_state = State[first_state_str]
            δ[State.START][keyword[0]] = first_state

			# Create transitions for each subsequent character in the keyword
            for i in range(n - 1):
                c = keyword[i + 1]
                state_str = f'{keyword.upper()}{i}'
                next_state_str = f'{keyword.upper()}{i + 1}'
                state = State[state_str]
                next_state = State[next_state_str]

                δ[state][c] = next_state
                add_all(state, LOWERCASE_AND_DIGITS_AND_UNDERSCORE, State.IDENTIFIER)

			# Allow identifiers to follow the final character of the keyword
            last_state_str = f'{keyword.upper()}{n - 1}'
            last_state = State[last_state_str]
            add_all(last_state, LOWERCASE_AND_DIGITS_AND_UNDERSCORE, State.IDENTIFIER)

		# Initial transitions from the START state for digits and punctuation
        δ[State.START] = {
            '0': State.DIGIT,
            '1': State.DIGIT,
            '(': State.LPAREN,
            ')': State.RPAREN,
            ';': State.SEMICOLON,
            ',': State.COMMA,
        }

        # Add transitions for each keyword
        for keyword in self.KEYWORDS:
            add_keyword_states(keyword)

        # Define transitions for operators (= and ==)
        δ[State.START]['='] = State.OPERATOR_ASSIGN
        δ[State.OPERATOR_ASSIGN]['='] = State.OPERATOR_EQUALITY

        # Define transitions for identifiers (letters and underscores)
        add_all(State.START, string.ascii_lowercase + '_', State.IDENTIFIER)
        add_all(State.IDENTIFIER, LOWERCASE_AND_DIGITS_AND_UNDERSCORE, State.IDENTIFIER)

        # Define transitions for whitespace characters (space and newline)
        δ[State.START][' '] = State.WHITESPACE
        δ[State.WHITESPACE][' '] = State.WHITESPACE
        δ[State.START]['\n'] = State.WHITESPACE

		# Expose State as an inner class and store the transition function
        DFA.State = State  # Make State an inner class.
        self.δ = δ

	# Function to perform a state transition based on the current state and input character
    def transition(self, state, c):
        if c in self.δ[state]:
            return self.δ[state][c]
        else:
            return self.State.ERROR

	# Function to check if a state is an accepting state
    def accepts(self, state):
        return state in self.ACCEPT_STATES

from lexer.tokenizer import Token
from lexer.enums import TokenClass
from parser.enums import NonTerminals
from parser.tree_node import TreeNode
from parser.ll1_parse_table import LL1_PARSE_TABLE

# Token classes where we don't need to check actual lexemes.
standalone_token_classes = set([TokenClass.IDENTIFIER, TokenClass.DIGIT])


class LL1Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    # Recursively performs parsing based on the given non-terminal.
    def parse(self, non_terminal=NonTerminals.Program, start=True):
        root_node = TreeNode(non_terminal.name)
        current_token = self.peek()

        # Obtain the next production rule from the LL(1) parse table
        if current_token.token_class in standalone_token_classes:
            key = (non_terminal, current_token.token_class)
        else:
            key = (non_terminal, str(current_token))
        if key not in LL1_PARSE_TABLE:
            raise Exception('Production rule not found in LL(1) parse table.')
        next_productions = LL1_PARSE_TABLE[key]

        # Iterate over the productions for the current non-terminal
        for production in next_productions:
            if production == 'ε':
                continue  # ignore ε
            elif str(production) == str(current_token) or (
                isinstance(production, TokenClass)
                and production == current_token.token_class
                and production in standalone_token_classes
            ):
				# If the production matches the current token, add it as a child node
                root_node.add_child(TreeNode(current_token))
                self.advance()
                current_token = self.peek()
            elif isinstance(production, NonTerminals):
				# If the production is a non-terminal, recursively parse it
                root_node.add_child(self.parse(production, False))
                current_token = self.peek()
            else:
				# Raise an error if the token does not match any valid production
                raise Exception(f'Invalid token at index {self.position} ({current_token}).')

		# If parsing is complete but not all tokens have been processed, raise an error
        if start and self.position < len(self.tokens):
            raise Exception('Failed to traverse whole token array')
        return root_node

	# Returns the current token without advancing the position
    def peek(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        else:
            return Token(TokenClass.KEYWORD, '$')

	# Advances the current position to the next token
    def advance(self):
        self.position += 1

	# Static method to convert a parse tree to a string representation
    @staticmethod
    def parse_tree_to_str(parse_tree):
        result = ''
        stack = [(parse_tree, 0)]
        while stack:
            cur_node, depth = stack.pop()
            result += '  ' * depth + '|-> ' + str(cur_node) + '\n'

            for child_node in cur_node.children[::-1]:  # Reverse so we traverse DFS correctly.
                stack.append((child_node, depth + 1))
        return result

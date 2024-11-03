from tokenizer import Token
from enums import TokenClass, NonTerminals
from ast import ASTNode
from ll1_parse_table import LL1_PARSE_TABLE

# Token Classes where we don't need to check actual lexemes
standalone_token_classes = set([TokenClass.IDENTIFIER, TokenClass.DIGIT])

class LL1Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.position = 0
		self.stack = []  # to perform DFS
		self.parse_tree = None  # Root of parse tree

	# Recursively performs parsing
	def parse(self, non_terminal=NonTerminals.Program, start=True):
		root_node = ASTNode(non_terminal.name)
		current_token = self.peek()
		if start:
			self.parse_tree = root_node

		# obtain next production from parse table
		if current_token.token_class in standalone_token_classes:
			key = (non_terminal, current_token.token_class)
		else:
			key = (non_terminal, str(current_token))
		if key not in LL1_PARSE_TABLE:
			raise Exception("Invalid parse tree")
		next_productions = LL1_PARSE_TABLE[key]

		# iterate over productions
		for production in next_productions:
			if production == "ε":
				continue  # ignore ε
			elif str(production) == str(current_token) or (type(production) == TokenClass and production == current_token.token_class and production in standalone_token_classes):
				root_node.add_child(ASTNode(str(current_token)))
				self.advance()  # move to next token
				current_token = self.peek()
			elif type(production) == NonTerminals:
				# perform DFS and recursively build parse tree
				root_node.add_child(self.parse(production, False))
				current_token = self.peek()
			else:
				raise Exception("Invalid parse tree")

		if start and self.position < len(self.tokens):
			raise Exception("Failed to traverse whole token array")
		return root_node

	def peek(self):
		return self.tokens[self.position] if self.position < len(self.tokens) else Token(TokenClass.KEYWORD, '$')  # end of token stream

	def advance(self):
		self.position += 1

	def printParseTree(self):
		# Perform DFS to print AST
		stack = [(self.parse_tree, 0)]
		while stack:
			cur_node, depth = stack.pop()
			print(" " * depth + "|-> " + str(cur_node))  # print with indentation

			# iterate over next nodes
			for child_node in cur_node.children[::-1]:  # reverse so we traverse DFS correctly
				stack.append((child_node, depth+1))





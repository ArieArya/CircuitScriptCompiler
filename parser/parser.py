from lexer.tokenizer import Token
from lexer.enums import TokenClass
from parser.enums import NonTerminals
from parser.tree_node import TreeNode
from parser.ll1_parse_table import LL1_PARSE_TABLE

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
		root_node = TreeNode(non_terminal.name)
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
				root_node.add_child(TreeNode(current_token))
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
		# Perform DFS to print parse tree
		stack = [(self.parse_tree, 0)]
		while stack:
			cur_node, depth = stack.pop()
			print(" " * depth + "|-> " + str(cur_node))  # print with indentation

			# iterate over next nodes
			for child_node in cur_node.children[::-1]:  # reverse so we traverse DFS correctly
				stack.append((child_node, depth+1))


# Token Classes where we can ignore when building AST
ignore_token_classes = set([TokenClass.SEMICOLON, TokenClass.LPAREN, TokenClass.RPAREN, TokenClass.COMMA])

class ASTGenerator:
	def __init__(self, parse_tree):
		self.parse_tree = parse_tree
		self.ast = None

	def buildAst(self, parse_tree_node):
		# Terminal Node - return itself
		if type(parse_tree_node.label) == Token and parse_tree_node.label.token_class not in ignore_token_classes:
			return parse_tree_node

		# Program Node - main program node
		elif parse_tree_node.label == NonTerminals.Program.name:
			self.ast = TreeNode(NonTerminals.Program.name, self.buildAst(parse_tree_node.children[0]))  # only has 1 child
			return self.ast

		# StatementList Node - returns list of statements
		elif parse_tree_node.label == NonTerminals.StatementList.name:
			statements = []
			for node in parse_tree_node.children:
				if node.label == NonTerminals.Statement.name:
					statements.append(self.buildAst(node))
				elif node.label == NonTerminals.StatementList.name:
					statements.extend(self.buildAst(node))
			return statements

		# Statement Node
		elif parse_tree_node.label == NonTerminals.Statement.name:
			return self.buildAst(parse_tree_node.children[0])  # statement node only has a single child

		# Declaration Node
		elif parse_tree_node.label == NonTerminals.Declaration.name:
			children = []
			for node in parse_tree_node.children:
				next_node = self.buildAst(node)
				if next_node:
					children.append(next_node)
			return TreeNode(NonTerminals.Declaration.name, children)

		# Assignment Node
		elif parse_tree_node.label == NonTerminals.Assignment.name:
			children = []
			for node in parse_tree_node.children:
				if type(node.label) == NonTerminals:
					children.append(self.buildAst(node))
				else:
					next_node = self.buildAst(node)
					if next_node:
						children.append(next_node)
			return TreeNode(NonTerminals.Assignment.name, children)

		# Expression
		elif parse_tree_node.label == NonTerminals.Expression.name:
			return self.buildAst(parse_tree_node.children[0])  # expression has a single child

		# Gate Expression
		elif parse_tree_node.label == NonTerminals.GateExpression.name:
			children = []
			for node in parse_tree_node.children:
				if node.label == NonTerminals.Arguments.name:
					children.extend(self.buildAst(node))  # extend list of arguments
				else:
					next_node = self.buildAst(node)  # works for both GateType and Terminals
					if next_node:
						children.append(next_node)
			return TreeNode(NonTerminals.GateExpression.name, children)

		# GateType
		elif parse_tree_node.label == NonTerminals.GateType.name:
			return parse_tree_node.children[0]

		# Arguments
		elif parse_tree_node.label == NonTerminals.Arguments.name:
			argument_list = []
			for node in parse_tree_node.children:
				if node.label == NonTerminals.Expression.name:
					argument_list.append(self.buildAst(node))
				elif node.label == NonTerminals.Arguments_.name:
					argument_list.extend(self.buildAst(node))  # for Arguments'
			return argument_list

		# Arguments'
		elif parse_tree_node.label == NonTerminals.Arguments_.name:
			argument_list = []
			for node in parse_tree_node.children:
				if node.label == NonTerminals.Arguments.name:
					argument_list.extend(self.buildAst(node))
			return argument_list

	def printAst(self):
		# Perform DFS to printAST
		stack = [(self.ast, 0)]
		while stack:
			cur_node, depth = stack.pop()
			print(" " * depth + "|-> " + str(cur_node))  # print with indentation

			# iterate over next nodes
			for child_node in cur_node.children[::-1]:  # reverse so we traverse DFS correctly
				stack.append((child_node, depth+1))
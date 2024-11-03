from enum import Enum

# Tokenizer Enum
TokenClass = Enum(
	'TokenClass',
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

# Parser Enum
NonTerminals = Enum(
	'NonTerminals',
	[
		'Program',
		'StatementList',
		'Statement',
		'Declaration',
		'Assignment',
		'PrintStmt',
		'IfStmt',
		'Expression',
		'GateExpression',
		'GateType',
		'Arguments',
		'Arguments_'
	]
)
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
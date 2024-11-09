from enum import Enum

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
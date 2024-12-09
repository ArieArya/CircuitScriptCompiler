from enum import Enum

# Enum representing different classes of non-terminals in the language
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
        'Arguments_',
    ],
)

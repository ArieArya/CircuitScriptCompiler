from lexer.tokenizer import Token
from lexer.enums import TokenClass
from parser.enums import NonTerminals

LL1_PARSE_TABLE = {
	# Program
    (NonTerminals.Program, str(Token(TokenClass.KEYWORD, "wire"))): [NonTerminals.StatementList],
    (NonTerminals.Program, str(Token(TokenClass.KEYWORD, "reg"))): [NonTerminals.StatementList],
    (NonTerminals.Program, str(Token(TokenClass.KEYWORD, "lut"))): [NonTerminals.StatementList],
    (NonTerminals.Program, TokenClass.IDENTIFIER): [NonTerminals.StatementList],
    (NonTerminals.Program, str(Token(TokenClass.KEYWORD, "print"))): [NonTerminals.StatementList],
    (NonTerminals.Program, str(Token(TokenClass.KEYWORD, "if"))): [NonTerminals.StatementList],

	# StatementList
    (NonTerminals.StatementList, str(Token(TokenClass.KEYWORD, "wire"))): [NonTerminals.Statement, Token(TokenClass.SEMICOLON, ";"), NonTerminals.StatementList],
    (NonTerminals.StatementList, str(Token(TokenClass.KEYWORD, "reg"))): [NonTerminals.Statement, Token(TokenClass.SEMICOLON, ";"), NonTerminals.StatementList],
    (NonTerminals.StatementList, str(Token(TokenClass.KEYWORD, "lut"))): [NonTerminals.Statement, Token(TokenClass.SEMICOLON, ";"), NonTerminals.StatementList],
    (NonTerminals.StatementList, TokenClass.IDENTIFIER): [NonTerminals.Statement, Token(TokenClass.SEMICOLON, ";"), NonTerminals.StatementList],
    (NonTerminals.StatementList, str(Token(TokenClass.KEYWORD, "print"))): [NonTerminals.Statement, Token(TokenClass.SEMICOLON, ";"), NonTerminals.StatementList],
    (NonTerminals.StatementList, str(Token(TokenClass.KEYWORD, "if"))): [NonTerminals.Statement, Token(TokenClass.SEMICOLON, ";"), NonTerminals.StatementList],
    (NonTerminals.StatementList, str(Token(TokenClass.KEYWORD, "$"))): ['ε'],

	# Statement
    (NonTerminals.Statement, str(Token(TokenClass.KEYWORD, "wire"))): [NonTerminals.Declaration],
    (NonTerminals.Statement, str(Token(TokenClass.KEYWORD, "reg"))): [NonTerminals.Declaration],
    (NonTerminals.Statement, str(Token(TokenClass.KEYWORD, "lut"))): [NonTerminals.Declaration],
    (NonTerminals.Statement, TokenClass.IDENTIFIER): [NonTerminals.Assignment],
    (NonTerminals.Statement, str(Token(TokenClass.KEYWORD, "print"))): [NonTerminals.PrintStmt],
    (NonTerminals.Statement, str(Token(TokenClass.KEYWORD, "if"))): [NonTerminals.IfStmt],

	# Declaration
    (NonTerminals.Declaration, str(Token(TokenClass.KEYWORD, "wire"))): [Token(TokenClass.KEYWORD, "wire"), TokenClass.IDENTIFIER],
    (NonTerminals.Declaration, str(Token(TokenClass.KEYWORD, "reg"))): [Token(TokenClass.KEYWORD, "reg"), TokenClass.IDENTIFIER, Token(TokenClass.OPERATOR, "="), TokenClass.DIGIT],
    (NonTerminals.Declaration, str(Token(TokenClass.KEYWORD, "lut"))): [Token(TokenClass.KEYWORD, "lut"), Token(TokenClass.LPAREN, "("), NonTerminals.Arguments, Token(TokenClass.RPAREN, ")"), NonTerminals.StatementList],

	# Assignment
    (NonTerminals.Assignment, TokenClass.IDENTIFIER): [TokenClass.IDENTIFIER, Token(TokenClass.OPERATOR, "="), NonTerminals.Expression],

	# PrintStmt
    (NonTerminals.PrintStmt, str(Token(TokenClass.KEYWORD, "print"))): [Token(TokenClass.KEYWORD, "print"), Token(TokenClass.LPAREN, "("), TokenClass.IDENTIFIER, Token(TokenClass.RPAREN, ")")],

	# IfStmt
    (NonTerminals.IfStmt, str(Token(TokenClass.KEYWORD, "if"))): [Token(TokenClass.KEYWORD, "if"), Token(TokenClass.LPAREN, "("), NonTerminals.Expression, Token(TokenClass.OPERATOR, "=="), NonTerminals.Expression, Token(TokenClass.RPAREN, ")"), NonTerminals.Statement],

	# Expression
    (NonTerminals.Expression, str(Token(TokenClass.KEYWORD, "and"))): [NonTerminals.GateExpression],
    (NonTerminals.Expression, str(Token(TokenClass.KEYWORD, "or"))): [NonTerminals.GateExpression],
    (NonTerminals.Expression, str(Token(TokenClass.KEYWORD, "not"))): [NonTerminals.GateExpression],
    (NonTerminals.Expression, str(Token(TokenClass.KEYWORD, "xor"))): [NonTerminals.GateExpression],
    (NonTerminals.Expression, str(Token(TokenClass.KEYWORD, "nand"))): [NonTerminals.GateExpression],
    (NonTerminals.Expression, TokenClass.IDENTIFIER): [TokenClass.IDENTIFIER],
    (NonTerminals.Expression, TokenClass.DIGIT): [TokenClass.DIGIT],

	# GateExpression
    (NonTerminals.GateExpression, str(Token(TokenClass.KEYWORD, "and"))): [NonTerminals.GateType, Token(TokenClass.LPAREN, "("), NonTerminals.Arguments, str(Token(TokenClass.RPAREN, ")"))],
    (NonTerminals.GateExpression, str(Token(TokenClass.KEYWORD, "or"))): [NonTerminals.GateType, Token(TokenClass.LPAREN, "("), NonTerminals.Arguments, str(Token(TokenClass.RPAREN, ")"))],
    (NonTerminals.GateExpression, str(Token(TokenClass.KEYWORD, "not"))): [NonTerminals.GateType, Token(TokenClass.LPAREN, "("), NonTerminals.Arguments, str(Token(TokenClass.RPAREN, ")"))],
    (NonTerminals.GateExpression, str(Token(TokenClass.KEYWORD, "xor"))): [NonTerminals.GateType, Token(TokenClass.LPAREN, "("), NonTerminals.Arguments, str(Token(TokenClass.RPAREN, ")"))],
    (NonTerminals.GateExpression, str(Token(TokenClass.KEYWORD, "nand"))): [NonTerminals.GateType, Token(TokenClass.LPAREN, "("), NonTerminals.Arguments, str(Token(TokenClass.RPAREN, ")"))],

	# GateType
    (NonTerminals.GateType, str(Token(TokenClass.KEYWORD, "and"))): [Token(TokenClass.KEYWORD, "and")],
    (NonTerminals.GateType, str(Token(TokenClass.KEYWORD, "or"))): [Token(TokenClass.KEYWORD, "or")],
    (NonTerminals.GateType, str(Token(TokenClass.KEYWORD, "not"))): [Token(TokenClass.KEYWORD, "not")],
    (NonTerminals.GateType, str(Token(TokenClass.KEYWORD, "xor"))): [Token(TokenClass.KEYWORD, "xor")],
    (NonTerminals.GateType, str(Token(TokenClass.KEYWORD, "nand"))): [Token(TokenClass.KEYWORD, "nand")],

	# Arguments
    (NonTerminals.Arguments, TokenClass.IDENTIFIER): [NonTerminals.Expression, NonTerminals.Arguments_],
    (NonTerminals.Arguments, TokenClass.DIGIT): [NonTerminals.Expression, NonTerminals.Arguments_],

	# Arguments_
    (NonTerminals.Arguments_, str(Token(TokenClass.COMMA, ","))): [Token(TokenClass.COMMA, ","), NonTerminals.Arguments],
    (NonTerminals.Arguments_, str(Token(TokenClass.RPAREN, ")"))): ['ε']
}
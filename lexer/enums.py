from enum import Enum

# Enum representing different classes of tokens in the language
TokenClass = Enum(
    'TokenClass',
    [
        'KEYWORD',     # Reserved words in the language (e.g., 'wire', 'reg')
        'IDENTIFIER',  # User-defined names (e.g., variable names)
        'OPERATOR',    # Operators (e.g., '=', '==')
        'WHITESPACE',  # Whitespace characters (e.g., spaces, newlines)
        'DIGIT',       # Numerical digits (e.g., '0', '1')
        'LPAREN',      # Left parenthesis '('
        'RPAREN',      # Right parenthesis ')'
        'COMMA',       # Comma ','
        'SEMICOLON',   # Semicolon ';'
    ],
)
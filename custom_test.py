from lexer import Tokenizer
from parser import LL1Parser, ASTGenerator

source_code = 'reg r1 = and(or(0, 1), 1);'

tokenizer = Tokenizer(source_code)
tokens, errors = tokenizer.tokenize()

parser = LL1Parser(tokens)
parse_tree = parser.parse()

ast_gen = ASTGenerator(parse_tree)
ast_gen.build_ast(ast_gen.parse_tree)

filename = 'chained_gates'
with open(f'sample_code/tester_output/{filename}.txt', 'w') as f:
    f.write(str(ast_gen))

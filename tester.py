import os
from lexer import Tokenizer
from parser import LL1Parser, ASTGenerator


def read_source_code_from_file(file_path):
    # Reads the source code from a text file.
    with open(file_path, 'r') as file:
        return file.read()


if __name__ == '__main__':
    source_code_dir = 'sample_code'

    for filename in sorted(os.listdir(source_code_dir)):
        file_path = os.path.join(source_code_dir, filename)

        if not os.path.isfile(file_path):
            continue

        # Lexical Analysis
        source_code = read_source_code_from_file(f'sample_code/{filename}')
        tokenizer = Tokenizer(source_code)
        tokens, errors = tokenizer.tokenize()

        # Syntactic Analysis - build parse tree
        parser = LL1Parser(tokens)
        parse_tree = parser.parse()

        # Syntactic Analysis - build AST
        ast_gen = ASTGenerator(parse_tree)
        ast_gen.build_ast(ast_gen.parse_tree)

        with open(f'sample_code/tester_output/{filename}.txt', 'w') as f:
            f.write(str(ast_gen))

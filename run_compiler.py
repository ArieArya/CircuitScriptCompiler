import os
from lexer import Tokenizer
from parser import LL1Parser, ASTGenerator
from code_gen import CodeGenerator


def read(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def write(file_path, s):
    with open(file_path, 'w') as file:
        return file.write(s)


def main():
    """
    Runs the lexer, parser, and AST generator on each .circuit file in the 'sample_code' directory.

    Per-phase outputs are generated inside of the 'sample_code/tester_output' directory.

    If any phase fails, the error will be outputted and subsequent phases will not run.
    """

    src_dir = 'sample_code'

    for filename in sorted(os.listdir(src_dir)):
        file_path = os.path.join(src_dir, filename)
        filename_no_ext, ext = os.path.splitext(filename)

        if not os.path.isfile(file_path) or ext != '.circuit':
            continue

        test_output_dir = os.path.join(src_dir, 'tester_output', filename_no_ext)
        os.makedirs(test_output_dir, exist_ok=True)
        lexer_path = os.path.join(test_output_dir, '1_lexer.txt')
        parser_path = os.path.join(test_output_dir, '2_parser.txt')
        ast_path = os.path.join(test_output_dir, '3_ast.txt')
        codegen_path = os.path.join(test_output_dir, '4_codegen.txt')
        optimized_path = os.path.join(test_output_dir, '5_optimized.txt')

        if filename != 'wires_and_registers.circuit':
            continue

        # 1. Lexical Analysis
        source_code = read(f'sample_code/{filename}')
        tokenizer = Tokenizer(source_code)
        tokens, errors = tokenizer.tokenize()
        if not errors:
            write(lexer_path, Tokenizer.tokens_to_str(tokens))
        else:
            write(lexer_path, Tokenizer.errors_to_str(errors))
            continue

        # 2. Syntactic Analysis - build parse tree
        parser = LL1Parser(tokens)
        try:
            parse_tree = parser.parse()
            write(parser_path, LL1Parser.parse_tree_to_str(parse_tree))
        except Exception as err:
            write(parser_path, f'Parse error: {err}')
            continue

        # 3. Syntactic Analysis - build AST
        ast_gen = ASTGenerator()
        ast = ast_gen.build_ast(parse_tree)
        write(ast_path, ast_gen.ast_to_str(ast))

        # 4. Code Generation - generate intermediate code
        try:
            code_generator = CodeGenerator(ast)
            ir = code_generator.generate_ir()
            ir_str = '\n'.join(str(instr) for instr in ir)
            write(codegen_path, ir_str)
        except Exception as err:
            write(codegen_path, f'Code generation error: {err}')

        # 5. Code Generation with optimization
        try:
            code_generator_opt = CodeGenerator(ast, True)
            ir = code_generator_opt.generate_ir()
            ir_str = '\n'.join(str(instr) for instr in ir)
            write(optimized_path, ir_str)
        except Exception as err:
            write(optimized_path, f'Code generation error: {err}')


if __name__ == '__main__':
    main()

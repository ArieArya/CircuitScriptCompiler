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
	# for filename in ["wires_and_registers.circuit"]:
		file_path = os.path.join(src_dir, filename)
		filename_no_ext, ext = os.path.splitext(filename)

		if not os.path.isfile(file_path) or ext != '.circuit':
			continue

		test_output_dir = os.path.join(src_dir, 'tester_output', filename_no_ext)
		os.makedirs(test_output_dir, exist_ok=True)
		lexer_path = os.path.join(test_output_dir, 'lexer.txt')
		parser_path = os.path.join(test_output_dir, 'parser.txt')
		ast_path = os.path.join(test_output_dir, 'ast.txt')
		codegen_path = os.path.join(test_output_dir, 'codegen.txt')

		# Lexical Analysis
		source_code = read(f'sample_code/{filename}')
		tokenizer = Tokenizer(source_code)
		tokens, errors = tokenizer.tokenize()
		if not errors:
			write(lexer_path, Tokenizer.tokens_to_str(tokens))
		else:
			write(lexer_path, Tokenizer.errors_to_str(errors))
			continue

		# Syntactic Analysis - build parse tree
		parser = LL1Parser(tokens)
		try:
			parse_tree = parser.parse()
			write(parser_path, LL1Parser.parse_tree_to_str(parse_tree))
		except Exception as err:
			write(parser_path, f'Parse error: {err}')
			continue

		# Syntactic Analysis - build AST
		ast_gen = ASTGenerator()
		ast = ast_gen.build_ast(parse_tree)
		write(ast_path, ASTGenerator.ast_to_str(ast))

		# Code Generation - generate intermediate code
		code_generator = CodeGenerator(ast)
		code_generator.generate_ir()
		write(codegen_path, code_generator.get_code_str())


if __name__ == '__main__':
	main()

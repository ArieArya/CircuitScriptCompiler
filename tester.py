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
		print(f'Lexing file: {filename}')
		source_code = read_source_code_from_file(f'sample_code/{filename}')
		tokenizer = Tokenizer(source_code)
		tokens, errors = tokenizer.tokenize()
		print('Tokens:')
		for token in tokens:
			print(token)
		if errors:
			print()
			print('Errors:')
			for lexeme, idx in errors:
				print(f'Error parsing {repr(lexeme)} at index {idx}.')
			print()
			continue
		print()

		# Syntactic Analysis - build parse tree
		print('Building Parse Tree from token stream')
		parser = LL1Parser(tokens)
		parser.parse()
		parser.printParseTree()
		print()

		# Syntactic Analysis - build AST
		print('Building AST from Parse Tree')
		astGen = ASTGenerator(parser.parse_tree)
		astGen.buildAst(astGen.parse_tree)
		astGen.printAst()



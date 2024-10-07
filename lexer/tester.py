import os
from lexer import Lexer

def read_source_code_from_file(file_path):
    # Reads the source code from a text file
    with open(file_path, 'r') as file:
        return file.read()


if __name__ == "__main__":
	source_code_dir = "./sample_code/"

	for filename in os.listdir(source_code_dir):
		file_path = os.path.join(source_code_dir, filename)

		if os.path.isfile(file_path):
			print(f"\nLexing file: {filename}")
			try:
				source_code = read_source_code_from_file(file_path)
				lexer = Lexer(source_code)
				tokens = lexer.tokenize()
				for token in tokens:
					print(token)
			except Exception as e:
				print(f"Error lexing file {filename}: {e}")
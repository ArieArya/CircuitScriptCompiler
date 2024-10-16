import os
from tokenizer import Tokenizer


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

        print(f'Lexing file: {filename}')
        source_code = read_source_code_from_file(file_path)

        tokenizer = Tokenizer(source_code)
        tokens, errors = tokenizer.tokenize()

        print('Tokens:')
        for lexeme, token in tokens:
            print(f'{token} (Lexeme = {repr(lexeme)})')

        if errors:
            print()

            print('Errors:')
            for lexeme, idx in errors:
                print(f'Error parsing {repr(lexeme)} at index {idx}.')

        print()

# CircuitScript Tokenizer

## How to Run

First, note that sample codes that will be tokenized are stored under `sample_code/*.circuit`.

1. Ensure docker is installed: https://docs.docker.com/engine/install/
2. Build the docker image as specified in the Dockerfile: `docker build -t circuit-script-compiler .`
3. Run the docker container: `docker run circuit-script-compiler`

The output of the script will show the tokenization outputs of the sample scripts stored under `sample_code/*.circuit`. The expected output is found in `sample_code/expected_output/`.

## Lexical Specification

Please find the README under `lexer/README.md` (HW1)

## Syntactic Specification

Please find the README under `parser/README.md` (HW2)

## Contributions

-   Arie Arya, ana2175
-   Jason Han, jjh2237

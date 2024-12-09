# CircuitScript Compiler

## How to Run

Note, this section specifies how to run our compiler. This includes all steps (lexer, parser, code generation, and code execution).

First, note that sample codes for our language that will be compiled are stored under `sample_code/*.circuit`.

1. Ensure docker is installed: https://docs.docker.com/engine/install/
2. Build the docker image as specified in the Dockerfile: `docker build -t circuit-script-compiler .`
3. Run the docker container: `docker run circuit-script-compiler`

The output of the script will show the compiler outputs run on each of the sample circuits stored under `sample_code/*.circuit`. The expected output is found in `sample_code/expected_output/`, while the actual generated output is found in `sample_code/tester_output/`. Note, errors in compilation / code generation will also be stored in this directory.

## Lexical Specification

Please find the README under `lexer/README.md` (HW1)

## Syntactic Specification

Please find the README under `parser/README.md` (HW2)

## Code Generation

Please find the README under `code_gen/README.md` (HW3)

## Contributions

-   Arie Arya, ana2175
-   Jason Han, jjh2237

# CircuitScript Compiler

## How to Run

First, note that sample codes that will be compiled are stored under `sample_code/*.circuit`.

1. Ensure docker is installed: https://docs.docker.com/engine/install/
2. Build the docker image as specified in the Dockerfile: `docker build -t circuit-script-compiler .`
3. Run the docker container: `docker run circuit-script-compiler`

The output of the script will show the compiler outputs run on each of the sample circuits stored under `sample_code/*.circuit`. The expected output is found in `sample_code/expected_output/`, while the generated output is found in `sample_code/tester_output/`. Note, errors in compilation / code generation will also be stored in this `tester_output` directory.

## Lexical Specification

Please find the README under `lexer/README.md` (HW1)

## Syntactic Specification

Please find the README under `parser/README.md` (HW2)

## Code Generation

Please find the README under `code_gen/README.md` (HW3)

## Contributions

-   Arie Arya, ana2175
-   Jason Han, jjh2237

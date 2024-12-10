# CircuitScript Compiler

## How to Run

Note, this section specifies how to run our compiler and VM (to read the IR from the compiler). This includes all steps (lexer, parser, code generation, and code execution).

Our compiler and VM is dockerized for ease of testing. Note that all sample source codes for our language that will be compiled are stored under `sample_code/*.circuit`.

Follow the steps below:

1. Ensure docker is installed: https://docs.docker.com/engine/install/
2. Build the docker image as specified in the Dockerfile: `docker build -t circuit-script-compiler .`
3. Run the docker container: `docker run circuit-script-compiler`.
    - This will compile all our sample source codes and run the IR on top of our VM. The output logs will be stored inside the docker container.
4. Copy the output logs from the container to your local machine. Make sure you run the below commands from the root directory of this project.
    - First, find the container ID of the container that ran the program: `docker ps -a`
    - Now, copy the compiler output locally: `docker cp <container-id>:app/sample_code/tester_output ./sample_code/tester_output_docker/`

The above command will store the output of the compiler into your local directory `./sample_code/tester_output_docker/`. Please view this directory to see the output of both the compiler and the VM for each circuit. Each circuit contains the following logs:

-   `1_lexer.txt`: contains the lexer output
-   `2_parser.txt`: contains the parser output
-   `3_ast.txt`: contains the AST of the program
-   `4_codegen.txt`: contains the intermediate representation (IR) of the program. This is not yet optimized.
-   `5_optimized.txt`: contains the optimized IR of the program.
-   `6_vm.txt`: contains the output of running the IR on top of the VM.

---

## Running the VM Individually

For running the VM on individual files, see [vm/README.md#executing-files](vm/README.md#executing-files).

For testing the VM on each sample code example, follow [vm/README.md#building](vm/README.md#building) for steps to build the VM binary, then execute `run_vm.py`.

The VM is automatically ran in the Dockerfile, so the above instructions are enough to get the VM output on the sample code.

---

## Lexical Specification

Please find the README under `lexer/README.md` (HW1)

## Syntactic Specification

Please find the README under `parser/README.md` (HW2)

## Code Generation

Please find the README under `code_gen/README.md` (HW3)

## Virtual Machine (VM)

Please find the README under `vm/README.md` (HW3)

## Contributions

-   Arie Arya, ana2175
-   Jason Han, jjh2237

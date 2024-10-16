# Lexer

---

## How to Run

First, note that sample codes that will be lexed are stored under `./sample_code/*.circuit`.

1. Ensure docker is installed: https://docs.docker.com/engine/install/
2. Build the docker image as specified in the Dockerfile: `docker build -t circuit-script-compiler .`
3. Run the docker container: `docker run circuit-script-compiler`

The output of the script will show the tokenization outputs of the sample scripts stored under `./sample_code/*.circuit`.

---

## Lexical Specification

For the first iteration, we can define the following tokens:

### KEYWORD

-   `wire` - a wire in the digital circuit
-   `reg` - register
-   `lut` - Lookup Table (LUT)
-   `and` - AND gate
-   `or` - OR gate
-   `not` - NOT gate
-   `xor` - XOR gate
-   `print` - prints content
-   `if` - for if statements

### OPERATOR

-   `=`
-   `==`

### PUNCTUATION

-   `(`
-   `)`
-   `;`
-   `,`

## INTLITERAL

-   `1`
-   `0`
-   Or other integers when using buses in later implementations

---

## Contributions

-   Arie Arya, ana2175
-   Jason Han, jjh2237

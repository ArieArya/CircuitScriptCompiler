# Lexer

---

## How to Run

First, note that sample codes that will be lexed are stored under `./sample_code/*.txt`. The `tester.py` script will automatically read all scripts under this directory and tokenizes them.

1. Ensure Python 3 interpreter is available
2. Either execute the bash script `bash run_lexer.sh` or execute the Python script directly `python3 tester.py`.

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
-   `nand` - NAND gate
-   `print` - prints content

### OPERATOR

-   `=`

### PUNCTUATION

-   `(`
-   `)`
-   `{`
-   `}`
-   `;`
-   `,`

## INTLITERAL

-   `1`
-   `0`
-   Or other integers when using buses in later implementations

---

## Contributions

-   Arie Arya, ana2175
-   Jason Han, jjh2237

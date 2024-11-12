# Syntactic Specification

We can construct a simplified Context-Free Grammar (CFG) for our compiler. The list of terminals are:

-   `KEYWORD("wire")`, `KEYWORD("reg")`, `KEYWORD("lut")`, `KEYWORD("and")`, `KEYWORD("or")`, `KEYWORD("not")`, `KEYWORD("xor")`, `KEYWORD("print")`, `KEYWORD("if")`
-   `OPERATOR("=")`, `OPERATOR("==")`
-   `LPAREN`
-   `RPAREN`
-   `SEMICOLON`
-   `COMMA`
-   `DIGIT`
-   `IDENTIFIER`

The list of non-terminals are:

-   `Program`: root non-terminal representing the whole program
-   `StatementList`: a sequence of statements / lines in our program
-   `Statement`: a single statement / line of code.
-   `Declaration`: a declaration of wires, registers, or LUTs
-   `Assignment`: an assignment of a value or expression to an identifier
-   `PrintStmt`: a print statement
-   `IfStmt`: an if statement for conditional logic
-   `Expression`: a logical arithmetic expression
-   `GateExpression`: logical gate expressions like `and`, `or`, `xor`, `nand`
-   `Arguments`: arguments for gate expressions or certain keywords (e.g. LUTs)

The Context-Free Grammar can be defined below:

```
Program         -> StatementList
StatementList   -> Statement SEMICOLON StatementList | ε
Statement       -> Declaration | Assignment | PrintStmt | IfStmt
Declaration     -> KEYWORD("wire") IDENTIFIER | KEYWORD("reg") IDENTIFIER | KEYWORD("wire") IDENTIFIER OPERATOR("=") Expression | KEYWORD("reg") IDENTIFIER OPERATOR("=") Expression | KEYWORD("lut") LPAREN Arguments RPAREN StatementList
Assignment      -> IDENTIFIER OPERATOR("=") Expression
PrintStmt       -> KEYWORD("print") LPAREN Expression RPAREN
IfStmt          -> KEYWORD("if") LPAREN Expression OPERATOR("==") Expression RPAREN Statement
Expression      -> GateExpression | IDENTIFIER | DIGIT
GateExpression  -> GateType LPAREN Arguments RPAREN
GateType        -> KEYWORD("and") | KEYWORD("or") | KEYWORD("not") | KEYWORD("xor") | KEYWORD("nand")
Arguments       -> Expression Arguments'
Arguments'      -> COMMA Arguments | ε
```

From here, we can construct an LL(1) Parsing table that maps current terminal to the next production rule. This is implemented in `ll1_parse_table.py`.

| **Non-Terminal**   | `KEYWORD("wire")`                                     | `KEYWORD("reg")`                                     | `KEYWORD("lut")`                                       | `IDENTIFIER`                          | `KEYWORD("print")`                          | `KEYWORD("if")`                                                              | `KEYWORD("and")`                   | `KEYWORD("or")`                    | `KEYWORD("not")`                   | `KEYWORD("xor")`                   | `KEYWORD("nand")`                  | `DIGIT`                 | `SEMICOLON` | `RPAREN` | `COMMA`            | `OPERATOR("=")` | `OPERATOR("==")` | `$` |
| ------------------ | ----------------------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------ | ------------------------------------- | ------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------- | ---------------------------------- | ---------------------------------- | ---------------------------------- | ---------------------------------- | ----------------------- | ----------- | -------- | ------------------ | --------------- | ---------------- | --- |
| **Program**        | `StatementList`                                       | `StatementList`                                      | `StatementList`                                        | `StatementList`                       | `StatementList`                             | `StatementList`                                                              | -                                  | -                                  | -                                  | -                                  | -                                  | -                       | -           | -        | -                  | -               | -                | -   |
| **StatementList**  | `Statement SEMICOLON StatementList`                   | `Statement SEMICOLON StatementList`                  | `Statement SEMICOLON StatementList`                    | `Statement SEMICOLON StatementList`   | `Statement SEMICOLON StatementList`         | `Statement SEMICOLON StatementList`                                          | -                                  | -                                  | -                                  | -                                  | -                                  | -                       | -           | -        | -                  | -               | -                | ε   |
| **Statement**      | `Declaration`                                         | `Declaration`                                        | `Declaration`                                          | `Assignment`                          | `PrintStmt`                                 | `IfStmt`                                                                     | -                                  | -                                  | -                                  | -                                  | -                                  | -                       | -           | -        | -                  | -               | -                | -   |
| **Declaration**    | `KEYWORD("wire") IDENTIFIER OPERATOR("=") Expression` | `KEYWORD("reg") IDENTIFIER OPERATOR("=") Expression` | `KEYWORD("lut") LPAREN Arguments RPAREN StatementList` | -                                     | -                                           | -                                                                            | -                                  | -                                  | -                                  | -                                  | -                                  | -                       | -           | -        | -                  | -               | -                | -   |
| **Assignment**     | -                                                     | -                                                    | -                                                      | `IDENTIFIER OPERATOR("=") Expression` | -                                           | -                                                                            | -                                  | -                                  | -                                  | -                                  | -                                  | -                       | -           | -        | -                  | -               | -                | -   |
| **PrintStmt**      | -                                                     | -                                                    | -                                                      | -                                     | `KEYWORD("print") LPAREN Expression RPAREN` | -                                                                            | -                                  | -                                  | -                                  | -                                  | -                                  | -                       | -           | -        | -                  | -               | -                | -   |
| **IfStmt**         | -                                                     | -                                                    | -                                                      | -                                     | -                                           | `KEYWORD("if") LPAREN Expression OPERATOR("==") Expression RPAREN Statement` | -                                  | -                                  | -                                  | -                                  | -                                  | -                       | -           | -        | -                  | -               | -                | -   |
| **Expression**     | `GateExpression`                                      | -                                                    | -                                                      | `IDENTIFIER`                          | -                                           | -                                                                            | `GateExpression`                   | `GateExpression`                   | `GateExpression`                   | `GateExpression`                   | `GateExpression`                   | `DIGIT`                 | -           | -        | -                  | -               | -                | -   |
| **GateExpression** | -                                                     | -                                                    | -                                                      | -                                     | -                                           | -                                                                            | `GateType LPAREN Arguments RPAREN` | `GateType LPAREN Arguments RPAREN` | `GateType LPAREN Arguments RPAREN` | `GateType LPAREN Arguments RPAREN` | `GateType LPAREN Arguments RPAREN` | -                       | -           | -        | -                  | -               | -                | -   |
| **GateType**       | -                                                     | -                                                    | -                                                      | -                                     | -                                           | -                                                                            | `KEYWORD("and")`                   | `KEYWORD("or")`                    | `KEYWORD("not")`                   | `KEYWORD("xor")`                   | `KEYWORD("nand")`                  | -                       | -           | -        | -                  | -               | -                | -   |
| **Arguments**      | `Expression Arguments'`                               | -                                                    | -                                                      | `Expression Arguments'`               | -                                           | -                                                                            | `Expression Arguments'`            | `Expression Arguments'`            | `Expression Arguments'`            | `Expression Arguments'`            | `Expression Arguments'`            | `Expression Arguments'` | -           | -        | -                  | -               | -                | -   |
| **Arguments'**     | -                                                     | -                                                    | -                                                      | -                                     | -                                           | -                                                                            | -                                  | -                                  | -                                  | -                                  | -                                  | -                       | -           | ε        | `COMMA Arguments'` | -               | -                | -   |

---

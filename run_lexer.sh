#!/bin/bash

python3 tester.py

if [ $? -eq 0 ]; then
    echo "Lexer executed successfully."
else
    echo "Error: Lexer execution failed."
fi

# S126-HIT137-SOFTWARE-NOW-A02
A group project that applied file encryption/decryption and a mathematical expression evaluator by means of recursive descent parsing.

# HIT137 – Assignment 2

This repository contains solutions for **HIT137 Assignment 2**.

The assignment includes two programming tasks:

---

# Question 1 – Encryption and Decryption

This program reads text from a file and applies a custom encryption method based on two user inputs: **shift1** and **shift2**.

## Features
- Reads text from `raw_text.txt`
- Encrypts the text using specific alphabet shifting rules
- Saves encrypted output to `encrypted_text.txt`
- Decrypts the encrypted text
- Saves decrypted output to `decrypted_text.txt`
- Verifies whether decrypted text matches the original text

## Files
question-1/
- question1.py
- raw_text.txt
- encrypted_text.txt
- decrypted_text.txt

## How to run
Open terminal and run:

cd question-1
py question1.py

Enter values for shift1 and shift2 when prompted.

---

# Question 2 – Mathematical Expression Evaluator

This program reads mathematical expressions from a file, evaluates them using recursive descent parsing, and writes results to an output file.

## Features
- Supports operators: +, -, *, /
- Supports parentheses
- Supports unary negation (example: -5, --5)
- Supports implicit multiplication (example: 2(3+4))
- Generates parse tree
- Generates token list
- Handles errors (invalid symbols, divide by zero)
- Writes results to `output.txt`

## Files
question-2/
- q2.py (tokenizer)
- parser_refactored.py (parser)
- question2.py (main evaluator)
- input.txt
- output.txt

## How to run

cd question-2
py question2.py

The program reads expressions from input.txt and creates output.txt automatically.

---

# Output Format

Each expression produces:

Input: original expression  
Tree: parse tree structure  
Tokens: list of tokens  
Result: calculated result or ERROR  

---

# Author
Manish Chaudhary

Student ID: 400984
himanhsu prabhat
student ID: 400927
Enosh Basnet
student ID: 400562

---

# GitHub Repository
Link included in github_link.txt

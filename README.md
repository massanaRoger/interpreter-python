# Custom Language Interpreter

## Project Overview

Welcome to the Calculator Language Interpreter project. This project implements a simple, dynamically-typed programming language with support for basic arithmetic operations, variable assignments, control structures, and print statements. The interpreter is implemented in Python and supports both an interactive REPL and script execution.

### Team Members
- **Roger Massana**
- **Joel Teodoro**

## Prerequisites

- Python 3.6 or higher

## Running the REPL
To start the interactive REPL, run:
```
python repl.py
```

## Running a Script
To execute a script written in the custom language, use:

```
python execute.py path/to/your_script.scl
```

## REPL Usage
Once you start the REPL, you can enter commands interactively:


```
Welcome to the interactive language REPL. Type 'exit' to quit.
>>> x = 10;
>>> y = 20;
>>> print(x + y);
30
>>> if (x < y) { print "x is less than y";
```

## Language Specification

### 1. **Data Types**
- **Integers**: Support for whole numbers.
- **Floats**: Support for decimal numbers.
- **Strings**: For error messages or other outputs (optional).

### 2. **Variables**
- Variables can be named with any combination of letters and underscores (not starting with a number).
- Variables are dynamically typed and can store integers, floats, or strings.

### 3. **Expressions**
- **Arithmetic Operations**: Addition (+), subtraction (-), multiplication (*), and division (/).
- **Parentheses** to influence precedence.

### 4. **Statements**
- **Assignment**: Set and update the value of variables.
- **Print**: Output the results of expressions or variable values.

### 5. **Control Structures**
- **If Statements**: Basic conditional evaluation (optional for complexity).

### 6. **Comments**
- Single-line comments start with `//`.

## Syntax Definition

Here’s how the syntax of each component could look:

```ebnf
program     ::= { statement }

statement   ::= assign_statement | print_statement | if_statement | comment

assign_statement ::= identifier '=' expr ';'

print_statement ::= 'print' (expr | string) ';'

if_statement ::= 'if' '(' expr ')' '{' program '}' ['else' '{' program '}']

expr        ::= comparison_expr

comparison_expr ::= addition_expr {('==' | '!=' | '<' | '>' | '<=' | '>=') addition_expr}

addition_expr ::= multiplication_expr {('+' | '-') multiplication_expr}

multiplication_expr ::= primary_expr {('*' | '/') primary_expr}

primary_expr ::= number | identifier | '(' expr ')' | unary_expr

identifier  ::= [a-zA-Z_][a-zA-Z0-9_]*

number      ::= [0-9]+ ('.' [0-9]+)?

string      ::= '"' [^"]* '"'

comment     ::= '//' [^\n]*
```

### Example code
```
// Initialize variables
x = 15;
y = 10;

// Compute sum
result = x + y;
print "The result is: ";
print result;

// Conditional statement
if (result > 20) {
    print "Result is greater than 20.";
} else {
    print "Result is 20 or less.";
}
```

## Architecture

### Abstract Syntax Tree (AST)
The Abstract Syntax Tree (AST) represents the hierarchical structure of the source code. The following AST node classes are defined:

- **ASTNode**: Base class for all AST nodes.
- **BinaryOperation**: Represents a binary operation (e.g., addition, subtraction).
- **Number**: Represents a numerical value.
- **String**: Represents a string value.
- **Variable**: Represents a variable.
- **AssignmentStatement**: Represents a variable assignment statement.
- **PrintStatement**: Represents a print statement.
- **IfStatement**: Represents an if statement.
- **Block**: Represents a block of statements.

## Lexer

The lexer tokenizes the source code into a sequence of tokens. It uses regular expressions to identify different types of tokens, such as numbers, strings, keywords, operators, and identifiers. The lexer processes the source code character by character and matches them against predefined token specifications. It generates tokens for valid sequences and skips over whitespace and comments. Any unrecognized characters result in an error.

### Key Responsibilities:
- **Tokenization**: Breaking the input source code into meaningful tokens.
- **Handling Whitespace and Comments**: Ignoring spaces, tabs, and comments to focus on the actual code content.
- **Error Handling**: Identifying and reporting illegal characters in the source code.

## Parser

The parser converts the sequence of tokens produced by the lexer into an Abstract Syntax Tree (AST). It follows the grammar rules of the language to construct the hierarchical structure of the source code. The parser processes tokens in a recursive descent manner, building the AST node by node.

### Key Responsibilities:
- **Parsing Expressions**: Handling arithmetic and logical expressions according to operator precedence and associativity.
- **Constructing AST**: Building a tree structure that represents the code's syntax, including operations, variable assignments, and control structures.
- **Error Handling**: Detecting and reporting syntax errors, such as unexpected tokens or mismatched parentheses.

## Interpreter

The interpreter traverses the AST and executes the code. It evaluates expressions, performs operations, and manages the program state through a symbol table (environment) that stores variable values. The interpreter supports basic arithmetic, logical operations, variable assignments, and control structures like if statements.

### Key Responsibilities:
- **Expression Evaluation**: Computing the results of arithmetic and logical expressions.
- **State Management**: Maintaining the environment to store and update variable values.
- **Control Flow Execution**: Handling if statements and other control structures to direct the flow of the program.
- **Error Handling**: Identifying runtime errors, such as undefined variables or division by zero, and reporting them.

### REPL

The REPL (Read-Eval-Print Loop) provides an interactive environment where users can type and execute code line by line. The REPL class handles user input, tokenizes it, parses it, and interprets it in a loop. It uses the same environment for the entire session, allowing variable values to persist across multiple lines of input.

## Testing

Unit tests are provided to ensure the correctness of the lexer, parser, and interpreter. The tests are located in the tests directory. To run the tests, use the following command:
```sh
python -m unittest discover tests
```


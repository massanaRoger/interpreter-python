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

unary_expr  ::= ('+' | '-') primary_expr

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
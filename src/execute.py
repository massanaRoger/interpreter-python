import sys
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter


def run_source_file(filename):
    try:
        with open(filename, 'r') as file:
            code = file.read()

        # Tokenize the code
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        # Parse the tokens
        parser = Parser(tokens)
        ast = parser.parse()

        # Interpret the AST
        interpreter = Interpreter(ast)
        interpreter.interpret()

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python execute.py source_file.scl")
    else:
        source_file = sys.argv[1]
        run_source_file(source_file)

from src.interpreter import Interpreter
from src.lexer import Lexer
from src.parser import Parser


class REPL:
    def __init__(self):
        self.environment = {}

    def start(self):
        print("Welcome to the interactive language REPL. Type 'exit' to quit.")
        while True:
            try:
                user_input = input('>>> ')
                if user_input.lower() == 'exit':
                    break

                # Tokenize input
                lexer = Lexer(user_input)
                tokens = lexer.tokenize()

                # Parse tokens
                parser = Parser(tokens)
                ast = parser.parse()

                # Interpret AST
                interpreter = Interpreter(ast)
                interpreter.environment = self.environment  # Use the same environment
                interpreter.interpret()

            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    repl = REPL()
    repl.start()
